"""
© 2021 @n4i8x9a
https://github.com/n4i8x9a
"""

import argparse
import os
import re
import requests
import threading
import time
from alive_progress import alive_bar

VERSION = "1.0"
GITHUB = "https://github.com/n4i8x9a"


class DownloaderException(Exception):
    def __init__(self, text):
        self.txt = text


URL_WITH_ERRORS = []
PROGRESS = {'successful': 0, 'total': 0, 'current': 0}


def save_error_log(directory, list_of_url):
    s = "THIS FILES FAILED TO DOWNLOAD : \n\n"
    for l in list_of_url:
        s += "URL : \'%s\' ; Error : \'%s\' \n\n" % (l['url'], l['error'])
    with open(directory + '/error_log.txt', 'w') as f:
        f.write(s)
        f.close()


def indicate_progress(directory):
    global PROGRESS, URL_WITH_ERRORS
    current = PROGRESS['successful']
    with alive_bar(PROGRESS['total']) as bar:
        while PROGRESS['successful'] <= PROGRESS['total']:
            if PROGRESS['successful'] > current:
                for i in range(PROGRESS['successful'] - current):
                    bar()
            if PROGRESS['current'] == PROGRESS['total']:
                break
            else:
                current = PROGRESS['successful']
            time.sleep(0.1)

    if len(URL_WITH_ERRORS) == 0:
        print("All files download successful !")
    else:
        save_error_log(directory, URL_WITH_ERRORS)
        print("%d files failed to load. See details in %s" % (len(URL_WITH_ERRORS), directory + '/error_log.txt'))


def parse_file(filename):
    regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    f = open(filename, 'r')
    s = f.read()
    f.close()
    url_list = re.findall(regex, s)
    return url_list


def download_file(url, filename):
    req = requests.get(url)

    if req.status_code != 200:
        raise Exception("HTTP Error %d" % req.status_code)
    else:
        with open(filename, 'wb') as f:
            f.write(req.content)
            f.close()


def download_files(url_list, start_index, end_index, directory):
    global URL_WITH_ERRORS, PROGRESS

    for i in range(start_index, end_index):
        url = url_list[i]
        file_type = url.split('.')[-1]
        name = str(i + 1)
        try:
            download_file(url, directory + "/" + name + '.' + file_type)
            PROGRESS['successful'] += 1
        except Exception as e:
            print('failed to download %s  ' % url)
            URL_WITH_ERRORS.append({'url': url, 'error': e})
        PROGRESS['current'] += 1


def main(url_file, number_of_threads, destination_folder):
    global PROGRESS
    try:
        if number_of_threads <= 0:
            raise DownloaderException('Number of threads should be > 0 !')

        if os.path.isfile(url_file) and os.path.isdir(destination_folder):

            url_list = parse_file(url_file)
            print("%d files to download" % len(url_list))
        else:
            raise DownloaderException(
                'TXT file with URL or destination folder does not exist! See \'--help\' for more information.')

        PROGRESS['total'] = number_of_files = len(url_list)
        files_in_thread = number_of_files // number_of_threads
        list_of_threads = []

        indicate = threading.Thread(target=indicate_progress, args=(destination_folder,))

        if files_in_thread == 0:
            list_of_threads.append(
                threading.Thread(target=download_files,
                                 args=(url_list, 0, number_of_files, destination_folder)))
        else:

            for i in range(number_of_threads):
                if i < number_of_threads - 1:
                    list_of_threads.append(
                        threading.Thread(target=download_files,
                                         args=(
                                             url_list, i * files_in_thread, files_in_thread * (i + 1),
                                             destination_folder
                                         )))
                else:
                    list_of_threads.append(
                        threading.Thread(target=download_files,
                                         args=(url_list, i * files_in_thread, number_of_files, destination_folder)))

        indicate.start()
        for t in list_of_threads:
            t.start()

    except DownloaderException as e:
        print(e)
        return -1

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Python multi threading file downloader v=%s . %s' % (VERSION, GITHUB))
    parser.add_argument("--u", help="This is path of TXT file with list of URLs")
    parser.add_argument("--d", default='', help="Path of destination folder")
    parser.add_argument("--t", default=20, help="Number of threads (20 is default)")
    args = parser.parse_args()
    main(url_file=str(args.u), number_of_threads=int(args.t), destination_folder=str(args.d))

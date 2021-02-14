# Python multi threading file downloader

### Install dependencies

`pip install alive_progress`

#

### Usage

`python downloader.py --u=files.txt --d=files --t=25`

`--u` is path of TXT file with URLs of files to download.
 
Example TXT file:
```
https://sun9-19.userapi.com/c856024/v856024483/1acdf3/9kbbWylPz3M.jpg
https://sun9-57.userapi.com/c856024/v856024483/1acdfc/KKnsQ_RkYJQ.jpg
https://sun9-58.userapi.com/c856024/v856024483/1ace06/gRTxnTHKvNU.jpg
```

`--d` is path of folder where files will downloaded.

`--t` is number of threads. Default value is 20.

If some files will failed to download, you can see details in `error_log.txt` in destination folder.

#
© 2021 @n4i8x9a

https://github.com/n4i8x9a
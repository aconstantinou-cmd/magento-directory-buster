#!/usr/bin/python
'''
    Usage:  ./TabulateURLs.py  [http//www.example.com]

'''
import requests
from tabulate import tabulate    # Need to first install tabulate with ==>   pip install tabulate
import sys
import time
import threading

class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)


adr = sys.argv[1]
if adr.endswith("/"):
    adr = adr.rstrip("/")

print("--------------------------------------------------------------------------------------------")

dirs=[["/downloader", 0,""], ["/admin",0,""], ["/downloader/.cache/community",0,""], ["/var/cache",0,""], ["/backups",0,""], ["/session",0,""], ["/media",0,""],["/rss/catalog/notifystock",0,""],["/rss/catalog/review",0,""],["/rss/order/new",0,""],["/errors",0,""],["/RELEASE_NOTES.txt",0,""],["/Robots.txt",0,""]]

scriptCheck=requests.head(adr + "/askdjflaskdjflasdfjadlskf", allow_redirects=False)
if scriptCheck.status_code!=404:
    print("Unexpected Result, check manualy", scriptCheck.status_code, scriptCheck.headers["Location"])
    exit()

spinner = Spinner()
counter = 0
while counter < len(dirs):
    sys.stdout.write(" [+] Requesting {0}... ".format(adr+dirs[counter][0]))
    sys.stdout.flush()
    spinner.start()

    resp = requests.head(adr + dirs[counter][0], allow_redirects=False)

    dirs[counter][1] = resp.status_code
    if resp.status_code == 200:
        dirs[counter][2] = "VULNERABLE"
    elif resp.status_code == 404:
        dirs[counter][2] = "Not Found"
    else:
        if resp.status_code == 403:
            dirs[counter][2] = "Unauthorised"
    #print('URL: {0}, Return Code: {1}'.format(dirs[counter], resp.status_code))
    spinner.stop()
    sys.stdout.write(" \b")
    sys.stdout.write("\n")
    sys.stdout.flush()
    counter+=1

print tabulate(dirs, tablefmt='grid')

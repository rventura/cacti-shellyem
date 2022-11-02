#!/usr/bin/env python3

import sys
import json
import urllib.request
import datetime

class Logger:
    def __init__(self, state, logfile="/var/log/cacti-shellyem.log"):
        self.fh = open(logfile, "a") if state else None

    def log(self, msg):
        if self.fh is not None:
            stamp = datetime.datetime.now().isoformat(' ', 'seconds')
            print(f"[{stamp}] {msg}", file=self.fh, flush=True)
    

def main(argv):
    dbg = Logger(True)
    try:
        host  = argv[1]
        index = int(argv[2])
        dbg.log(f"Called with host={host} and index={index}")
    except IndexError:
        print(f"*** Usage: {argv[0]} <hostname> <index>")
        return
    except ValueError:
        print("*** <index> argument must be an integer")
        return
    url = f"http://{host}/status"
    with urllib.request.urlopen(url) as fh:
        data = json.load(fh)
        dbg.log(f"Read JSON from {url} with {len(data)} keys")
    try:
        em = data['emeters'][index]
        if em['is_valid']:
            fs = [f"{k}:{em[k]}" for k in ('voltage', 'power', 'reactive', 'pf' )]
        dbg.log(f"Parsed {len(fs)} fields from JSON")
        print(' '.join(fs))
    except IndexError as ex:
        print(f"*** Error extracting data")
        dbg.log(f"Error parsing JSON: {ex}")
        return

if __name__=='__main__':
    main(sys.argv)

# EOF

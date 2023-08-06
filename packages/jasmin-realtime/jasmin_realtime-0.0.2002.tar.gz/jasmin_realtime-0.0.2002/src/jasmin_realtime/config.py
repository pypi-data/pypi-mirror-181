#!/usr/bin/env python
"""
high level support for doing this and that.
"""
from sources import MongoDB

from settings import *

script_log = "conf-> "
if __name__ == "__main__":
    print(" ", flush=True)
    print(" ", flush=True)
    print(f"{f'{script_log}*************** `Config watcher` ':*<68}", flush=True)
    print(f"{f'{script_log}***         Staring `Config watcher`':<65}"+"***", flush=True)
    print(f"{f'{script_log}*':*<68}", flush=True)

    print(f"{f'{script_log}*** Checking MongoDB connection settings...':<65}"+"***", flush=True)
    if config_ready is not True:
        print(
            f"{f'{script_log}*** no MongoDB configurations found':<65}"+"***", flush=True)
        print(f"{f'{script_log}*** Shutting down!!!':<65}"+"***", flush=True)
        print(f"{f'{script_log}*':*<68}", flush=True)
        exit()

    print(f"{f'{script_log}*** MongoDB READY!':<65}"+"***", flush=True)
    print(f"{f'{script_log}*** Set to use MongoDB connection':<65}" +
          "***", flush=True)
    print(f"{f'{script_log}*** ':<65}"+"***", flush=True)
    mongosource = MongoDB(
        database_name=MONGODB_MODULES_DATABASE, script_log=script_log)
    if mongosource.startConnection() is True:
        mongosource.stream(syncCurrentFirst=True)

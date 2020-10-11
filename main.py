
import os, time, getpass
import configparser as cfg

from sel_module import *

DAY = 86400 # day to seconds

if __name__ == "__main__":
    parser = cfg.ConfigParser()
    print("*** Provide your login details.")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    dv = boot()
    login(dv, username, password)
    while True:
        try:
            for listing in os.listdir():
                if "listing_" in listing:
                    parser.read(listing + "/data.cfg")
                    publish(dv, parser, listing)
            time.sleep(DAY)
        except KeyboardInterrupt:
            break
    killb(dv)

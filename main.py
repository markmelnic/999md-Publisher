
import os, time
import configparser as cfg
from argparse import ArgumentParser, RawTextHelpFormatter

from sel_module import *

DAY = 86400 # day to seconds

if __name__ == "__main__":
    cfgparser = cfg.ConfigParser()
    argparser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    argparser.add_argument("username", metavar="username", type=str, help="Login username.")
    argparser.add_argument("password", metavar="password", type=str, help="Login password.")
    args = argparser.parse_args()

    dv = boot()
    login(dv, args.username, args.password)
    while True:
        try:
            for listing in os.listdir():
                if "listing_" in listing:
                    cfgparser.read(listing + "/data.cfg")
                    publish(dv, cfgparser, listing)
            time.sleep(DAY)
        except KeyboardInterrupt:
            break
    killb(dv)

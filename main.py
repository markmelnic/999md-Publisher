
import os
import configparser as cfg

from sel_module import *

if __name__ == "__main__":
    parser = cfg.ConfigParser()
    with open("creds.txt", "r") as creds_file:
        creds = creds_file.readlines()
    dv = boot()
    login(dv, creds[0].strip("\n"), creds[1])
    for listing in os.listdir():
        if not "." in listing and not "__" in listing:
            parser.read(listing + "/data.cfg")
            publish(dv, parser, listing)
    killb(dv)

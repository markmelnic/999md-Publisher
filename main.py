
import os, getpass
import configparser as cfg

from sel_module import *

if __name__ == "__main__":
    parser = cfg.ConfigParser()
    print("*** Provide your login details.")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    dv = boot()
    login(dv, username, password)
    for listing in os.listdir():
        if not "." in listing and not "__" in listing:
            parser.read(listing + "/data.cfg")
            publish(dv, parser, listing)
    killb(dv)

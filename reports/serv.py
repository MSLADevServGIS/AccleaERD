"""Server Command Line Utility (WIP)
Author: Garin Wally; 5/9/2023

Good for executing code manually.
"""
import datetime as dt
from subprocess import Popen, PIPE


import click

#from edens_interface.edens_interface import 

@click.thing()  # TODO:
def connections():
    cmd = "python server_test/server_test.py"
    p = Popen(cmd, shell=True, stdout=PIPE)
    return p.communicate()

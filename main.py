#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import subprocess
import os
import os.path
import re
import sys
import platform

# "  BCLM  [ui8 ]  60 (bytes 3c)"
OUTPUT_RE = re.compile(r"  BCLM  \[([a-z0-9]*)\s*\]  ([0-9a-f]+) \(bytes (.+)\)")


def get_smc_binary_path(script_directory) -> str:
    smc_directory = os.path.join(script_directory, "smc-command")

    binary_path = os.path.join(smc_directory, "smc")
    exists = os.path.exists(binary_path)
    
    if not exists:
        current_dir = os.getcwd()
        os.chdir(smc_directory)
        out = subprocess.run(["make"], capture_output=True)
        os.chdir(current_dir)
        if out.returncode != 0:
            print("SMC build failed!", file=sys.stderr)
            print(out.stderr)
            exit(1)
        
        exists = os.path.exists(binary_path)
        if not exists:
            print("SMC binary does not exist at {}!".format(binary_path), file=sys.stderr)
            exit(1)
    
    return binary_path
        

def get_arguments():
    parser = argparse.ArgumentParser(description="Macbook battery charge limit using SMC")

    parser.add_argument("-c", 
                        dest="current",
                        default=False,
                        action="store_true",
                        help="Current limit value")

    parser.add_argument("-r", 
                        dest="reset",
                        default=False,
                        action="store_true",
                        help="Reset on default value (100)")

    parser.add_argument("-s", 
                        dest="set", 
                        type=int,
                        default=None,
                        help="Target charge limit in percents, from 40 to 100")

    args = parser.parse_args()
    
    return args


def get_and_check_current_battery_charge_limit(smc_binary_path) -> int:
    #./smc -r -k BCLM
    get_value_out = subprocess.run([smc_binary_path, "-k", "BCLM", "-r"], capture_output=True)
    # print(get_value_out)
    if (get_value_out.returncode != 0) or (len(get_value_out.stdout) == 0):
        print("Battery limit value read failed:", file=sys.stderr)
        print(get_value_out.stderr, file=sys.stderr)
        exit(1)

    out_string = get_value_out.stdout.decode("utf-8").rstrip("\n")
    # print(out_string)

    parse_result = OUTPUT_RE.match(out_string)
    if parse_result is None:
        error_text = "SMC out parse failed:\nvalid \"{}\"\ncurrent \"{}\"".format(
            "  BCLM  [ui8 ]  60 (bytes 3c)", 
            out_string
        )
        print(error_text, file=sys.stderr)
        exit(1)

    #print(get_value_out.stdout)
    value_type = parse_result.group(1)
    current_value = int(parse_result.group(2))
    #bytes_value = parse_result.group(3)
    
    value_type_valid = (value_type == "ui8")
    current_value_valid = (current_value >= 20) and (current_value <= 100)
    if not value_type_valid or not current_value_valid:
        error_text = \
            "Invalid SMC output values: type = {}, value = {}\n"\
            "must be: type = {}, value = {}"\
            .format(value_type, current_value, "ui8", "20 <= val <= 100")
        print(error_text, file=sys.stderr)
        exit(1)

    return current_value


def is_root_user() -> bool:
    return (os.geteuid() == 0)


def set_current_battery_charge_limit(smc_binary_path, value) -> int:
    is_root = is_root_user()
    if not is_root:
        print("Set limit must be run as root", file=sys.stderr)
        exit(1)

    if (value > 100) or (value < 20) or (not isinstance(value, int)):
        print("New limit integer value must be: 20 <= val <= 100", file=sys.stderr)
        exit(1)

    hex_value = hex(value).replace("0x", "")
    if hex_value is None:
        print("Value convert to hex failed", file=sys.stderr)
        exit(1)
    if len(hex_value) != 2:
        print("Value convert to hex failed, too short hex: {}".format(hex_value), file=sys.stderr)
        exit(1)

    # sudo ./smc -k BCLM -w 3c
    set_value_out = subprocess.run([smc_binary_path, "-k", "BCLM", "-w", hex_value], capture_output=True)
    # print(set_value_out)
    if (set_value_out.returncode != 0):
        print("Battery limit value set failed:", file=sys.stderr)
        print(set_value_out.stderr, file=sys.stderr)
        exit(1)

    return True


def change_battery_limit_value(smc_binary_path, value):
    current_value = get_and_check_current_battery_charge_limit(smc_binary_path)
    if current_value is None:
        print("Battery limit previous value read failed", file=sys.stderr)
        exit(1)

    print("Previous battery charge limit is {}%".format(current_value))

    success = set_current_battery_charge_limit(smc_binary_path, value)
    if success:
        new_value = get_and_check_current_battery_charge_limit(smc_binary_path)
        print("New battery charge limit is {}%".format(new_value))
    else:
        print("Battery limit value set failed", file=sys.stderr)
        exit(1)


def print_current_limit(smc_binary_path):
    current_value = get_and_check_current_battery_charge_limit(smc_binary_path)
    print("Current battery charge limit is {}%".format(current_value))    


def main():
    current_system = platform.system()
    if current_system != "Darwin":
        print("Script must be run using OSX platform only", file=sys.stderr)
        exit(1)

    # Script directory
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # SMC binary path
    smc_binary_path = get_smc_binary_path(script_directory)
    
    # Arguments
    args = get_arguments()

    if args.current:
        print_current_limit(smc_binary_path)
    elif args.set:
        change_battery_limit_value(smc_binary_path, args.set)
    elif args.reset:
        change_battery_limit_value(smc_binary_path, 60)
    else:
        print_current_limit(smc_binary_path)


if __name__ == "__main__":
    main()
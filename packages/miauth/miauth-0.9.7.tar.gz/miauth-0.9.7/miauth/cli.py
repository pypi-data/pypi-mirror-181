#
#     MiAuth - Authenticate and interact with Xiaomi devices over BLE
#     Copyright (C) 2021-2022  Daljeet Nandha
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
import sys
import os
import argparse

from miauth.mi.miclient import MiClient
from miauth.mi.m365client import M365Client
from miauth.nb.nbclient import NbClient
from miauth.nb.nbcrypto import NbCrypto

from miauth.ble.blue import BluePy

parser = argparse.ArgumentParser()
parser.add_argument("mac", help="mac address of target device")
parser.add_argument("-m", "--m365", action='store_true', help="use M365 protocol instead")
parser.add_argument("-n", "--nb", action='store_true', help="use Nb protocol instead")
parser.add_argument("-c", "--command", help="send command (w/o checksum) to uart and print reply")
parser.add_argument("-s", "--serial", action='store_true', help="retrieve serial number")
parser.add_argument("-f", "--fwver", action='store_true', help="retrieve firmware version")
parser.add_argument("-v", "--verbose", action='store_true', help="activate verbose (debug) log")

parser.add_argument("-r", "--register", action='store_true',
                    help="register with device / create token (caution: will lose bond to all other apps)")
parser.add_argument("-d", "--register_did", help="supply did for registeration (advanced)")
parser.add_argument("-t", "--token_file", default="./mi_token",
                    help="path to mi token file (default: ./mi_token)")

args = parser.parse_args()
print(args)


def nb_main(ble):
    nc = NbClient(ble, NbCrypto(), debug=args.verbose)

    print("Connecting")
    nc.connect()

    print("Authenticating")
    nc.auth()

    if args.command:
        resp = nc.comm(args.command)
        print("UART reply:", resp.hex(" "))

    # NOTE: don't send checksums!
    if args.serial:
        print("Retrieving serial number")
        resp = nc.comm("5aa5013d2001100e")
        print("Serial no.:", resp.decode())
    if args.fwver:
        print("Retrieving firmware version")
        resp = nc.comm("5aa5013d20011a10")
        print("Firmware version:", f"{resp[0]}.{resp[1]}")

    print("Disconnecting")
    nc.disconnect()


def m365_main(ble):
    mc = M365Client(ble, debug=args.verbose)

    print("Connecting")
    mc.connect()
    mc.recover_key()

    if args.command:
        resp = mc.comm(args.command)
        print("UART reply:", resp.hex(" "))

    # NOTE: don't send checksums!
    if args.serial:
        print("Retrieving serial number")
        resp = mc.comm("55aa032001100e")
        print("Serial no.:", resp.decode())
    if args.fwver:
        print("Retrieving firmware version")
        resp = mc.comm("55aa0320011a10")
        print("Firmware version:", f"{resp[0]}.{resp[1]}")

    print("Disconnecting")
    mc.disconnect()


def mi_main(ble):
    mc = MiClient(ble, debug=args.verbose)

    print("Connecting")
    mc.connect()

    if args.register:
        print("Registering")
        mc.register(did=args.register_did)
        mc.save_token(args.token_file)
        print("Saved token to:", args.token_file)

    if not mc.token:
        if not os.path.isfile(args.token_file):
            sys.exit("""
No authentication token found, register with '-r' or specify path to token file with '-t <path>'.
Caution: After registration this device will lose coupling to all other apps (remove/add device in Mi Home app if needed).
                     """)

        print("Loading token from:", args.token_file)
        mc.load_token(args.token_file)

    print("Logging in...")
    mc.login()

    if args.command:
        print("Sending command:", args.command)
        resp = mc.comm(args.command)
        print("UART reply:", resp.hex(" "))

    # NOTE: don't send checksum
    if args.serial:
        print("Retrieving serial number")
        resp = mc.comm("55aa032001100e")
        print("Serial number:", resp.decode())
    if args.fwver:
        print("Retrieving firmware version")
        resp = mc.comm("55aa0320011a10")
        print("Firmware version:", f"{resp[0]}.{resp[1]}")

    print("Disconnecting")
    mc.disconnect()


def main():
    # default BLE lib is bluepy
    ble = BluePy(args.mac)

    if args.nb:
        print("Using Nb")
        nb_main(ble)
    elif args.m365:
        m365_main(ble)
    else:
        print("Using Mi")
        mi_main(ble)


if __name__ == "__main__":
    main()

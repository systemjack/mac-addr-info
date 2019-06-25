#!/usr/bin/env python
"""
This application queries the macaddress.io MAC address lookup API to retrieve related metadata for a given address.
"""

import os
import sys
import argparse
import re
import requests

macaddressio = "https://api.macaddress.io/v1"
epilog = 'note: accepts mac address from stdin if not supplied as argument'

parser = argparse.ArgumentParser(epilog=epilog)
parser.add_argument('mac', nargs='?', help='mac address to query')
parser.add_argument('--key', default=os.environ.get('MACADDRESS_API_KEY', None),
        help='your macaddress.io api key (defaults to MACADDRESS_API_KEY environment variable)')
parser.add_argument('--output', choices=['vendor', 'json', 'xml', 'csv'], default='vendor',
        help='output format to request (default: vendor)')
parser.add_argument('--api', default=macaddressio,
        help='api path (default: {})'.format(macaddressio))


def lookup_mac(api, key, output, mac):
    try:
        payload = {'apiKey': key, 'output': output, 'search': mac}
        r = requests.get(api, params=payload)
        return r.text
    except Exception as e:
        sys.stderr.write('error: problem making api request to {}: {}\n'.format(api, e))
        sys.exit(1)


def main():
    args = parser.parse_args()

    if not args.mac:
        if not sys.stdin.isatty():
            args.mac = sys.stdin.read()
        else:
            sys.stderr.write('error: must provide mac address\n\n')
            parser.print_help(sys.stderr)
            sys.exit(1)

    if not re.match('[0-9a-f]{2}([-:.]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$', args.mac.lower()):
        sys.stderr.write('error: invalid mac address: {}\n'.format(args.mac))
        sys.exit(1)

    if not args.key:
        sys.stderr.write('error: no api key specified\n\n')
        parser.print_help(sys.stderr)
        sys.exit(1)

    print(lookup_mac(args.api, args.key, args.output, args.mac))


if __name__ == '__main__':
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

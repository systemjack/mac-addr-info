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


def parse_args():
    epilog = 'note: accepts newline delimited mac addresses from stdin as well'
    parser = argparse.ArgumentParser(epilog=epilog)
    parser.add_argument('mac', nargs='*', help='mac address(es) to query')
    parser.add_argument('--key', default=os.environ.get('MACADDRESS_API_KEY', None),
            help='your macaddress.io api key (defaults to MACADDRESS_API_KEY environment variable)')
    parser.add_argument('--output', choices=['vendor', 'json', 'xml', 'csv'], default='vendor',
            help='output format to request (default: vendor)')
    parser.add_argument('--api', default=macaddressio,
            help='api path (default: {})'.format(macaddressio))
    return parser, parser.parse_args()


def is_valid_mac(mac):
    return re.match('[0-9a-f]{2}([-:.]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$', mac.lower())


def lookup_mac(api, key, output, mac):
    try:
        payload = {'apiKey': key, 'output': output, 'search': mac}
        r = requests.get(api, params=payload)
        return r.text
    except Exception as e:
        sys.stderr.write('error: problem making api request to {}: {}\n'.format(api, e))
        sys.exit(1)


def main():
    parser, args = parse_args()

    if not args.key:
        sys.stderr.write('error: no api key specified\n\n')
        parser.print_help(sys.stderr)
        sys.exit(1)

    if not args.mac:
        if not sys.stdin.isatty():
            args.mac = sys.stdin.readlines()
        else:
            sys.stderr.write('error: must provide mac address\n\n')
            parser.print_help(sys.stderr)
            sys.exit(1)

    for m in args.mac:
        m = m.rstrip()
        if is_valid_mac(m):
            print(lookup_mac(args.api, args.key, args.output, m))
        else:
            sys.stderr.write('warning: skipping invalid mac address: {}\n'.format(m))


if __name__ == '__main__':
    main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

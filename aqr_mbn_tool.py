#! /usr/bin/python

'''
The MIT License (MIT)

Copyright (c) 2024 Paweł Owoc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
'''

#usage: aqr_mbn_tool.py [-h] [-o FILE] AQR_FW
#
#AQR firmware MBN header tool
#
#positional arguments:
#  AQR_FW                add MBN header to AQR_FW file
#
#options:
#  -h, --help            show this help message and exit
#  -o FILE, --output FILE
#                        output file name

import io
from argparse import ArgumentParser
from mmap import mmap, ACCESS_COPY
from struct import pack

IMG_TYPE = 0x13
VERSION = 0x3
BASE = 0x44000000

MBN_FILE = 'aqr_fw.mbn'


def mbn_header(size):
    header = pack(
        '<10L',
        IMG_TYPE,
        VERSION,
        0x0,
        BASE,
        size,
        size,
        BASE + size,
        0x0,
        BASE + size,
        0x0
    )

    return(header)


def cmd_add_mbn_header(args):
    with io.open(args.add_mbn_header, 'rb') as f:
        aqr_fw = mmap(f.fileno(), 0, access=ACCESS_COPY)

        fw_size = len(aqr_fw)
        header = mbn_header(fw_size)
        mbn_fw = header + aqr_fw
        mbn_fw_size = len(mbn_fw)

        print(f'AQR firmware size with MBN header: {mbn_fw_size}B ({hex(mbn_fw_size)})')

        with io.open(args.output or MBN_FILE, 'wb') as m:
            m.write(mbn_fw)


def main():
    parser = ArgumentParser(description='AQR firmware MBN header tool')

    parser.add_argument('add_mbn_header', metavar='AQR_FW',
                        help='add MBN header to AQR_FW file')

    parser.add_argument('-o', '--output', metavar='FILE',
                        help='output file name')

    args = parser.parse_args()

    if args.add_mbn_header:
        return cmd_add_mbn_header(args)


if __name__ == '__main__':
    main()
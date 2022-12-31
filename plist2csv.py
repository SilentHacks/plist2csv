#!/usr/bin/env python3

import csv
import json
import plistlib
import random
import sys
import time

csv.register_dialect('UniversalScrobbler', delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_ALL)
OUT = sys.argv[2] if len(sys.argv) == 3 else 'out.csv'


def write2csv(iterable, array):
    scrobbles = 0

    with open(OUT, 'w') as fc:
        writer = csv.writer(fc, dialect='UniversalScrobbler')
        for t in iterable:
            try:
                title = array[t]['Name']
            except KeyError:
                try:
                    title = array[t]['Title']
                except KeyError:
                    print('Record {} is missing mandatory title information, skipping!'.format(t), file=sys.stderr)
                    continue

            try:
                artist = array[t]['Artist']
            except KeyError:
                print(array[t])
                print('Record {} is missing mandatory artist information, skipping!'.format(t), file=sys.stderr)
                continue

            try:
                album = array[t]['Album']
            except KeyError:
                album = ''

            try:
                album_artist = array[t]['Album Artist']
            except KeyError:
                album_artist = ''

            try:
                length = int(array[t]['Total Time']/1000)
            except KeyError:
                try:
                    length = int(array[t]['Track Duration'])
                except KeyError:
                    length = ''

            try:
                play_count = array[t]['Play Count']
            except KeyError:
                try:
                    play_count = array[t]['Track Play Count']
                except KeyError:
                    print('Failed to get play count for record {}, skipping!'.format(t), file=sys.stderr)
                    continue

            if play_count == 0:
                print('Zero plays for record {}!'.format(t), file=sys.stderr)

            for _ in range(play_count):
                date = int(time.time()) - random.randint(0, 1209600)  # get a random date in the last 2 weeks
                date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(date))  # convert to ISO 8601
                writer.writerow([artist, title, album, date, album_artist, length])
                scrobbles += 1

    return scrobbles


def xml2csv():
    with open(sys.argv[1], 'rb') as fp:
        pl = plistlib.load(fp)

    return write2csv(pl['Tracks'], pl['Tracks'])


def json2csv():
    with open(sys.argv[1], 'r') as fp:
        pl = json.load(fp)

    return write2csv(range(len(pl)), pl)


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print('usage: {} <input.xml> [output.csv]'.format(sys.argv[0]))
        return

    scrobbles = xml2csv() if sys.argv[1].endswith('.xml') else json2csv()
    print('{} scrobbles written to {}'.format(scrobbles, OUT))


if __name__ == '__main__':
    main()

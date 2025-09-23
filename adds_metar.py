#!/usr/bin/env python3
"""Fetches metars from the ADDS Text Data Server.

    It is now called the "Aviation Weather Center Data API".

    Documentation: https://aviationweather.gov/data/api/#schema

    URL = 'https://aviationweather.gov/api/data/metar?format=xml&ids=CYEG'

    Some other options:
     * format=raw
     * format=json
     * format=xml
     * hours=1.5

    The cgi-bin API URL was deprecated around September 2025, so our v1.1 reflects the change to a new URL. 

    Note: I've notice two bugs (2025-09-25):
     * xml: dewpoint is missing if dewpoint is 00 in the METAR
     * json: gives altimeter setting as hPa for Canadian and North American stations

"""

__version__     = 'v1.1'
__initialdate__ = 'August 2016'
__author__      = 'Darren Paul Griffith <https://madphilosopher.ca/>'


from xml.etree import ElementTree
import requests
import time
import random
import sys


DEBUG         = False
TESTFILE      = "cyeg.xml"
TESTFILE      = "cyeg_cyoj.xml"
degree_symbol = chr(176)
degree_symbol = u"\N{DEGREE SIGN}"

URL = 'https://aviationweather.gov/api/data/metar?format=xml&ids='


def degrees_to_cardinal(degrees):
    """Convert degrees >= 0 to one of 16 cardinal directions."""

    CARDINALS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

    if degrees == "VRB":
        degrees = 0.0
    else:
        degrees = float(degrees)

    if degrees < 0: return None

    i = (degrees + 11.25)/22.5

    return CARDINALS[int(i % 16)]



def fetch_multiple(station_list):
    """Fetch the metars for a list of station IDs."""

    # convert list to space-separated string
    stations = "%2C".join(station_list)
    if DEBUG: print("stations:", stations)

    # fetch the url and parse the xml data
    url = URL + stations
    if DEBUG:
        # print out an equivalent curl command-line
        print(f"curl -s '{url}'")

    tree = None
    if DEBUG:
        f = open(TESTFILE, 'rt')
        tree = ElementTree.parse(f)
    else:
        attempts = 0
        success = False
        while attempts < 3 and not success:
            try:
                rq = requests.get(url, timeout=16.0)
                rq.raise_for_status()
                if rq.status_code == requests.codes.ok:
                    intext = rq.text
                    tree = ElementTree.fromstring(intext)
                success = True
            except:
                attempts = attempts + 1
                time.sleep(random.uniform(3,60))

    # start walking the tree
    out_dict = {}
    for node in tree.findall("./data/METAR"):
        s_metar = {}
        for x in node:
            # store each tag in a dictionary for that station
            s_metar[x.tag] = x.text

        # convert some keys
        if "wind_dir_degrees" in s_metar:
            s_metar["wind_dir_compass"] = degrees_to_cardinal(s_metar["wind_dir_degrees"])
        if "temp_c" in s_metar:
            s_metar["temp_f"] = float(s_metar["temp_c"])*9.0/5.0 + 32.0
        if "wind_speed_kt" in s_metar:
            s_metar["wind_speed_mph"] = float(s_metar["wind_speed_kt"]) * 1.150779
        if "sea_level_pressure_mb" in s_metar:
            s_metar["sea_level_pressure_kpa"] = float(s_metar["sea_level_pressure_mb"]) / 10.0

        # store the entire station metar dictionary in a dictionary
        out_dict[s_metar["station_id"]] = s_metar

    return out_dict


def fetch(station):
    """Fetch the metar for a single station ID."""

    d = fetch_multiple([station])
    return d.get(station) # returns None if d has no such key


def test():
    '''Perform single and multiple station fetch, printing dictionary.'''

    from pprint import pprint
    WIDTH   = 150

    # single fetch
    print("=" * WIDTH)
    d = fetch('CYEG')
    if d: pprint(d, width=WIDTH)
    print()

    # multiple fetch
    print("=" * WIDTH)
    m = fetch_multiple(['CZVL','CYEG'])
    if m: pprint(m, width=WIDTH)
    print()


if __name__ == '__main__':


    if len(sys.argv) == 2:
        station = sys.argv[1].upper()
    else:
        station = "CYEG"

    d = fetch(station)
    if d and DEBUG:
        from pprint import pprint
        print()
        pprint(d, width=150)
        print()

    if d:
        temp_c     = d.get("temp_c")       # will be None if missing
        dewpoint_c = d.get("dewpoint_c")   # will be None if missing

        print(f'Code:               {d["raw_text"]}')
        print(f'Observation:        {d["observation_time"]}')
        print(f'Temperature:        {temp_c}{degree_symbol}C')
        print(f'Dew Point:          {dewpoint_c}{degree_symbol}C')
        print(f'Wind Direction:     {d["wind_dir_compass"]} ({d["wind_dir_degrees"]}{degree_symbol})')
        print(f'Wind Speed:         {d["wind_speed_kt"]} KT')
        if "wind_gust_kt" in d:
            print(f'Wind Gust:         {d["wind_gust_kt"]} KT')
        print(f'Sea Level Pressure: {d["sea_level_pressure_mb"]} hPa')
        print(f'Altimeter Setting:  {d["altim_in_hg"]}')



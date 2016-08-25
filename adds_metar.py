#!/usr/bin/env python
"""Fetches metars from the ADDS Text Data Server.

Documentation: https://aviationweather.gov/dataserver

URL: https://aviationweather.gov/adds/dataserver_current/httpparam?datasource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=1.5&stationString=CYEG

"""

__RCS__ = '$Id$'
__version__ = '$Revision:$'
__initialdate__ = 'August 2016'
__author__ = 'Darren Paul Griffith <http://madphilosopher.ca/>'


from xml.etree import ElementTree
import urllib2


DEBUG = False
TESTFILE = "cyeg.xml"
TESTFILE = "cyeg_cyoj.xml"

URL = 'https://aviationweather.gov/adds/dataserver_current/httpparam?datasource=metars&requestType=retrieve&format=xml&mostRecentForEachStation=constraint&hoursBeforeNow=1.5&stationString='


def degrees_to_cardinal(degrees):
    """Convert degrees >= 0 to one of 16 cardinal directions."""

    CARDINALS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

    degrees = float(degrees)

    if degrees < 0: return None

    i = (degrees + 11.25)/22.5

    return CARDINALS[int(i % 16)]



def fetch_multiple(station_list=list(["CYEG", "CYOJ"])):
    """Fetch the metars for a list of station IDs."""

    # convert list to space-separated string
    stations = "%20".join(station_list)
    if DEBUG: print "stations:", stations

    # fetch the url and parse the xml data
    url = URL + stations
    if DEBUG:
        f = open(TESTFILE, 'rt')
    else:
        f = urllib2.urlopen(url)
    tree = ElementTree.parse(f)

    # start walking the tree
    out_dict = {}
    for node in tree.findall("./data/METAR"):
        s_metar = {}
        for x in node:
            # store each tag in a dictionary for that station
            s_metar[x.tag] = x.text

        # convert some keys
        if s_metar.has_key("wind_dir_degrees"):
            s_metar["wind_dir_compass"] = degrees_to_cardinal(s_metar["wind_dir_degrees"])
        if s_metar.has_key("temp_c"):
            s_metar["temp_f"] = float(s_metar["temp_c"])*9.0/5.0 + 32.0
        if s_metar.has_key("wind_speed_kt"):
            s_metar["wind_speed_mph"] = float(s_metar["wind_speed_kt"]) * 1.150779

        # store the entire station metar dictionary in a dictionary
        out_dict[s_metar["station_id"]] = s_metar

    return out_dict


def fetch(station="CYEG"):
    """Fetch the metar for a single station ID."""

    #station_list = [station]
    #d = fetch_multiple(station_list)
    d = fetch_multiple([station])
    return d[station]




if __name__ == '__main__':

    if DEBUG:
        import pprint
        pprint.pprint(fetch("CYEG"))
        print

    d = fetch("CYEG")
    if d:
        if DEBUG: print
        print "Observation:       ", d["observation_time"]
        print "Code:              ", d["metar_type"], d["raw_text"]
        print "Temperature (C):   ", d["temp_c"]
        print "Dew Point (C):     ", d["dewpoint_c"]
        print "Wind Speed:        ", d["wind_speed_kt"], "KT"
        print "Wind Direction:    ", d["wind_dir_compass"], "(", d["wind_dir_degrees"], ")"
        print "Sea Level Pressure:", d["sea_level_pressure_mb"], "mb"




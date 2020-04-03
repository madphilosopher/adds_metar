# ADDS METAR
This Python 2 module fetches aviation weather METARs from the ADDS Text Data Server.

The [ADDS Text Data Server](https://aviationweather.gov/dataserver) is
a subservice of the Aviation Weather Centre, and provides METAR data
for U.S. stations and global stations (when available) in XML, CSV,
and gzip formats.

The module can simply download the METAR data via one of two methods:
 * ```fetch()```
 * ```fetch_multiple()```

returning the station data as a Python dictionary.


## Motivation

I wrote this module in 2016 when the excellent [pymetar
library](https://github.com/klausman/pymetar) by Tobias Klausmann stopped
working, when the source server ```weather.noaa.gov``` went offline.

The ```adds_metar.py``` module is much simpler in design. It does not
need to decode the METAR since the decoded weather data is included in
the response from the ADDS Text Data Server.


## Features

 * Can fetch single or multiple stations in one ```https``` request
 * Makes three attempts on network errors, with a random timeout interval
 * Derives the following values from the fetched data:
    * Cardinal wind direction (N, NNE, NE, etc.)
    * Temperature in Fahrenheit
    * Wind speed in mph
    * Sea level pressure in kPa


## Example Usage

### Command Line

```sh
$ python adds_metar.py CYEG

Observation:        2020-02-20T18:00:00Z
Code:               METAR CYEG 201800Z 24004KT 20SM BKN220 M07/M15 A2991 RMK CI5 SLP176
Temperature (C):    -7.0
Dew Point (C):      -15.0
Wind Speed:         4 KT
Wind Direction:     WSW ( 240 )
Sea Level Pressure: 1017.6 mb
Sea Level Pressure: 101.76 kPa
```

### Python Module

```python

>>> import adds_metar
>>> from pprint import pprint
>>> pprint(adds_metar.fetch("CYVR"))

{'altim_in_hg': '30.301182',
 'dewpoint_c': '1.0',
 'elevation_m': '2.0',
 'flight_category': 'VFR',
 'latitude': '49.17',
 'longitude': '-123.17',
 'metar_type': 'METAR',
 'observation_time': '2020-02-20T18:00:00Z',
 'raw_text': 'CYVR 201800Z 29005KT 220V300 20SM FEW220 06/01 A3030 RMK CI1 SLP261',
 'sea_level_pressure_kpa': 102.60999999999999,
 'sea_level_pressure_mb': '1026.1',
 'sky_condition': None,
 'station_id': 'CYVR',
 'temp_c': '6.0',
 'temp_f': 42.8,
 'visibility_statute_mi': '20.0',
 'wind_dir_compass': 'WNW',
 'wind_dir_degrees': '290',
 'wind_speed_kt': '5',
 'wind_speed_mph': 5.753895}


>>> pprint(adds_metar.fetch_multiple(["CYYC", "KLAS"]))
{'CYYC': {'altim_in_hg': '29.970472',
          'dewpoint_c': '-11.0',
          'elevation_m': '1084.0',
          'flight_category': 'VFR',
          'latitude': '51.12',
          'longitude': '-114.02',
          'metar_type': 'METAR',
          'observation_time': '2020-02-20T19:00:00Z',
          'raw_text': 'CYYC 201900Z 29010KT 40SM FEW180 07/M11 A2997 RMK AC1 AC TR SLP201',
          'sea_level_pressure_kpa': 102.01,
          'sea_level_pressure_mb': '1020.1',
          'sky_condition': None,
          'station_id': 'CYYC',
          'temp_c': '7.0',
          'temp_f': 44.6,
          'visibility_statute_mi': '40.0',
          'wind_dir_compass': 'WNW',
          'wind_dir_degrees': '290',
          'wind_speed_kt': '10',
          'wind_speed_mph': 11.50779},
 'KLAS': {'altim_in_hg': '30.339567',
          'dewpoint_c': '-12.8',
          'elevation_m': '636.0',
          'flight_category': 'VFR',
          'latitude': '36.07',
          'longitude': '-115.17',
          'metar_type': 'METAR',
          'observation_time': '2020-02-20T18:56:00Z',
          'quality_control_flags': '\n        ',
          'raw_text': 'KLAS 201856Z 01003KT 10SM CLR 13/M13 A3034 RMK AO2 SLP269 T01331128',
          'sea_level_pressure_kpa': 102.69000000000001,
          'sea_level_pressure_mb': '1026.9',
          'sky_condition': None,
          'station_id': 'KLAS',
          'temp_c': '13.3',
          'temp_f': 55.94,
          'visibility_statute_mi': '10.0',
          'wind_dir_compass': 'N',
          'wind_dir_degrees': '10',
          'wind_speed_kt': '3',
          'wind_speed_mph': 3.452337}}

```


## Compatibility

 * Tested under Python 2.7.12, 2.7.17
 * Designed for the ADDS Text Data Server (TDS) ver 1.3




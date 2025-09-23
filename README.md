# ADDS METAR
This Python module fetches aviation weather METARs from the ADDS Text
Data Server (Data API).

The ADDS Text Data Server is
now called the [Data API](https://aviationweather.gov/data/api/),
a subservice of the Aviation Weather Centre, and provides METAR data
for U.S. stations and global stations (when available) in raw, xml,
and json formats.

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
the response from the Data API.


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
$ python3 adds_metar.py CYEG

Code:               METAR CYEG 230400Z 16011KT 20SM SKC 15/01 A2989 RMK SLP130 DENSITY ALT 3000FT
Observation:        2025-09-23T04:00:00.000Z
Temperature:        15°C
Dew Point:          1°C
Wind Direction:     SSE (160°)
Wind Speed:         11 KT
Sea Level Pressure: 1013 hPa
Altimeter Setting:  29.89
```

### Python Module

```python

>>> import adds_metar
>>> from pprint import pprint
>>> pprint(adds_metar.fetch("CYVR"))

{'altim_in_hg': '30.11',
 'dewpoint_c': '11',
 'elevation_m': '2',
 'flight_category': 'VFR',
 'latitude': '49.1830',
 'longitude': '-123.1680',
 'metar_type': 'METAR',
 'observation_time': '2025-09-23T04:00:00.000Z',
 'quality_control_flags': None,
 'raw_text': 'METAR CYVR 230400Z 03004KT 20SM SKC 15/11 A3011 RMK SLP200',
 'sea_level_pressure_kpa': 102.0,
 'sea_level_pressure_mb': '1020',
 'sky_condition': None,
 'station_id': 'CYVR',
 'temp_c': '15',
 'temp_f': 59.0,
 'visibility_statute_mi': '20',
 'wind_dir_compass': 'NNE',
 'wind_dir_degrees': '30',
 'wind_speed_kt': '4',
 'wind_speed_mph': 4.603116}


>>> pprint(adds_metar.fetch_multiple(["CYYC", "KLAS"]))
{'CYYC': {'altim_in_hg': '29.99',
          'dewpoint_c': '2',
          'elevation_m': '1085',
          'flight_category': 'VFR',
          'latitude': '51.1160',
          'longitude': '-114.0110',
          'metar_type': 'METAR',
          'observation_time': '2025-09-23T04:00:00.000Z',
          'quality_control_flags': None,
          'raw_text': 'METAR CYYC 230400Z 21004KT 170V230 15SM FEW230 14/02 A2999 RMK CI1 CI TR SLP167 DENSITY ALT 4300FT',
          'sea_level_pressure_kpa': 101.67,
          'sea_level_pressure_mb': '1016.7',
          'sky_condition': None,
          'station_id': 'CYYC',
          'temp_c': '14',
          'temp_f': 57.2,
          'visibility_statute_mi': '15',
          'wind_dir_compass': 'SSW',
          'wind_dir_degrees': '210',
          'wind_speed_kt': '4',
          'wind_speed_mph': 4.603116},
 'KLAS': {'altim_in_hg': '29.86',
          'dewpoint_c': '6.1',
          'elevation_m': '662',
          'flight_category': 'VFR',
          'latitude': '36.0719',
          'longitude': '-115.1634',
          'metar_type': 'METAR',
          'observation_time': '2025-09-23T03:56:00.000Z',
          'quality_control_flags': None,
          'raw_text': 'METAR KLAS 230356Z 23006KT 10SM FEW220 29/06 A2986 RMK AO2 SLP087 T02890061',
          'sea_level_pressure_kpa': 100.87,
          'sea_level_pressure_mb': '1008.7',
          'sky_condition': None,
          'station_id': 'KLAS',
          'temp_c': '28.9',
          'temp_f': 84.02,
          'visibility_statute_mi': '10+',
          'wind_dir_compass': 'SW',
          'wind_dir_degrees': '230',
          'wind_speed_kt': '6',
          'wind_speed_mph': 6.904674}}

```


## Compatibility

 * Tested under Python 3.9.2, 3.10.12, 3.11.2
 * Designed for the Data API (September 2025)




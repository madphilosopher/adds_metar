#!/usr/bin/env python


def degrees_to_cardinal(degrees):
    """Convert degrees >= 0 to one of 16 cardinal directions."""

    CARDINALS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

    if degrees < 0: return None

    i = (degrees + 11.25)/22.5
    
    return CARDINALS[int(i % 16)]




if __name__ == '__main__':


    for i in range(365):
        print i, degrees_to_cardinal(i)

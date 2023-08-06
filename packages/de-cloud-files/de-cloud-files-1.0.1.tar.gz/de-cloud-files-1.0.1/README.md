League Event Interface
================

Create custom callbacks to various in game events made possible with the League Client API

## Original
Heavily borrows from LeagueOfEvents - [check out the original LeagueOfEvents package here](https://pypi.org/project/LeagueOfEvents/)

## Installing

Install the [PyPI Package](https://pypi.org/project/LeagueEventInterface/):

    pip install LeagueEventInterface

## Examples
Basic example:
```py
import leagueeventinterface

def pentakill_handler():
    print("Yaay! A Penta!")

leagueeventinterface.subscribe("PlayerPentakill", pentakill_handler)
```

# Events
TODO

# calparse

```
usage: calparse [-h] [-u URLS] [-c CACHE] [--cache_timeout CACHE_TIMEOUT] [-i INTERVAL] [-f] mode

Parses iCal URLs in different ways.

positional arguments:
  mode                  supports 'random', 'list'

options:
  -h, --help            show this help message and exit
  -u, --urls URLS       JSON file containing a list of iCal URLs
  -c, --cache CACHE     cache file of calendar state (default $HOME/.cache/calparse-cache.json)
  --cache_timeout CACHE_TIMEOUT
                        length of time the cache is good for (seconds, default: 3600)
  -i, --interval INTERVAL
                        number of seconds in an interval for the 'sequence' mode
  -f, --force           force update of the cache, overriding cache_timeout
```

Here is an example `urls.json` file:

```json
["https://ics.calendarlabs.com/76/b7458267/US_Holidays.ics"]
```

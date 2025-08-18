# calparse

## Command-line usage

```
usage: calparse [-h] [-u URLS] [-c CACHE] [--cache_timeout CACHE_TIMEOUT]
                [-i INTERVAL] [-f] [--version] [-n]
                [mode]

Parses iCal URLs in different ways.

positional arguments:
  mode                  supports 'random', 'list'

options:
  -h, --help            show this help message and exit
  -u, --urls URLS       JSON file containing a list of iCal URLs (default:
                        ./urls.json)
  -c, --cache CACHE     cache file of calendar state (default
                        $HOME/.cache/calparse-cache.json)
  --cache_timeout CACHE_TIMEOUT
                        length of time the cache is good for (seconds,
                        default: 3600)
  -i, --interval INTERVAL
                        number of seconds in an interval for the 'sequence'
                        mode
  -f, --force           force update of the cache, overriding cache_timeout
  --version             print version information (latest git commit hash and
                        date)
  -n, --no-skip         do not skip any events despite not_until_days
                        configuration
```

Here is an example `urls.json` file:

```json
["https://ics.calendarlabs.com/76/b7458267/US_Holidays.ics"]
```

## More functionality

Add a description like the following to a calendar event to ensure calparse does
not display an event until 0 days before it occurs:

```json
{
  "not_until_days": 0
}
```

# Smart FACT crawler

the smartfact crawler acquieres data from the FACT DIM network via the DIM to web bridge [smartfact](http://www.fact-project.org/smartfact/).
Information as DRIVE, SOURCE, and WEATHER are accessable in a python dictonary.
Most numerical values are converted to their propper representation  e.g. float, int, datetime...

Where it makes sense we use a namedtuple of `(value, unit)`

## Usage

```python
>>> import smart_fact_crawler as sfc

>>> print(sfc.camera_climate().humidity_mean)
Quantity(value=24.9, unit='%')
```

# Retries

As of version `0.2.0` the retry logic implemented in `smart_fact_crawler`
was dumped.
This was decided because the necessery retry logic might differ from use case
to use case.

If you need a retry logic, you can wrap the `smart_fact_crawler` functions
with the tools provided by e.g. the `retrying` library:

```
from retrying import retry
from smart_fact_crawler import smartfact

smartfact_with_retry = retry(
  smartfact, stop_max_attempt_number=10, wait_fixed=2000
)
```

This would retry a failed call to smartfact 10 times with a delay
of 2 seconds between tries before actually raising an Exception.

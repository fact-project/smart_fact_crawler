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

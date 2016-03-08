# Smart FACT crawler

the smartfact crawler is a tool to acquiere data from the FACT DIM network via the DIM to web bridge [smartfact](http://www.fact-project.org/smartfact/).
Information as DRIVE, SOURCE, and WEATHER can be retrieved in a python dictonary. Most numerical values are already converted to their propper representation  e.g. float, int, datetime...

## Usage
### The full SmartFact representation in python:

```
#!python
import smart_fact_crawler as sfc
smf = sfc.SmartFact()
smf.drive()
	{
		'Azimuth_in_Deg': -223.0,
		'Control_Deviation_in_ArcSec': 1.28,
 		'Declination_in_Deg': 21.628,
 		'Distance_to_Moon_in_Deg': '&mdash;',
 		'Right_Ascention_in_h': 5.5425,
 		'Source_Name': ['Crab'],
 		'Time_Stamp': datetime.datetime(2015, 9, 25, 6, 2, 25, 756000, tzinfo=<UTC>),
 		'Zenith_Distance_in_Deg': 9.47
 	}
```

### Or one uses the single SmartFact functions directly: 
```
#!python
import smart_fact_crawler as sfc
sfc.drive()
	{
		'Azimuth_in_Deg': -223.0,
		'Control_Deviation_in_ArcSec': 1.28,
 		'Declination_in_Deg': 21.628,
 		'Distance_to_Moon_in_Deg': '&mdash;',
 		'Right_Ascention_in_h': 5.5425,
 		'Source_Name': ['Crab'],
 		'Time_Stamp': datetime.datetime(2015, 9, 25, 6, 2, 25, 756000, tzinfo=<UTC>),
 		'Zenith_Distance_in_Deg': 9.47
 	}
```

or the Sky Quality Meter:
```
#!python
import smart_fact_crawler as sfc
sfc.sqm()
	{
		'Magnitude': 0.0,
	 	'Sensor_Frequency_in_Hz': 546549.0,
	 	'Sensor_Period_in_s': 0.0,
	 	'Sensor_Temperature_in_C': 33.5,
	 	'Time_Stamp': datetime.datetime(2015, 9, 25, 13, 40, 27, 545000, tzinfo=<UTC>)
	 }
```
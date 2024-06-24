# midterm_proj
# Tropical prediction for SLD 45

Hurricane data is heavily researched from the National Weather Service (NWS) and National Hurricane Center (NHC). 

My aim is to provide a focused analysis of hurricane impacts on the Space Coast of Florida since 1851 and the potential impacts in the future. 
Note: For this analysis I am considering the Space Coast as ranging from Palm Bay, Fl to just south of New Smyrna Beach, Fl.

I hope to provide a future probability of impact specifically to the Space Launch Delta 45 (SLD 45) and Kennedy Space Center (KSC).

Even more specifically I would like to predict the likelihood of tropical storms impact to the launch mission. 

If possible I will explore what options our leaders have to mitigate impacts to the mission. 

# Thoughts
If we can determine the most likely months of impact and probabilities of storms occuring could we better prepare? Could we adjust launch wind speed constraints?

Need to show that impacts from tropical storms is not only a direct hit, but also the proximity to a storm. 

# Questions to answer in the data
-Overall, what is the trend of number of Atlantic hurricanes or tropical storms over time?
-How many hurricanes and/or tropical storms hit the Space Coast over time?
-What months are most likely? Maybe a histogram examining this.
-Has the strength of tropical storms increased over time? Intensity and development rate.
-For this analysis how do we categorize impacts? Daily life, launch constraints, safety constraints. 
-Can we predict the likelihood of tropical storm impacts to the Space Coast specifically in the future?
-Is storm surge something we need to worry about? If so, what areas are most likely to be impacted? 

# Possible questions to explore
-Why has the trend in number of hurricanes been increasing?
-Should there be a concern for erosion caused by tropical storms. 
-What can we do to mitigate impacts to the mission? Is there anything?
-Does El Nino or La Nina have a correlation with storms?
-Can trajectory of launch aid in mitigation?

# What data sources will be used?
1. 
Atlantic hurricane database (HURDAT2) 1851-2023 
hurdat2_1851_2023.txt
https://www.nhc.noaa.gov/data/
This dataset (known as Atlantic HURDAT2) has a comma-delimited, text format with six-hourly information on the location, maximum winds, central pressure, and (beginning in 2004) size of all known tropical cyclones and subtropical cyclones.
HURDAT Reference
Landsea, C. W. and J. L. Franklin, 2013: Atlantic Hurricane Database Uncertainty and Presentation of a New Database Format. Mon. Wea. Rev., 141, 3576-3592.

This is a detailed description of [hurdat2](https://www.aoml.noaa.gov/hrd/hurdat/hurdat2-format.pdf)

2. GIS view of historical tracks
https://coast.noaa.gov/hurricanes/#map=7.17/28.131/-80.257&search=eyJzZWFyY2hTdHJpbmciOiJDYXBlIENhbmF2ZXJhbCwgQnJldmFyZCBDb3VudHksIEZsb3JpZGEsIDMyOTIwLCBVU0EiLCJzZWFyY2hUeXBlIjoiZ2VvY29kZWQiLCJvc21JRCI6IjEyMTY2MTAiLCJjYXRlZ29yaWVzIjpbIkg1IiwiSDQiLCJIMyIsIkgyIiwiSDEiLCJUUyIsIlREIiwiRVQiXSwieWVhcnMiOltdLCJtb250aHMiOltdLCJlbnNvIjpbXSwicHJlc3N1cmUiOnsicmFuZ2UiOlswLDEwMzBdLCJpbmNsdWRlVW5rbm93blByZXNzdXJlIjp0cnVlfSwiYnVmZmVyIjo2MCwiYnVmZmVyVW5pdCI6WyJOYXV0aWNhbCBNaWxlcyJdLCJzb3J0U2VsZWN0aW9uIjp7InZhbHVlIjoieWVhcnNfbmV3ZXN0IiwibGFiZWwiOiJZZWFyIChOZXdlc3QpIn0sImFwcGx5VG9BT0kiOnRydWUsImJhc2VtYXAiOiJzYXRlbGxpdGUiLCJpc1N0b3JtTGFiZWxzVmlzaWJsZSI6dHJ1ZX0=

This is the source of the raw data. https://coast.noaa.gov/digitalcoast/data/

## Notes

- Storm surge was difficult to explain due to lack of reliable data. 
- Tried breaking down the amount of storms per day/week in the months. Was not that helpful to the overall message. 
- 

## LEGEND
- TD - Tropical Cyclone <34kt intensity
- TS - Tropical Cyclone 34-63kt intensity
- HU - Hurricane >64kt intensity
- EX - Extratropical cyclone of any intensity
- SD - Subtropical cyclone <34kt intensity
- SS - Subtropical cyclone >34kt intensity
- LO - A low pressure system not tropical
- WV - Tropical wave of any intensity
- DB - Disturbance of any intensity
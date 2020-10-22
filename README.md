# Covid_MIPT research of COVID-19 pandemic throughout the World

main.py -- file with parser to extract information from <a href="https://www.worldometers.info/coronavirus/"> Worldometer: </a>

* Example of parsed data about coronavirus in Russia:
```python
python3 main.py russia
```
* Example of parsed data about coronavirus in states of the USA:
```python
python3 main.py usa_states
```
Data -- folder that includes parsed data about coronavirus pandemic in different countries.

Russia_regions (in Data folder) -- folder that includes parsed data about coronavirus in russian regions.

covid_stringency_index -- index measuring the stringency of different governments in dealing with pandemic, from 0 (no measures taken) to 100 (most severe restriction imposed). Proposed by Oxford Covid-19 Government Response Tracker. You can find more information about it <a href="https://github.com/OxCGRT/covid-policy-tracker/blob/master/documentation/index_methodology.md"> here. </a>

population_dict.py -- python dictionary, containing population of different countries.

all_restrictions -- folder with information about restrictions in different countries: 0 - no restrictions, 1 - some restriction are imposed (measures aimimg at protecting vulnerable groups of citizens, etc.), 3 - complete lockdown.

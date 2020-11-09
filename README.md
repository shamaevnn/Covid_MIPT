# Covid_MIPT research of COVID-19 pandemic throughout the World

<b> main.py </b> -- file with parser to extract information from <a href="https://www.worldometers.info/coronavirus/"> Worldometer: </a>

* Example of parsing data about coronavirus in Russia:
```python
python3 main.py russia
```
* Example of parsing data about coronavirus in USA by states:
```python
python3 main.py usa_states
```
<b> Data </b> -- folder that includes parsed data about coronavirus pandemic in different countries.

<b> Russia_regions </b> (in Data folder) -- folder that includes parsed data about coronavirus in russian regions.

<b> all_restrictions </b> -- folder containing information about stringency index of different countries while dealing with covid pandemic. Index vary from 0 (no measures taken) to 100 (most severe restriction imposed). Proposed by Oxford Covid-19 Government Response Tracker. You can find more information about it <a href="https://github.com/OxCGRT/covid-policy-tracker/blob/master/documentation/index_methodology.md"> here. </a> 

<b> population_dict.py </b> -- python dictionary containing population of different countries.

<b> SIR.ipynb </b> -- prototype of SIR (Susceptible, Infectious, Recovered) model.

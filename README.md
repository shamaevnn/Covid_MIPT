# Covid MIPT research of COVID-19 pandemic throughout the World

<b> parser.py </b> -- file with parser to extract information from <a href="https://www.worldometers.info/coronavirus/"> Worldometer: </a>

* Example of parsing data about coronavirus in Russia:
```python
python3 parser.py russia
```
* Example of parsing data about coronavirus in USA by states:
```python
python3 parser.py usa_states
```
<b> Data </b> -- folder that includes parsed data about coronavirus pandemic in different countries.

<b> Russia_regions </b> (in Data folder) -- folder that includes parsed data about coronavirus in russian regions.

<b> all_restrictions </b> -- folder containing information about stringency index of different countries while dealing with covid pandemic. Index vary from 0 (no measures taken) to 100 (most severe restriction imposed). Proposed by Oxford Covid-19 Government Response Tracker. You can find more information about it <a href="https://github.com/OxCGRT/covid-policy-tracker/blob/master/documentation/index_methodology.md"> here. </a> 

<b> population_dict.py </b> -- python dictionary containing population of different countries.

<b> SIR.py </b> -- script which predicts data according to SIR model (Suspected, Infectious, Recovered) and puts results to SIR folder.

* Example of using SIR.py:
```python
python3 SIR.py --countries germany
python3 SIR.py --countries germany,austria
```
<b> SIR </b> -- folder which contains results of SIR.py model.

<b> benfords_law </b> -- script which validates data about number of infected people and total number of coronavirus cases in different countries using Benford's law model, puts the results into Benfords_law folder.

* Example of using benfords_law.py:
```python
python3 benfords_law.py --countries germany
python3 benfords_law.py --countries germany,austria
```

<b> Benfords_law </b> -- folder which contains results of benfords_law.py model.

<b> pearson_test.py </b> -- script which validates factual and predicted data about number of infected and recovered people in different countries using chi-square (χ2) test, puts the results into Pearson folder.

* Example of using pearson_test.py:
```python
python3 pearson_test.py --countries germany
python3 pearson_test.py --countries germany,austria
```

<b> Pearson </b> -- folder which contains results of pearson_test.py script.

<b> Spearman_corr.py </b> -- script which calculates Spearman's rank correlation coefficient, the sign of the Spearman correlation indicates the direction of association between variables.

* Example of using Spearman_corr.py:
```python
python3 Spearman_corr.py --countries germany
python3 Spearman_corr.py --countries germany,austria
```

<b> Spearman </b> -- folder which contains results of Spearman_corr.py script.

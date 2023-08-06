# Pandas DataFrame to nested dict

```python

# from: https://stackoverflow.com/a/74810722/15096247

$pip install a-pandas-ex-to-dict

from a_pandas_ex_to_dict import pd_add_df_to_nested_dict
import pandas as pd
from pprint import pprint

pd_add_df_to_nested_dict()

df = pd.read_csv("https://github.com/pandas-dev/pandas/raw/main/doc/data/titanic.csv")
df = df[:10]
dfdict2 = df.d_to_nested_dict(["Survived", "Pclass", "Embarked", "Fare", "Cabin"])
dfdict = df.d_to_nested_dict()
pprint(dfdict2)
pprint(dfdict)


{0: {1: {'S': {51.8625: {'E46': 1}}},
     3: {'Q': {8.4583: {}}, 'S': {7.25: {}, 8.05: {}, 21.075: {}}}},
 1: {1: {'C': {71.2833: {'C85': 1}}, 'S': {53.1: {'C123': 1}}},
     2: {'C': {30.0708: {}}},
     3: {'S': {7.925: {}, 11.1333: {}}}}}
{1: {0: {3: {'Braund, Mr. Owen Harris': {'male': {22.0: {1: {0: {'A/5 21171': {7.25: 1}}}}}}}}},
 2: {1: {1: {'Cumings, Mrs. John Bradley (Florence Briggs Thayer)': {'female': {38.0: {1: {0: {'PC 17599': {71.2833: 1}}}}}}}}},
 3: {1: {3: {'Heikkinen, Miss. Laina': {'female': {26.0: {0: {0: {'STON/O2. 3101282': {7.925: 1}}}}}}}}},
 4: {1: {1: {'Futrelle, Mrs. Jacques Heath (Lily May Peel)': {'female': {35.0: {1: {0: {'113803': {53.1: 1}}}}}}}}},
 5: {0: {3: {'Allen, Mr. William Henry': {'male': {35.0: {0: {0: {'373450': {8.05: 1}}}}}}}}},
 6: {0: {3: {'Moran, Mr. James': {'male': {}}}}},
 7: {0: {1: {'McCarthy, Mr. Timothy J': {'male': {54.0: {0: {0: {'17463': {51.8625: 1}}}}}}}}},
 8: {0: {3: {'Palsson, Master. Gosta Leonard': {'male': {2.0: {3: {1: {'349909': {21.075: 1}}}}}}}}},
 9: {1: {3: {'Johnson, Mrs. Oscar W (Elisabeth Vilhelmina Berg)': {'female': {27.0: {0: {2: {'347742': {11.1333: 1}}}}}}}}},
 10: {1: {2: {'Nasser, Mrs. Nicholas (Adele Achem)': {'female': {14.0: {1: {0: {'237736': {30.0708: 1}}}}}}}}}}
```

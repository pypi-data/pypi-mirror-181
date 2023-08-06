# Pandas DataFrame to dict with crosstab DataFrames 

```python

$pip install a-pandas-ex-crosstab-dict

from a_pandas_ex_crosstab_dict import pd_add_crosstab_dict
import pandas as pd
pd_add_crosstab_dict()
df = pd.read_csv(
    "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv"
)
df.ds_get_crosstab_dict(maincolumn="Cabin", columns=None)
df.ds_get_crosstab_dict( maincolumn="Cabin", columns=["Survived", "Sex",'Fare'])
Out[5]: 
{'Survived': Cabin     A10  A14  A16  A19  A20  A23  A24  ...  F G73  F2  F33  F38  F4  G6  T
 Survived                                     ...                                
 0           1    1    0    1    0    0    1  ...      2   1    0    1   0   2  1
 1           0    0    1    0    1    1    0  ...      0   2    3    0   2   2  0
 
 [2 rows x 147 columns],
 'Sex': Cabin   A10  A14  A16  A19  A20  A23  A24  ...  F G73  F2  F33  F38  F4  G6  T
 Sex                                        ...                                
 female    0    0    1    0    0    0    0  ...      0   0    3    0   1   4  0
 male      1    1    0    1    1    1    1  ...      2   3    0    1   1   0  1
 
 [2 rows x 147 columns],
 'Fare': Cabin     A10  A14  A16  A19  A20  A23  A24  ...  F G73  F2  F33  F38  F4  G6  T
 Fare                                         ...                                
 0.0000      0    0    0    0    0    0    0  ...      0   0    0    0   0   0  0
 5.0000      0    0    0    0    0    0    0  ...      0   0    0    0   0   0  0
 7.6500      0    0    0    0    0    0    0  ...      2   0    0    0   0   0  0
 7.7500      0    0    0    0    0    0    0  ...      0   0    0    1   0   0  0

```

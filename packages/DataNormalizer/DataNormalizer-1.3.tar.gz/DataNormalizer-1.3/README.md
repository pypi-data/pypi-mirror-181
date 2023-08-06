# General Information
The DataNormalizer package is made to help data scientists with validating and normalising data that they are going to import. Right now the library is able to validate columns and check datasets based on a set of rules like custom data types. 
 
```python
import DataNormalizer
```

### Setting variables
The DataNormalizer library might need the details of the target app. These setting are set through properties.
```python
Clappform.Auth(baseURL="https://dev.clappform.com/", username="user@email.com", password="password")
Normalise = DataNormalizer.Normalise()
Normalise.app_data = Clappform.App("appname").ReadOne(extended=True)
Normalise.dataframe = pandas.read_excel("../data.xlsx")
Normalise.rules = json.load(open('../rules.json'))
```

### checkRules
Function that will check the custom rules against your dataframe. Requires dataframe and rules. Returns a dataframe
```python
Normalise = DataNormalizer.Normalise()
Normalise.dataframe = pandas.read_excel("../data.xlsx")
Normalise.rules = json.load(open('../rules.json'))
result = Normalise.checkRules()
```
Rules are added in a JSON file. Every column has its own rule, however rules without a column name are seen as global rules. 
```json
[
{
    "reset_coverage":"True",
    "action": "np.nan",
    "verbose": "to_file"
},
{ 
    "column": "city",
    "check_coverage": "10",
    "selection": [ "Aa en Hunze", "Aalsmeer", "Aalten", "Achtkarspelen"]
},
{
    "column": "postalCode",
    "type": "postal_code"
}
]
```
Supported keys are
| keys                | value                                                       | explanation                                                                          | Global      |
| ------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------- |
| verbose             | to_file / silent...                                         | How do you want to be notified of errors?                                            | Yes         |
| column              | gemeente                                                    | On which column does this rule apply                                                 | No          |
| type                | postal_code / int / string...                               | What should the values of this column be                                             | No          |
| action              | np-nan                                                      | What to do with the value if incorrect                                               | Yes         |
| selection           | [ "Aa en Hunze", "Aalsmeer", "Aalten"]                      | The values must be one of these values                                               | No          |
| one_hot_encoding    | "prefix" or "" with no prefix                               | Concat pandas dummies on the dataframe                                               | No          |
| concat              | {"name": "uniqueID", "columns": ["col1", "col2"]}           | Concatenate columns together (for unique ID generation)                              | Only Global |
| operator            | {"name": "divide", "columns": ["A", "B"], "type": "divide"} | Apply operator on two columns, result to new column                                  | Only Global |
| drop_duplicates     | ["col1", "col2"]                                            | Drop duplicates based on a subset of column values                                   | Only Global |
| shared_colname_drop | "anything"                                                  | If multiple shared column names, keep one                                            | Only Global |
| timestamp           | "%Y-%m-%d"                                                  | Map values to a datetime object, skip rule immediatly if one value fails             | No          |
| range_time          | ["2017-12-01 00:00:00", "2012-12-01 00:00:00"]              | Converts data to timestamp and checks range, combining with timestamp improves speed | No          |
| fillna              | value                                                       | Fill every NaN value to a key                                                        | Yes         |
| range               | ["-inf", 2010] / [2010, "inf"]                              | Number range, left <= value >= right                                                 | No          |
| mapping             | {"bad": "0","moderate": "1"}                                | Map row values to something else                                                     | yes         |
| column_mapping      | {"postcode": "postal_code","stad": "city"}                  | Map column values to something else                                                  | Yes         |
| regex               | [1-9][0-9]?$^100$                                           | Column value should look like this regex                                             | No          |
| check_coverage      | 50                                                          | Take a smaller sample of the column, in percentage                                   | Yes         |
| reset_coverage      | True / False                                                | If an error is found in the sample, fall back to 100%                                | Yes         |

Supported values for types
| type                 | explanation                                                                           |
| -------------------- | ------------------------------------------------------------------------------------- |
| int                  | accepts ints and floats get decimal removed                                           |
| positive-int         | same as int but only positive and zero                                                |
| negative-int         | same as int but only negative                                                         |
| string               | characters accepted                                                                   |
| float                | decimal numbers accepted                                                              |
| boolean              | makes lowercase and accepts true / false                                              |
| postal_code          | accepts 1111AB format. Removes special chars then makes string uppercase              |
| street               | Accepts letters, spaces and '. Makes first character and characters after ' uppercase |
| latitude / longitude | accepts 32.111111 format                                                              |
| letters              | only accepts letters                                                                  |

Operator options
| operator | explanation                                                    |
| -------- | -------------------------------------------------------------- |
| divide   | Divide two columns on row level and put result to new column   |
| multiply | Multiply two columns on row level and put result to new column |

Fillna options
| action         | explanation                                               | value                       |
| -------------- | --------------------------------------------------------- | --------------------------- |
| fillna         | Fill NaN value with something else                        | Some thing to fill NaN with |
| fillna_diffcol | Fill NaN with the value of a different column on that row | Other column name           |
| fillna_mean    | Fill NaN with mean of column                              | Doesn't matter              |
| fillna_median  | Fill NaN with median of column                            | Doesn't matter              |

Supported values for action
| action | explanation                     |
| ------ | ------------------------------- |
| np.nan | Replaces mismatches with np.nan |
| drop   | Drop the row                    |

Supported values for verbose
| action     | explanation                                        |
| ---------- | -------------------------------------------------- |
| to_console | (DEFAULT) Print errors to console                  |
| to_file    | Print errors to a file with a timestamp.txt format |
| silent     | Dont print                                         |

### obtainKeys
Function that will find keys needed for the app, needs app_data. Returns keys
```python
Normalise = DataNormalizer.Normalise()
Normalise.app_data = Clappform.App("appname").ReadOne(extended=True)
Normalise.obtainKeys()
```

### matchKeys
Function that will find missing keys, needs app_data and dataframe. Returns missing and additional keys
```python
Normalise = DataNormalizer.Normalise()
Normalise.app_data = Clappform.App("appname").ReadOne(extended=True)
Normalise.dataframe = pandas.read_excel("../data.xlsx")
Normalise.matchKeys()
```

### fixMismatch
Function that will suggest changes to your dataset based on missing keys, needs app_data and dataframe. Lowering the strictness will increase the amount of matches with possible keys. Needs app_data and dataframe. Interaction via terminal.
```python
Normalise = DataNormalizer.Normalise()
Normalise.app_data = Clappform.App("appname").ReadOne(extended=True)
Normalise.dataframe = pandas.read_excel("../data.xlsx")
Normalise.fixMismatch(strictness = 0.8)
```
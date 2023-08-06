# normscaler

This is a package for data normalization using *MinMaxScaler*, *MaxAbsScaler*, *RobustScaler*, *StandardScaler* and *Normalizer* in Scikit-learning, and *DecimalScaler*. This package will not normalize the one-hot encoded string, dummy or categorical features because their values are in the range of [0,1].

This package uses dataset in Pandas DataFrame. 

Developed by Shouke Wei from Deepsim Academy, Deepsim Intelligence Technology Inc. (c) 2022

## Install the package
```python
pip install normscaler
```

## An example
In this example, there are encoded categorical features, and package can automatically skip them.

### (1) import required packages
```python
import pandas as pd
from sklearn.model_selection import train_test_split
```

### (2) read data
This is a socio-economic dataset of the first five top GDP ranking provinces in China.
```python
url = 'https://raw.githubusercontent.com/shoukewei/data/main/data-pydm/gdp_china_encoded.csv'
df = pd.read_csv(url)
df
```
### (3) slice data into features and target
GDP is the target and others are features.
```python
X = df.drop(['gdp'],axis=1)
y = df['gdp']
```
### (4) split dataset for training and testing
```python
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.30, random_state=1)
```

### (5) normalize train and test features using one scaler
- MinMaxScaler
- MaxAbsScaler
- RobustScaler
- StandardScaler
- Normalizer
- DecimalScaler  

For example, use decimal scaling method, i.e. DecimalScaler
```python
from normascaler.scaler import DecimalScaler
```
Normalize the train features and test features
```python
X_train_scaled, X_train_scaled = DecimalScaler(X_train, X-test)
```
Display the normalized X_train data in Pandas DataFrame
```python
X_train_scaled
```
Display the normalized X_test data in Pandas DataFrame
```python
X_test_scaled
```
## License
https://opensource.org/licenses/MIT

## PyPI page: 
https://pypi.org/project/normcaler


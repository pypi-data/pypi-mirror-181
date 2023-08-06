"""
Different data nomarlization scalers:
- MinMaxScaler
- MaxAbsScaler
- RobustScaler
- StandardScaler
- Normalizer
- DecimalScaler

Constructor method.
    Parameters
    ----------

    X_train: Pandas DataFrame dataset for train
    X_test: Pandas DataFrame dataset for test
"""

import pandas as pd
from sklearn import preprocessing

# MinMaxScaler
def MinMaxScaler(X_train,X_test): 
    
    for x in X_train:
        max = X_train[x].max()    
        if abs(max) <= 1:
            pass
        else:
            min_max_scaler = preprocessing.MinMaxScaler().fit(X_train)
            X_train_scaled = min_max_scaler.transform(X_train)
            X_test_scaled = min_max_scaler.transform(X_test)
            X_train_scaled = pd.DataFrame(X_train_scaled,index=X_train.index,
                                        columns=X_train.columns)
            X_test_scaled = pd.DataFrame(X_test_scaled,index=X_test.index,
                                        columns=X_test.columns)
    
    return X_train_scaled, X_test_scaled

# MaxAbsScaler
def MaxAbsScaler(X_train,X_test): 
    
    for x in X_train:
        max = X_train[x].max()    
        if abs(max) <= 1:
            pass
        else:
            max_abs_scaler = preprocessing.MaxAbsScaler().fit(X_train)
            X_train_scaled = max_abs_scaler.transform(X_train)
            X_test_scaled = max_abs_scaler.transform(X_test)
            X_train_scaled = pd.DataFrame(X_train_scaled,index=X_train.index,
                                        columns=X_train.columns)
            X_test_scaled = pd.DataFrame(X_test_scaled,index=X_test.index,
                                        columns=X_test.columns)
    
    return X_train_scaled, X_test_scaled

# RobustScaler
def RobustScaler(X_train,X_test): 
    
    for x in X_train:
        max = X_train[x].max()    
        if abs(max) <= 1:
            pass
        else:
            robust_scaler = preprocessing.RobustScaler().fit(X_train)
            X_train_scaled = robust_scaler.transform(X_train)
            X_test_scaled = robust_scaler.transform(X_test)
            X_train_scaled = pd.DataFrame(X_train_scaled,index=X_train.index,
                                        columns=X_train.columns)
            X_test_scaled = pd.DataFrame(X_test_scaled,index=X_test.index,
                                        columns=X_test.columns)
    
    return X_train_scaled, X_test_scaled

# StandardScaler
def StandardScaler(X_train,X_test): 
    
    dum = [x for x in X_train.columns if max(abs(X_train[x]))<=1]
    X_train_drop = X_train.drop(dum, axis=1)
    X_test_drop = X_test.drop(dum, axis=1)
    
    standard_scaler = preprocessing.StandardScaler().fit(X_train_drop)
    X_train_scaled = standard_scaler.transform(X_train_drop)
    X_test_scaled = standard_scaler.transform(X_test_drop)
    
    X_train_scaled = pd.DataFrame(X_train_scaled,index=X_train_drop.index,
                                        columns=X_train_drop.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled,index=X_test_drop.index,
                                        columns=X_test_drop.columns)
    X_train_scaled = X_train_scaled.join(X_train[dum])
    X_test_scaled = X_test_scaled.join(X_test[dum])
                              
    return X_train_scaled, X_test_scaled

# Normalizer
def Normalizer(X_train,X_test): 
    
    dum = [x for x in X_train.columns if max(abs(X_train[x]))<=1]
    X_train_drop = X_train.drop(dum, axis=1)
    X_test_drop = X_test.drop(dum, axis=1)
    
    normalizer_scaler = preprocessing.Normalizer().fit(X_train_drop)
    X_train_scaled = normalizer_scaler.transform(X_train_drop)
    X_test_scaled = normalizer_scaler.transform(X_test_drop)
    
    X_train_scaled = pd.DataFrame(X_train_scaled,index=X_train_drop.index,
                                        columns=X_train_drop.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled,index=X_test_drop.index,
                                        columns=X_test_drop.columns)
    X_train_scaled = X_train_scaled.join(X_train[dum])
    X_test_scaled = X_test_scaled.join(X_test[dum])
                              
    return X_train_scaled, X_test_scaled

# DecimalScaler
def DecimalScaler(X_train,X_test): 
    X_train_scaled = X_train.copy()  
    X_test_scaled = X_test.copy() 
    
    for x in X_train:
        max = X_train[x].max()
        max_int = int(max)
        j = len(str(abs(max_int)))
            
        if abs(max) <= 1:
            pass
        else:
            X_train_scaled[x] = X_train[x]/10**j 
            X_test_scaled[x] = X_test[x]/10**j
    return X_train_scaled, X_test_scaled
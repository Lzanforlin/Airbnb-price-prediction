import pandas as pd
import numpy as np


def corrigir_monetario(df, name='name'):
    """
    Correção de valores float incorretos 1.0 para 1000.0
    df = Dataframe
    name= Nome da variável    
    """
    
    filter_1 = df.loc[(df[name] < 10.0), :].index   
    df['New_name'] = df.iloc[filter_1][name] * 1000    
    value = df[name]    
    df['New_name'] = df['New_name'].fillna(value)
    df = df.drop(name, axis=1)
    df.rename(columns = {'New_name': name}, inplace=True)
    return df

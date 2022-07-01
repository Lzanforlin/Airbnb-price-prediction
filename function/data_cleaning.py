import pandas as pd
import numpy as np


def create_dummies(df):
    """
    Create dummies from Plus and Superhost columns
    df = DataFrame from airbnb scrapping
    Return DataFrame with dummies columns and dropped the originals
    """ 
    # Dummies das colunas Plus
    plus1 = df['Plus 1'].unique()
    plus2 = df['Plus 2'].unique()
    plus3 = df['Plus 3'].unique()
    plus4 = df['Plus 3'].unique()
    fullplus = plus1.tolist() + plus2.tolist() + plus3.tolist() + plus4.tolist()
    fullplus = set(fullplus)
    def word_in_columns(df, word):
        if word in df['Plus 1'] or word in df['Plus 2'] or word in df['Plus 3'] or word in df['Plus 4']:
            return 1
        else:
            return 0
        
    count = 0
    for word in fullplus:
        df[f'{word}'] = df.apply(word_in_columns, axis=1, args= (word, ))
        count += 1
    
    # Dummies para Superhost
    Superhost = df['Superhost'].unique()
    def host_in_columns(df, word):
        if word in df['Superhost']:
            return 1
        else:
            return 0
        
    count = 0
    for word in Superhost:
        df[f'{word}'] = df.apply(word_in_columns, axis=1, args= (word, ))
        count += 1
    
    #Drop das colunas 
    df = df.drop(columns=['Plus 1' , 'Plus 2', 'Plus 3', 'Plus 4', 'Superhost'])
    
    return df

       
def quartos_transformation(df):
    """
    df = dataframe to be rooms transformed
    """
    df['Número Quartos'].replace({'Estúdio': '1'}, inplace=True)      
    return df


def banheiro_transformation(df):
    """
    Extract any word inside Número de banheiros column and create a new one called Banheiro Compartilhado.
    In banheiro Compartilhado: If True, There is Banheiro compartilhado. If False, There is no Banheiro compartilhado.
    df = raw dataset cleanned from airbnb scrapping
    """
    df['Banheiro Compartilhado'] = df['Número Banheiros'].str.contains('\\ ', regex=True)

    # Pega o primeiro digito numérico
    df['Número Banheiros'] = df['Número Banheiros'].str[0:1]
    df['Número Banheiros'] = df['Número Banheiros'].str.strip()  
    return df


def ajuste_tipos(df):
    """
    Types transformation
    df= dataset
    """
    # Object to Numeric
    df['Número Quartos'] = pd.to_numeric(df['Número Quartos'], errors = 'coerce')
    df['Número Banheiros'] = pd.to_numeric(df['Número Banheiros'], errors = 'coerce')
    # To DateTime
    df['Check-In'] = pd.to_datetime(df['Check-In'], format ='%Y-%m-%d')
    df['Check-Out'] = pd.to_datetime(df['Check-Out'], format ='%Y-%m-%d')    
    return df


def drop_variables(df):
    df = df.drop({'Unnamed: 0', 'titulo_2'}, axis= 1)
    return df



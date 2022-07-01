import pandas as pd
import numpy as np

    
def create_vista(df):
    """
    Create variable called Vista
    df= Dataframe
    """
    df['Vista'] = df['Vista para as águas'] + df['Vista para o mar']
    return df


def tranform_frequency(df, variables='Localização'):
    """
    Transform categorical variable into frequency
    df = dataset
    variable = name of vaviable to be transformed
    """
    from feature_engine.categorical_encoders import CountFrequencyCategoricalEncoder
    cfce = CountFrequencyCategoricalEncoder(encoding_method='frequency', variables=[variables])
    df = cfce.fit_transform(df)    
    return df


def eng_create_demand(df):
    """
    Create new a column called Demanda from maximum localization
    df= dataset
    """
    df['Demanda'] = df['Localização']
    df['Demanda'] = [1 if i == df['Localização'].max() else 0 for i in df['Demanda']]
    return df


def eng_create_is_holiday(df , df_feriados = pd.read_csv('../data/feriados_nacionais_2021.csv', sep=';')):
    """
    Create new column called É feriado.
    df = Dataframe
    df_feriados = Dafaframe contendo uma lista de feriados nacionais

    """
    #import da tabela feriado
    df_feriados = df_feriados.drop('evento', axis=1)
    df_feriados.replace({'feriado nacional' : '1', 'ponto facultativo': '1'}, inplace=True)
    df_feriados.rename(columns={'status': 'É_feriado'}, inplace=True)
    df_feriados.rename(columns={'data': 'Check-In' }, inplace=True)
    df_feriados['Check-In'] = pd.to_datetime(df_feriados['Check-In'], format ='%Y-%m-%d')

    # Vamos juntar as duas tabelas Preço Médio e Feriados
    df = df.merge(df_feriados, left_on='Check-In', right_on='Check-In', how='left')

    #preenche os nulos com 0
    df = df.fillna(0)   
    return df


def create_taxa(df):
    """
    Create a feature called taxa from Preço com taxas.
    """
    df['Diária com taxas'] = df['Preço com taxas'] / 2
    df['Taxa'] = df['Diária com taxas'] - df['Preço/Noite']
    # Tratando Valores Negativos
    df['Taxa'] = df['Taxa'].mask(df['Taxa'].lt(0)).ffill().fillna(0).convert_dtypes()
    return df


def eng_is_outlier(df, n_neighbors=11 ):
    """
    Create column is outlier from DBSCAM model
    df = DataFrame
    n_neighbors = default is 11
    """
    #libs
    from feature_engine.categorical_encoders import CountFrequencyCategoricalEncoder
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.cluster import DBSCAN
    from sklearn.neighbors import NearestNeighbors
    from kneed import KneeLocator

    X = df.drop({'ID', 'Check-In', 'Check-Out'}, axis=1)
    
    cfce = CountFrequencyCategoricalEncoder(encoding_method='frequency', variables=['É_feriado'])
    pipe = Pipeline(steps=[('scaler', MinMaxScaler())])

    X = cfce.fit_transform(X)
    X = pipe.fit_transform(X)

    nearest_neighbors = NearestNeighbors(n_neighbors=11)
    neighbors = nearest_neighbors.fit(X)

    distances, indices = neighbors.kneighbors(X)
    distances = np.sort(distances[:,10], axis=0)

    i = np.arange(len(distances))
    knee = KneeLocator(i, distances, S=1, curve='convex', direction='increasing', interp_method='polynomial')

    db = DBSCAN(eps=distances[knee.knee], min_samples=11).fit(X)
    labels = db.labels_

    df['É outilier'] = labels   
    return df


def create_dates(df, date='Check-In'):
    """
    Split date into year, month, day and day of year
    df = DataFrame
    date = put date column. Default is 'Check-In'

    In week, Monday is 0 and Sunday is 6. 
    """
    df['Mes'] = df[date].dt.month
    df['Dia'] = df[date].dt.day
    df['Semana_do_ano'] = df[date].dt.week   
    return df


def eng_create_holiday_week(df , df_feriados = pd.read_csv('../data/feriados_nacionais_2021.csv', sep=';')):
    """
    Create new column called Semana de feriado.
    df = Dataframe
    df_feriados = Dafaframe contendo uma lista de feriados nacionais

    """
    #import da tabela feriado
    df_feriados = df_feriados.drop({'evento', 'status'}, axis=1)
    df_feriados.rename(columns={'data': 'Check-In' }, inplace=True)
    df_feriados['Check-In'] = pd.to_datetime(df_feriados['Check-In'], format ='%Y-%m-%d')
    df_feriados['Semana de Feriado'] = df_feriados['Check-In'].dt.week

    # Vamos juntar as duas tabelas Preço Médio e Feriados
    df = df.merge(df_feriados, left_on='Check-In', right_on='Check-In', how='left')
    #preenche os nulos com 0
    df = df.fillna(int(0))   
    return df
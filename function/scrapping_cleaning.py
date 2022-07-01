import pandas as pd
import numpy as np

def first_cleaness (dataset):
    """
    Funccion of first cleanness
    dataset: Name of dataframe extracted from AirBnb's scraping
    """
    #drop da coluna unnamed
    dataset.drop(['Unnamed: 0'], axis=1, inplace=True)
    
    #rename columns:
    dataset = dataset.rename(columns={'id': 'ID', 
                                      'check-in': 'Check-In', 
                                      'check-out': 'Check-Out',
                                       'titulo': 'Localização', 
                                      'atributo_1': 'Número Hóspedes',
                                       'atributo_2': 'Número Quartos', 
                                      'atributo_3': 'Número Camas',
                                       'atributo_4': 'Número Banheiros', 
                                      'atributo_5':'Plus 1',
                                      'atributo_6':'Plus 2',
                                       'atributo_7':'Plus 3',
                                      'atributo_8':'Plus 4', 
                                      'avaliação':'Avaliação',
                                        'comentários': 'Número Comentários', 
                                      'preço': 'Preço/Noite',
                                      'preço_total': 'Preço com taxas',
                                       'superhost': 'Superhost'})
    #Find out Neighborhood:
    dataset['Localização'] = dataset['Localização'].str.replace('Apartamento inteiro em ','')
    dataset['Localização'] = dataset['Localização'].str.replace('Condomínio inteiro em ','')
    dataset['Localização'] = dataset['Localização'].str.replace('Quarto inteiro em ','')
    dataset['Localização'] = dataset['Localização'].str.replace('Flat inteiro em ','')
    dataset['Localização'] = dataset['Localização'].str.replace('Loft inteiro em ','')
    dataset['Localização'] = dataset['Localização'].str.replace('Suíte de visitas inteira em ','')
    
    #Only numbers
    dataset['Número Hóspedes'] = dataset['Número Hóspedes'].str.replace(' hóspedes','')
    dataset['Número Quartos'] = dataset['Número Quartos'].str.replace(' quartos','')
    dataset['Número Quartos'] = dataset['Número Quartos'].str.replace(' quarto','')
    dataset['Número Camas'] = dataset['Número Camas'].str.replace(' camas','')
    dataset['Número Camas'] = dataset['Número Camas'].str.replace(' cama','')
    dataset['Número Banheiros'] = dataset['Número Banheiros'].str.replace(' banheiros','')
    dataset['Número Banheiros'] = dataset['Número Banheiros'].str.replace(' banheiro','')
    
    x = dataset.drop_duplicates('Localização')
    np.array(x['Localização'])
    
    # Datatime transforming
    dataset['ID'] = dataset['ID'].astype('object')
    dataset['Check-In'] = pd.to_datetime(dataset['Check-In'], format='%Y-%m-%d')
    dataset['Check-Out'] = pd.to_datetime(dataset['Check-Out'], format='%Y-%m-%d')  
    return dataset

import pandas as pd
import numpy as np

def teste_correlacao(df, Target, features, alpha=0.05):
    """
    df = Dataframe
    Target = target
    features = numeric features to be tested
    Return list of variable which are correlationed with target
    """
    from scipy.stats import stats
    correlation = []
    no_correlation = []
    for col in features:
        cor, p = stats.spearmanr(df_train[col],df_train[Target])
        if p <= alpha:
            correlation.append(col)
        else:
            no_correlation.append(col)           
    return correlation


def teste_chi2_(df, features_cat, Target='Target', aplha=0.05):
    """
    Chi2 test
    df = DataFrame
    Target = Target string
    features = List of categorical features
    aplha = indice of significance
    Return a list of variable which has passed for Chi2 test
    """
    from scipy.stats import chi2_contingency
    p_values_cat_features = {}
    for col in features_cat:
        # Cria tabela de contingencia
        df_cross = pd.crosstab(df[col], df[Target])
        # Aplica o teste e extrai o p-valor
        p_value = scipy.stats.chi2_contingency(df_cross)[1]
        # Armazena coluna e p-valor em um dict
        p_values_cat_features[col] = p_value
        
    p_values_cat_features = pd.Series(p_values_cat_features)
    filter_cat_features = p_values_cat_features[p_values_cat_features < aplha].index.tolist()      
    return filter_cat_features


def multicolinearidade(df, features):
    """
    V-Cramer test
    df = DataFrame without Target
    features = numerical features to be tested
    Return a Dataframe with VIF score
    """ 
    from statsmodels.stats.outliers_influence import variance_inflation_factor
    # VIF dataframe 
    vif_data = pd.DataFrame() 
    vif_data["feature"] = df.loc[:,features].columns 
    # calculando VIF 
    vif_data["VIF"] = [variance_inflation_factor(df.loc[:,features].values, i) for i in range(len(df.loc[:,features].columns))]   
    return vif_data.sort_values(by='VIF', ascending=False)


def teste_rfe(X_train, y_train):
    """
    RFE Test
    X_train = Dataframe with all features to be tested and not target
    y_train = Target
    Return a list of varibales which has passed for the test
    """
    from sklearn.feature_selection import RFECV
    from sklearn.ensemble import RandomForestRegressor
    rfecv_RFC = RFECV(estimator=RandomForestRegressor(n_jobs = -1, max_depth = 5), scoring='neg_mean_squared_error')
    rfecv_RFC.fit(X_train,y_train)
    mask_RFC = rfecv_RFC.support_
    cols_selected_RFE = X_train.columns.tolist()   
    return cols_selected_RFE


def teste_boruta(X_train, y_train):
    """
    Boruta Test - Return features which was aproved
    X_train = Dataframe with all features to be tested and not target
    y_train = Target
    Return a list of varibales which has passed for the test
    """
    from boruta import BorutaPy
    from sklearn.ensemble import RandomForestRegressor
    # -1 indica para o python usar todo o processador 
    boruta_selector = BorutaPy(RandomForestRegressor(n_jobs = -1, max_depth = 5), n_estimators = 50, max_iter=100, random_state = 0)
    boruta_selector.fit(np.array(X_train), np.array(y_train))
    boruta_selector.support_
    boruta_selector.support_weak_
    features_boruta = X_train.loc[:, boruta_selector.support_].columns.tolist()
    return features_boruta 


def feature_results(correlation, chi2, rfe, boruta):
    """
    Return a list which has passed for three testes
    correlation = set of result from corrrelation teste
    chi2 = set of features which has passed from chi2 teste
    rfe = set of features which has passed from rfe teste
    boruta = set of features which has passed from boruta teste
    """
    # Junção dos testes de correlação e Chi2
    statistic_test = correlation + chi2
    # Interserção entre testes estatísticos e RFE
    statistic_test_rfe = list(set(statistic_test).intersection(set(rfe)))
    # Interserção entre testes estatísticos e boruta
    statistic_test_boruta = list(set(statistic_test).intersection(set(boruta)))
    # Interserção entre rfe e boruta
    rfe_boruta = list(set(rfe).intersection(set(boruta)))
    
    # Quem passou no primeiro que também passou no boruta
    feature_selection = set(statistic_test_rfe) & set(statistic_test_boruta) & set(rfe_boruta)   
    return feature_selection


def features_for_modeling(df):
    """
    Set of features which has passed from tests
    """
    features = ['Mes', 'Número Banheiros', 'Número Camas', 'Número Comentários', 'Número Hóspedes', 'Taxa',
    'Semana_do_ano', 'Jacuzzi', 'Academia', 'Secadora', 'Localização', 'Piscina', 'Permitido animais','Preço/Noite']
    df = df[features]
    return df

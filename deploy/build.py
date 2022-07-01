from flask import Flask, render_template
import sys
import pandas as pd
import numpy as np
import pickle
import scipy
import os
sys.path.append('..')
# Bibliotecas do formulário
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField, IntegerField, FloatField
from wtforms.validators import DataRequired

#Funções Externas
def create_dates(df, date='Check-In'):
    """
    Create variables called Mês and semana do Ano from Check-In
    """
    df['Check-In'] = pd.to_datetime(df['Check-In'], errors='coerce')
    df['Mes'] = df[date].dt.month
    df['Semana_do_ano'] = df[date].dt.week
    df = df.drop('Check-In', axis=1)
    return df

def tranform_frequency(df, variables='Localização'):
    """
    Transform categorical variable into frequency
    """
    from feature_engine.encoding import CountFrequencyEncoder
    cfce = CountFrequencyEncoder(encoding_method='frequency', variables=[variables])
    df = df.dropna(axis=0)
    df = cfce.fit_transform(df)    
    return df

# Definição de Classe do Formulário.
class my_form(FlaskForm):
    localizacao = StringField('localizacao', validators=[DataRequired()])
    check_in = DateField('check_in', validators=[DataRequired()])
    n_banheiros = IntegerField('n_banheiros', validators=[DataRequired()])
    n_camas = StringField('n_camas', validators=[DataRequired()])
    n_hospedes = IntegerField('n_hospedes', validators=[DataRequired()])
    n_comentarios = IntegerField('n_comentarios')
    taxas = FloatField('taxas')
    academia = BooleanField('academia')
    jacuzzi = BooleanField('jacuzzi')
    secadora = BooleanField('secadora')
    piscina = BooleanField('piscina')
    permitido_animais = BooleanField('permitido_animais')

# Import do modelo: 
MODEL_NAME = 'model_v0.pkl'
MODEL_PATH = '../models'
model = pickle.load(open(os.path.join(MODEL_PATH, MODEL_NAME), 'rb'))

#Instancia um objeto do flask
app = Flask(__name__, template_folder='template')
app.config['SECRET_KEY'] = 'minha_senha'

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    forms = my_form()
    global resultado
    resultado = {}
    if forms.validate_on_submit():
        dicio = {
        'Localização': forms.localizacao.data,
        'Check-In': forms.check_in.data,
        'Número Banheiros': forms.n_banheiros.data,
        'Número Camas': forms.n_camas.data,
        'Número Comentários': forms.n_comentarios.data,
        'Número Hóspedes': forms.n_hospedes.data,
        'Taxa': forms.taxas.data,
        'Jacuzzi': forms.jacuzzi.data,
        'Academia': forms.academia.data,
        'Secadora': forms.secadora.data,
        'Localização': forms.localizacao.data,
        'Piscina': forms.piscina.data,
        'Permitido animais': forms.permitido_animais.data
        }
        df = pd.DataFrame(data=dicio, index=[0])
        df = create_dates(df, date='Check-In') #feature Engineering criar mês e semana do ano
        df = tranform_frequency(df) #feature Engineering - transforming Frequency
        previsao = model.predict(df)
        lambda_found = -0.4897796628352117 #Valor de lambda para conversão box-cox
        previsao = scipy.special.inv_boxcox(previsao, lambda_found) # Retransformação do valor de lambda
        preco_noite = np.round(previsao, 2)
        preco_noite = preco_noite.tolist()
        resultado['Diaria'] = preco_noite
        print(resultado)
    else:
        print(forms.errors) 
    return render_template('home.html', form=forms, resultado=resultado)

if __name__=='__main__':
    app.run(port=5000, debug=True) #Para subir no heroku precisa indicar host='0.0.0.0'. 

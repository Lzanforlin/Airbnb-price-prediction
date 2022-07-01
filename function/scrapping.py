from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# Função para extrção em Masssa.
# em rows guardo uma lista temporária de dicts de dados capturados, 1 dict por imóvel
imoveis_=[]

for pagina in imoveis:
    #print("Estou aqui: " + url.format(npagina=pagina))
    
    # pega a página do site pela internet
    for i in pages:
        doc = requests.get(i, headers={"User-agent": userAgents[1]})
    
        # analiza o HTML
        analizador = BeautifulSoup(doc.content, 'html.parser')

        # extrai somente a lista de imóveis (em HTML) usando o seletor descoberto no código da página
        imoveis = analizador.find_all('div', class_="_gig1e7")

        for unidade in imoveis:
            uni={}
            # extrai dado por dado segundo seus seletores...
            
            # id:
            for link in unidade.select("a"):
                rooms = link.get('href')
                rooms = rooms.split('?')
                uni['id'] = rooms[0].replace('/rooms/', ' ').strip()
                #quarto:
                rooms = rooms[1].split('&')
                #check-in:
                uni['check-in'] = rooms[1].replace('check_in=', ' ').strip()
                #check-out:
                uni['check-out'] = rooms[2].replace('check_out=', ' ').strip()
                
            
            # titulo 1:
            uni['titulo'] = unidade.find("div",class_="_tmwq9g").find("div",class_="_1jzvdu8").find("div",class_="_1tanv1h")
            .find("div",class_="_b14dlit").contents[0].strip()

            # titulo 2:
            uni['titulo_2'] = unidade.find("div",class_="_tmwq9g").find("div",class_="_bzh5lkq").contents[0].strip()

            # atributo 1:
            try:
                uni['atributo_1']  = unidade.find("div",class_="_kqh46o").contents[0].strip()
            except (IndexError, ValueError, AttributeError):
                continue

            # atributo 2:
            try:
                uni['atributo_2'] = unidade.find("div",class_="_kqh46o").contents[2].strip()
            except (IndexError, ValueError, AttributeError):
                continue

            # atributo 3:
            try:
                uni['atributo_3'] = unidade.find("div",class_="_kqh46o").contents[4].strip()
            except (IndexError, ValueError, AttributeError):
                continue

            #atributo 4
            try:
                uni['atributo_4'] = unidade.find("div",class_="_kqh46o").contents[6].strip()
            except (IndexError, ValueError, AttributeError):
                continue
            
            #atributo 5
            try:
                uni['atributo_5'] = unidade.find_next("div", class_="_kqh46o",style="margin-top:4px").contents[0].strip()
            except (IndexError, ValueError, AttributeError):
                continue
            
             #atributo 6
            try:
                uni['atributo_6'] = unidade.find_next("div", class_="_kqh46o",style="margin-top:4px").contents[2].strip()
            except (IndexError, ValueError, AttributeError):
                continue
            
             #atributo 7:
            try:
                uni['atributo_7'] = unidade.find_next("div", class_="_kqh46o",style="margin-top:4px").contents[4].strip()
            except (IndexError, ValueError, AttributeError):
                continue
                
              #atributo 8:
            try:
                uni['atributo_8'] = unidade.find_next("div", class_="_kqh46o",style="margin-top:4px").contents[6].strip()
            except (IndexError, ValueError, AttributeError):
                continue
                    
            # avaliação:
            try: 
                uni['avaliação'] = unidade.find("span",class_="_18khxk1").find("span",class_="_10fy1f8").text.strip()
            except (IndexError, ValueError, AttributeError):
                continue
            
            # comentários:
            try:
                uni['comentários'] = unidade.find("span",class_="_18khxk1").find("span",class_="_a7a5sx")
                .text.replace('(', '').replace(')', '').strip()
            except (IndexError, ValueError, AttributeError):
                continue
            
            # preço:
            try:
                uni['preço'] = unidade.find("span",class_="_olc9rf0").text.replace("R$", " ").strip()
            except (IndexError, ValueError, AttributeError):
                continue   
            
            # preço total:
            try:
                uni['preço_total'] = unidade.find("div",class_="_1c02cnn").text.replace("Total de R$", " ")
                .replace("Ver detalhamento de preço", " ").strip()
            except (IndexError, ValueError, AttributeError):
                continue 
            
            # Superhost:
            try:
                uni['superhost'] = unidade.find("div",class_="_17bkx6k").contents[0].strip()
            except (IndexError, ValueError, AttributeError):
                continue
            
            
            # No final deste loop, o dict uni contém os dados de 1 imóvel, aí adiciono-o a uma lista de imóveis
            imoveis_.append(uni)
                                 
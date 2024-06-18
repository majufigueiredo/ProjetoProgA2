import streamlit as st
import requests
import pandas as pd
from matplotlib import pyplot as plt

# Defina sua chave API
api_key = "88193101454b15bf710f79d9106882aa"

# Função para adicionar uma imagem de fundo
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://raw.githubusercontent.com/majufigueiredo/ProjetoProgA2/upload/main/nuvem");
             background-image: url("https://raw.githubusercontent.com/majufigueiredo/ProjetoProgA2/main/foto.fundo.nuvem.jpg");
             background-size: cover;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

# Adiciona a imagem de fundo
add_bg_from_url()

# Título da aplicação
st.title("Consulta de Clima🌞🌧️❄️")

# Campo de entrada para o nome da cidade
cidade = st.text_input("Digite o nome da cidade:")

# Função para obter o clima a partir das coordenadas
def get_weather(latitude, longitude):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric&lang=pt_br"
    response = requests.get(url)
    if response.status_code == 200:
        dados_cidade = response.json()
        temperatura_atual = dados_cidade['main']['temp']
        name = dados_cidade['name']
        if 'sys' in dados_cidade and 'country' in dados_cidade['sys']:
            country = dados_cidade['sys']['country']
            return name, country, temperatura_atual
        else:
            return None, None, None
    else:
        st.error(f'Error {response.status_code}')
        return None, None, None

# Se o usuário inseriu uma cidade
if cidade:
    # Define a URL da API com os parâmetros necessários
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt_br"

    # Faz a solicitação para a API
    response = requests.get(url)
    dados_clima = response.json()

    # Verifica se a cidade foi encontrada
    if response.status_code == 200:
        # Extrai as informações importantes do JSON retornado
        temperatura_atual = dados_clima['main']['temp']
        temperatura_minima = dados_clima['main']['temp_min']
        temperatura_maxima = dados_clima['main']['temp_max']
        sensacao_termica = dados_clima['main']['feels_like']
        umidade = dados_clima['main']['humidity']
        descricao = dados_clima['weather'][0]['description']
        
        cidade = dados_clima['name']
        latitude = dados_clima['coord']['lat']
        longitude = dados_clima['coord']['lon']
        pais = dados_clima['sys']['country']

        # Exibe as informações
        st.subheader(f"Clima em {cidade.capitalize()} ({pais}):")
        st.write(f"**Descrição:** {descricao.capitalize()}")
        
        # Exibe as métricas
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Temperatura Atual", f"{temperatura_atual}°C")
        col2.metric("Temperatura Mínima", f"{temperatura_minima}°C")
        col3.metric("Sensação Térmica", f"{sensacao_termica}°C")
        col4.metric("Temperatura Máxima", f"{temperatura_maxima}°C")
        col5.metric("Umidade", f"{umidade}%")
        
        # Coleta dados das cidades vizinhas
        cidades = [ { 'localidade': f'{cidade} ({pais})', 'temperatura': temperatura_atual } ]
        for lat in range(-30, 30, 10):
            for lon in range(-30, 30, 10):
                localidade, pais, temperatura_atual = get_weather(latitude + lat/10, longitude + lon/10)
                if localidade:
                    cidades.append({ 'localidade': f'{localidade} ({pais})', 'temperatura': temperatura_atual })

        # Cria DataFrame
        df = pd.DataFrame(cidades)
        
        # Criação do gráfico
        plt.style.use('ggplot')
        df.plot(kind='bar', x='localidade', y='temperatura', figsize=(10, 5), color='darkblue', title='Temperaturas da Região')
        plt.xlabel("Localidades")
        plt.gca().spines[['top', 'right']].set_visible(False)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Exibe o gráfico no Streamlit
        st.pyplot(plt.gcf())
        
    else:
        st.error(f"Não foi possível encontrar o clima para a cidade '{cidade}'. Verifique o nome e tente novamente.")


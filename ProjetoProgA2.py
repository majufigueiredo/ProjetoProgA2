import streamlit as st
import requests
import matplotlib.pyplot as plt
import datetime

# Função para adicionar uma imagem de fundo (opcional)
def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("URL_DA_IMAGEM");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Adiciona a imagem de fundo
add_bg_from_url()

# Título da aplicação
st.title("Consulta de Clima")

# Campo de entrada para o nome da cidade
cidade = st.text_input("Digite o nome da cidade:")

# Sua chave da API (substitua 'sua_api_key' pela sua chave real)
api_key = 'sua_api_key'

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

        # Exibe as informações
        st.subheader(f"Clima em {cidade.capitalize()}:")
        st.write(f"**Descrição:** {descricao.capitalize()}")
        st.write(f"**Temperatura Atual:** {temperatura_atual}°C")
        st.write(f"**Temperatura Mínima:** {temperatura_minima}°C")
        st.write(f"**Temperatura Máxima:** {temperatura_maxima}°C")
        st.write(f"**Sensação Térmica:** {sensacao_termica}°C")
        st.write(f"**Umidade:** {umidade}%")

        # Pega a latitude e longitude da cidade
        lat = dados_clima['coord']['lat']
        lon = dados_clima['coord']['lon']

        # URL da API One Call para previsão semanal
        url_forecast = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={api_key}&units=metric&lang=pt_br"
        response_forecast = requests.get(url_forecast)
        dados_forecast = response_forecast.json()

        if response_forecast.status_code == 200:
            # Extrai os dados de previsão diária
            dias = []
            temperaturas = []

            for dia in dados_forecast['daily']:
                dias.append(datetime.datetime.fromtimestamp(dia['dt']).strftime('%d/%m'))
                temperaturas.append(dia['temp']['day'])

            # Cria o gráfico de linha
            plt.figure(figsize=(10, 5))
            plt.plot(dias, temperaturas, marker='o')
            plt.title(f'Previsão de Temperatura para a Semana em {cidade.capitalize()}')
            plt.xlabel('Dias')
            plt.ylabel('Temperatura (°C)')
            plt.grid(True)
            st.pyplot(plt.gcf())
        else:
            st.error("Não foi possível obter a previsão do tempo. Tente novamente mais tarde.")
    else:
        st.error(f"Não foi possível encontrar o clima para a cidade '{cidade}'. Verifique o nome e tente novamente.")

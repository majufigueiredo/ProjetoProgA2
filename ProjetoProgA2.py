import streamlit as st
import requests

# Defina sua chave API
api_key = "88193101454b15bf710f79d9106882aa"

# Função para adicionar uma imagem de fundo
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://raw.githubusercontent.com/majufigueiredo/ProjetoProgA2/upload/main/nuvem");
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
    else:
        st.error(f"Não foi possível encontrar o clima para a cidade '{cidade}'. Verifique o nome e tente novamente.")


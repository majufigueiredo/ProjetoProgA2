import streamlit as st
import requests
import matplotlib.pyplot as plt

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
st.title("Consulta de Clima⛅")

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
        
        # Exibe as métricas
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Temperatura Atual", f"{temperatura_atual}°C")
        col2.metric("Temperatura Mínima", f"{temperatura_minima}°C")
        col3.metric("Sensação Térmica", f"{sensacao_termica}°C")
        col4.metric("Temperatura Máxima", f"{temperatura_maxima}°C")
        col5.metric("Umidade", f"{umidade}%")
        
        # Dados para o gráfico comparativo
        categorias = ['Temperatura Atual', 'Sensação Térmica', 'Temperatura Máxima']
        valores = [temperatura_atual, sensacao_termica, temperatura_maxima]

        # Criação do gráfico
        plt.figure(figsize=(10, 5))
        plt.plot(categorias, valores, marker='o')
        plt.xlabel('Categorias')
        plt.ylabel('Temperatura (°C)')
        plt.title('Comparação de Temperaturas')
        plt.grid(True)
        
        # Adiciona as linhas com cores diferentes
        plt.plot(categorias[0], valores[0], 'bo-', label='Temperatura Atual')
        plt.plot(categorias[1], valores[1], 'ro-', label='Sensação Térmica')
        plt.plot(categorias[2], valores[2], 'go-', label='Temperatura Máxima')

        # Exibe o gráfico no Streamlit
        st.pyplot(plt.gcf())
        
    else:
        st.error(f"Não foi possível encontrar o clima para a cidade '{cidade}'. Verifique o nome e tente novamente.")


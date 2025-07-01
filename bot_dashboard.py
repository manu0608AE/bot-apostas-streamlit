# Bot de Apostas com Dashboard (com jogos reais via API-Football)

import requests
import datetime
import random
import streamlit as st
import pandas as pd

def obter_jogos_hoje():
    hoje = datetime.datetime.now().strftime('%Y-%m-%d')
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?date={hoje}"

    headers = {
        "X-RapidAPI-Key": "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",
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    resposta = requests.get(url, headers=headers)
    dados = resposta.json()
    jogos = dados.get('response', [])

    lista_jogos = []
    for jogo in jogos:
        info = {
            'Casa': jogo['teams']['home']['name'],
            'Fora': jogo['teams']['away']['name']
        }
        lista_jogos.append(info)

    return lista_jogos

def prever_mercados(jogo):
    p_btts = round(random.uniform(0.5, 0.9), 2)
    p_over25 = round(random.uniform(0.5, 0.9), 2)
    p_htft = round(random.uniform(0.4, 0.8), 2)
    p_cartoes = round(random.uniform(0.6, 0.95), 2)
    p_cantos = round(random.uniform(0.5, 0.85), 2)

    sugestoes = []
    if p_btts > 0.6:
        sugestoes.append(('Ambas Marcam (BTTS)', p_btts, round(1 / p_btts + 0.10, 2)))
    if p_over25 > 0.6:
        sugestoes.append(('Mais de 2.5 Golos', p_over25, round(1 / p_over25 + 0.10, 2)))
    if p_htft > 0.6:
        sugestoes.append(('HT/FT', p_htft, round(1 / p_htft + 0.15, 2)))
    if p_cartoes > 0.65:
        sugestoes.append(('Mais de 4.5 Cartões', p_cartoes, round(1 / p_cartoes + 0.12, 2)))
    if p_cantos > 0.6:
        sugestoes.append(('Mais de 8.5 Cantos', p_cantos, round(1 / p_cantos + 0.10, 2)))

    return sugestoes

def main():
    st.set_page_config(page_title="Bot de Apostas Futebol", layout="wide")
    st.title("📊 Bot de Apostas Desportivas - Futebol")
    st.subheader("Jogos reais com sugestões de mercado")

    jogos = obter_jogos_hoje()
    linhas = []

    for jogo in jogos:
        sugestoes = prever_mercados(jogo)
        for mercado, prob, odd in sugestoes:
            linhas.append({
                'Jogo': f"{jogo['Casa']} vs {jogo['Fora']}",
                'Mercado': mercado,
                'Probabilidade (%)': int(prob * 100),
                'Odd Mínima Recomendada': odd
            })

    if linhas:
        df = pd.DataFrame(linhas)
        mercado_opcao = st.selectbox("Filtrar por mercado:", options=["Todos"] + list(df['Mercado'].unique()))

        if mercado_opcao != "Todos":
            df = df[df['Mercado'] == mercado_opcao]

        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Sem sugestões de apostas para hoje.")

if __name__ == '__main__':
    main()

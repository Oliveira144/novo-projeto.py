import streamlit as st from typing import List

st.set_page_config(layout="wide")

st.title("🔁 Análise de Reescrita - Football Studio")

Mapeamento de cores para emojis

COLOR_MAP = { "🔴": "red", "🔵": "blue", "🟡": "gold" }

def draw_ball(color): return f'<div style="width:26px;height:26px;border-radius:50%;background-color:{color};margin:auto;"></div>'

Entrada de histórico

st.markdown("### 📥 Histórico (mais recente primeiro)") history_input = st.text_area("Digite ou cole os resultados (separados por espaço)", placeholder="🔴 🔵 🟡 🔴 🔵 🔵 🔴...", height=100)

results = history_input.strip().split() if len(results) < 36: st.info("Adicione pelo menos 36 bolas para formar 6 linhas de 9.") st.stop()

Monta linhas de 9 (esquerda para direita)

def montar_linhas(data): linhas = [] for i in range(0, len(data), 9): linhas.append(data[i:i+9]) return linhas[:6]

linhas = montar_linhas(results)

Divide entre atual (3 mais recentes) e antigo (anteriores)

linhas_atual = linhas[:3] linhas_antigo = linhas[3:6] if len(linhas) >= 6 else []

st.markdown("### 🧱 Histórico Atual (esquerda) vs Antigo (direita)") for i in range(3): col_a, col_b = st.columns(2) with col_a: if i < len(linhas_atual): st.markdown("<div style='font-size:28px; text-align:center;'>" + " ".join(linhas_atual[i]) + "</div>", unsafe_allow_html=True) with col_b: if i < len(linhas_antigo): st.markdown("<div style='font-size:28px; text-align:center;'>" + " ".join(linhas_antigo[i]) + "</div>", unsafe_allow_html=True)

Análise da 4ª coluna vs 1ª coluna

st.markdown("### 🔍 Análise: 4ª Coluna vs 1ª Coluna") def colunas_por_indice(linhas): colunas = [[] for _ in range(9)] for linha in linhas: for idx, val in enumerate(linha): colunas[idx].append(val) return colunas

if len(linhas) >= 4: todas_colunas = colunas_por_indice(linhas) col1 = todas_colunas[0]  # Primeira coluna (nova) col4 = todas_colunas[3]  # Quarta coluna (velha)

comparacao = []
match_count = 0
for i in range(min(len(col1), len(col4))):
    ok = "✅" if col1[i] == col4[i] else "❌"
    if ok == "✅":
        match_count += 1
    comparacao.append({"Índice": i+1, "Coluna 1": col1[i], "Coluna 4": col4[i], "Resultado": ok})

st.markdown(f"**Acertos exatos:** {match_count}/3")
st.table(comparacao)

else: st.info("Histórico insuficiente para análise de colunas (mínimo 4 linhas de 9).")

Sugestão com base na estrutura da 4ª coluna

st.markdown("### 🤖 Sugestão Inteligente") if match_count >= 2: st.success("O padrão da 4ª coluna está se repetindo na 1ª coluna.") st.markdown("Sugestão: Baseie a próxima jogada na estrutura da coluna 4.") else: st.warning("A 1ª coluna ainda não replica claramente o padrão da 4ª. Aguarde mais jogadas.")

Estilo

st.markdown(""" <style> .stTextArea textarea { font-size: 20px; line-height: 1.5; } </style> """, unsafe_allow_html=True)


import streamlit as st
from typing import List
from collections import Counter

st.set_page_config(layout="wide")
st.title("🔁 Analisador de Reescrita de Colunas - Football Studio")

# Mapeamento de cores
COLOR_MAP = {
    "🔴": "red",
    "🔵": "blue",
    "🟡": "gold"
}

# Entrada de histórico
st.markdown("### 📥 Digite os resultados (mais recente primeiro)")
history_input = st.text_area(
    "Cole os emojis separados por espaço (mínimo 36):",
    placeholder="🔴 🔵 🟡 🔴 🔵 🔵 🔴...",
    height=120
)

# Processamento do histórico
results = history_input.strip().split()
if len(results) < 36:
    st.info("Digite pelo menos 36 resultados para formar 6 linhas de 9.")
    st.stop()

# Função para dividir em linhas de 9
def build_rows(data):
    rows = []
    for i in range(0, len(data), 9):
        rows.append(data[i:i+9])
    return rows[:6]

rows = build_rows(results)

# Separar em atual (acima) e antigo (abaixo)
current_rows = rows[:3]
old_rows = rows[3:6]

# Mostrar linhas lado a lado
st.markdown("### 🧱 Histórico Atual (esquerda) vs Histórico Antigo (direita)")
for i in range(3):
    col1, col2 = st.columns(2)
    with col1:
        if i < len(current_rows):
            st.markdown(
                "<div style='font-size:28px; text-align:center;'>" +
                " ".join(current_rows[i]) +
                "</div>", unsafe_allow_html=True
            )
    with col2:
        if i < len(old_rows):
            st.markdown(
                "<div style='font-size:28px; text-align:center;'>" +
                " ".join(old_rows[i]) +
                "</div>", unsafe_allow_html=True
            )

# Função para extrair colunas de linhas
def extract_columns(rows: List[List[str]]) -> List[List[str]]:
    columns = [[] for _ in range(9)]
    for row in rows:
        for idx, val in enumerate(row):
            columns[idx].append(val)
    return columns

# Função para normalizar padrão (ex: 🔴🔵🟡 → 123 ou 🔵🔴🔵 → 121)
def normalize_pattern(col: List[str]) -> str:
    mapping = {}
    result = []
    code = 1
    for color in col:
        if color not in mapping:
            mapping[color] = str(code)
            code += 1
        result.append(mapping[color])
    return "".join(result)

# Análise das colunas
st.markdown("### 🔍 Comparar Coluna 1 (nova) com Coluna 4 (anterior)")

if len(rows) >= 4:
    all_columns = extract_columns(rows)
    col1 = all_columns[0]
    col4 = all_columns[3]

    exact_matches = 0
    structure_matches = 0
    comparison = []

    for i in range(3):
        a = col1[i]
        b = col4[i]
        if a == b:
            result = "✅ Exata"
            exact_matches += 1
        elif normalize_pattern([a]) == normalize_pattern([b]):
            result = "🔁 Estrutura"
            structure_matches += 1
        else:
            result = "❌"
        comparison.append({
            "Linha": i + 1,
            "Coluna 1": a,
            "Coluna 4": b,
            "Resultado": result
        })

    st.markdown(f"**Correspondências Exatas:** {exact_matches}/3  ")
    st.markdown(f"**Correspondências Estruturais:** {structure_matches}/3")
    st.table(comparison)
else:
    st.warning("É necessário pelo menos 4 linhas para a análise de coluna.")

# Sugestão Inteligente
st.markdown("### 🤖 Sugestão Inteligente")

if exact_matches >= 2:
    st.success("🧠 A Coluna 1 está repetindo a Coluna 4 exatamente.")
    st.markdown("📌 Sugestão: Siga a estrutura da Coluna 4 para a próxima jogada.")
elif structure_matches >= 2:
    st.info("🔄 A Coluna 1 está reescrevendo a Coluna 4 com outras cores.")
    st.markdown("📌 Sugestão: O padrão estrutural se mantém, considere continuidade com troca de paleta.")
else:
    st.warning("Nenhuma semelhança significativa detectada. Aguarde mais resultados.")

# Estilo extra para textarea
st.markdown("""
<style>
    .stTextArea textarea {
        font-size: 20px;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

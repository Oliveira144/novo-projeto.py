import streamlit as st

# ---------- Configuração da Página ----------
st.set_page_config(page_title="Análise de Padrões - Football Studio", layout="wide")

# ---------- Cores ----------
COLOR_MAP = {
    "🔵": "#3498db",
    "🔴": "#e74c3c",
    "🟡": "#f1c40f",
}

# ---------- Estado Inicial ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Entrada de Resultados ----------
st.title("📊 Histórico em Colunas de 9")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔵 Azul"):
        st.session_state.history.insert(0, "🔵")
with col2:
    if st.button("🔴 Vermelho"):
        st.session_state.history.insert(0, "🔴")
with col3:
    if st.button("🟡 Empate"):
        st.session_state.history.insert(0, "🟡")

# ---------- Função para separar em colunas de 9 ----------
def split_columns(data, size=9):
    return [data[i:i+size] for i in range(0, len(data), size)]

# ---------- Mostrar histórico em colunas ----------
columns = split_columns(st.session_state.history)

st.subheader("📌 Histórico (Mais Recente Primeiro)")
if columns:
    layout = st.columns(len(columns))
    for idx, col_data in enumerate(columns):
        with layout[idx]:
            for item in col_data:
                st.markdown(
                    f"<div style='text-align:center;font-size:36px;margin-bottom:4px;'>{item}</div>",
                    unsafe_allow_html=True
                )
else:
    st.info("Adicione resultados para começar.")

# ---------- Análise da 4ª Coluna vs 1ª Coluna ----------
def analisar_padroes(columns):
    if len(columns) < 4:
        return "🔍 Aguardando pelo menos 4 colunas para análise..."

    ref_col = columns[0]      # Nova coluna (mais recente)
    col_antiga = columns[3]   # Quarta coluna visível (mais antiga)

    comparacoes = []
    for i in range(min(len(ref_col), len(col_antiga))):
        comparacoes.append({
            "Índice": i + 1,
            "4ª Coluna": col_antiga[i],
            "1ª Coluna": ref_col[i],
            "✔️ Igual": "✅" if col_antiga[i] == ref_col[i] else "❌"
        })

    return comparacoes

# ---------- Exibir Análise ----------
st.subheader("🔎 Análise: Reescrita da 4ª Coluna na Nova")

resultado = analisar_padroes(columns)

if isinstance(resultado, str):
    st.info(resultado)
else:
    st.table(resultado)

# ---------- Botão de Limpar ----------
st.markdown("---")
if st.button("🗑️ Limpar Histórico"):
    st.session_state.history = []
    st.experimental_rerun()

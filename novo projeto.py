import streamlit as st

# ---------- Configurações ----------
st.set_page_config(page_title="Análise Inteligente - Football Studio", layout="wide")

# ---------- Mapa de Cores ----------
COLOR_MAP = {
    "🔵": {"color": "#3498db", "text": "#fff"},
    "🔴": {"color": "#e74c3c", "text": "#fff"},
    "🟡": {"color": "#f1c40f", "text": "#000"},
}

# ---------- Inicialização ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Entrada manual ----------
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

# ---------- Função para dividir em colunas de 9 ----------
def split_columns(data, size=9):
    return [data[i:i+size] for i in range(0, len(data), size)]

# ---------- Exibir Histórico ----------
columns = split_columns(st.session_state.history)

st.subheader("📌 Histórico (Mais Recente Primeiro)")
if len(columns) > 0:
    col_layout = st.columns(len(columns))
    for i, col_data in enumerate(columns):
        with col_layout[i]:
            st.markdown(f"**Col {i+1}**")
            for val in col_data:
                info = COLOR_MAP[val]
                st.markdown(
                    f"<div style='background-color:{info['color']};color:{info['text']};text-align:center;padding:6px;border-radius:6px;margin:2px;font-weight:bold'>{val}</div>",
                    unsafe_allow_html=True
                )
else:
    st.info("Ainda sem dados. Comece inserindo resultados.")

# ---------- Lógica de Análise ----------
def analisar_padroes(columns):
    if len(columns) < 4:
        return "🔍 Aguardando pelo menos 4 colunas para análise..."

    ref_col = columns[0]  # Primeira (mais recente)
    padrao_col = columns[3]  # Quarta coluna mais antiga visível

    comparacoes = []
    for i in range(min(len(ref_col), len(padrao_col))):
        match = (ref_col[i] == padrao_col[i])
        comparacoes.append((i+1, padrao_col[i], ref_col[i], match))

    return comparacoes

# ---------- Exibir Análise ----------
st.subheader("🔎 Análise: Reescrita da 4ª Coluna na Nova")
resultado = analisar_padroes(columns)

if isinstance(resultado, str):
    st.info(resultado)
else:
    st.markdown("Se a **primeira coluna** estiver repetindo o padrão da **quarta coluna**, com ou sem cores iguais, você verá abaixo:")
    st.table([
        {"Índice": i, "4ª Coluna": ant, "1ª Coluna": nova, "✔️ Igual": "✅" if ok else "❌"}
        for i, ant, nova, ok in resultado
    ])

# ---------- Botão de Reset ----------
st.markdown("---")
if st.button("🗑️ Limpar Histórico"):
    st.session_state.history = []
    st.experimental_rerun()

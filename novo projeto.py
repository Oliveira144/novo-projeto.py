import streamlit as st

# Configuração da página
st.set_page_config(page_title="Análise Football Studio", layout="wide")

# Mapeamento de cores
COLOR_MAP = {
    "🔵": "#3498db",  # Azul
    "🔴": "#e74c3c",  # Vermelho
    "🟡": "#f1c40f",  # Amarelo
}

# Histórico salvo na sessão
if "history" not in st.session_state:
    st.session_state.history = []

# Entrada dos resultados
st.title("📌 Histórico (Mais Recente Primeiro)")
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

# Função: Quebra o histórico em colunas de 9 (da esquerda pra direita)
def dividir_em_colunas_lado_a_lado(lista, altura=9):
    colunas = [[] for _ in range((len(lista) + altura - 1) // altura)]
    for i, valor in enumerate(lista):
        colunas[i // altura].append(valor)
    return colunas

# Montar colunas
colunas = dividir_em_colunas_lado_a_lado(st.session_state.history)

# Exibir histórico em colunas de bolinhas
st.subheader("🎯 Histórico em Colunas de 9")
if colunas:
    layout = st.columns(len(colunas))
    for i, coluna in enumerate(colunas):
        with layout[i]:
            st.markdown(f"**Coluna {i+1}**")
            for item in coluna:
                st.markdown(
                    f"<div style='text-align:center;font-size:40px;'>{item}</div>",
                    unsafe_allow_html=True
                )
else:
    st.info("Nenhum resultado ainda.")

# Análise: Reescrita da 4ª Coluna na Nova
st.subheader("🔍 Análise: Reescrita da 4ª Coluna na Nova")
if len(colunas) >= 4:
    primeira = colunas[0]
    quarta = colunas[3]
    analise = []
    for i in range(min(len(primeira), len(quarta))):
        analise.append({
            "Índice": i+1,
            "4ª Coluna": quarta[i],
            "1ª Coluna": primeira[i],
            "Resultado": "✅" if quarta[i] == primeira[i] else "❌"
        })
    st.table(analise)
else:
    st.info("🔄 Aguardando pelo menos 4 colunas para comparar...")

# Botão de reset
if st.button("🧹 Limpar Histórico"):
    st.session_state.history = []
    st.experimental_rerun()

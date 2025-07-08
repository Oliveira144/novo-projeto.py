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

# Função: Divide o histórico em linhas completas de 9 elementos
def dividir_em_linhas(lista, elementos_por_linha=9):
    linhas = []
    for i in range(0, len(lista), elementos_por_linha):
        linha = lista[i:i+elementos_por_linha]
        # Completa a linha com None se necessário
        while len(linha) < elementos_por_linha:
            linha.append(None)
        linhas.append(linha)
    return linhas

# Montar linhas
linhas = dividir_em_linhas(st.session_state.history)

# Exibir histórico em linhas de bolinhas
st.subheader("🎯 Histórico em Linhas de 9")
if st.session_state.history:
    for linha in linhas:
        cols = st.columns(9)
        for i, resultado in enumerate(linha):
            with cols[i]:
                if resultado:
                    st.markdown(
                        f"<div style='text-align:center;font-size:40px;'>{resultado}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        "<div style='text-align:center;font-size:40px;'>-</div>",
                        unsafe_allow_html=True
                    )
else:
    st.info("Nenhum resultado ainda.")

# Análise: Reescrita da 4ª Linha na Nova
st.subheader("🔍 Análise: Reescrita da 4ª Linha na Nova")
if len(linhas) >= 4:
    primeira_linha = linhas[0]
    quarta_linha = linhas[3]
    analise = []
    for i in range(9):  # Compara os 9 elementos de cada linha
        if primeira_linha[i] and quarta_linha[i]:
            analise.append({
                "Posição": i+1,
                "4ª Linha": quarta_linha[i],
                "1ª Linha": primeira_linha[i],
                "Resultado": "✅" if quarta_linha[i] == primeira_linha[i] else "❌"
            })
    st.table(analise)
else:
    st.info("🔄 Aguardando pelo menos 4 linhas completas para comparar...")

# Botão de reset
if st.button("🧹 Limpar Histórico"):
    st.session_state.history = []
    st.experimental_rerun()

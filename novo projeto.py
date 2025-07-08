import streamlit as st

# Configuração da página
st.set_page_config(page_title="Análise Football Studio", layout="wide")

# Histórico salvo na sessão
if "history" not in st.session_state:
    st.session_state.history = []

# Entrada dos resultados
st.title("📌 Histórico de Resultados")
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

# Exibir histórico em linha horizontal
st.subheader("🎯 Histórico (Mais Recente na Esquerda)")

# Container flexível para o histórico
history_container = st.container()

# Usar HTML/CSS para criar layout horizontal com quebras
history_html = """
<div style="display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 20px;">
"""

for i, result in enumerate(st.session_state.history):
    # Quebra a cada 9 resultados
    if i > 0 and i % 9 == 0:
        history_html += "</div><div style='display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 20px;'>"
    
    history_html += f"""
    <div style="
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        border: 1px solid #ddd;
        border-radius: 5px;
    ">
        {result}
    </div>
    """

history_html += "</div>"

# Exibir o histórico
if st.session_state.history:
    history_container.markdown(history_html, unsafe_allow_html=True)
else:
    st.info("Nenhum resultado ainda. Adicione os primeiros resultados.")

# Botão de reset
if st.button("🧹 Limpar Histórico"):
    st.session_state.history = []
    st.experimental_rerun()

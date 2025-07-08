import streamlit as st

# Configuração da página
st.set_page_config(page_title="Análise Football Studio", layout="wide")

# Histórico salvo na sessão
if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.rows = []

# Entrada dos resultados
st.title("📌 Histórico de Resultados (Mais Recente à Esquerda)")
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

# Atualizar linhas sempre que o histórico mudar
if st.session_state.history:
    st.session_state.rows = []
    current_row = []
    
    for i, result in enumerate(st.session_state.history):
        current_row.insert(0, result)  # Inverte a ordem na linha
        
        if (i + 1) % 9 == 0:
            st.session_state.rows.insert(0, current_row)
            current_row = []
    
    # Adiciona a linha atual se não estiver vazia
    if current_row:
        # Preenche com espaços vazios se necessário
        while len(current_row) < 9:
            current_row.insert(0, "-")
        st.session_state.rows.insert(0, current_row)

# Exibir histórico em linhas de 9 resultados
st.subheader("🎯 Histórico em Linhas de 9 (Mais Recente à Esquerda)")
if st.session_state.rows:
    for row_idx, row in enumerate(st.session_state.rows):
        st.markdown(f"**Linha {len(st.session_state.rows) - row_idx}**")
        cols = st.columns(9)
        for i, result in enumerate(row):
            with cols[i]:
                if result != "-":
                    st.markdown(
                        f"<div style='text-align:center;font-size:40px;'>{result}</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        "<div style='text-align:center;font-size:40px;color:#cccccc;'>-</div>",
                        unsafe_allow_html=True
                    )
else:
    st.info("Nenhum resultado ainda. Adicione os primeiros resultados.")

# Análise: Comparação com a 4ª linha anterior
st.subheader("🔍 Análise: Comparação com a 4ª Linha Anterior")
if len(st.session_state.rows) >= 4:
    linha_atual = st.session_state.rows[0]
    linha_4_anterior = st.session_state.rows[3]
    
    analise = []
    for pos in range(9):
        analise.append({
            "Posição": pos + 1,
            "Linha Atual": linha_atual[pos],
            "4ª Linha Anterior": linha_4_anterior[pos],
            "Resultado": "✅" if linha_atual[pos] == linha_4_anterior[pos] else "❌"
        })
    st.table(analise)
else:
    st.info("🔄 Aguardando pelo menos 4 linhas completas para comparar...")

# Botão de reset
if st.button("🧹 Limpar Histórico"):
    st.session_state.history = []
    st.session_state.rows = []
    st.experimental_rerun()

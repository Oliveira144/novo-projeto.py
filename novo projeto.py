import streamlit as st

# Configuração da página
st.set_page_config(page_title="Análise Football Studio", layout="wide")

# Histórico salvo na sessão
if "history" not in st.session_state:
    st.session_state.history = []
    st.session_state.rows = []

# Entrada dos resultados
st.title("📌 Histórico de Resultados")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔵 Azul"):
        st.session_state.history.insert(0, "🔵")
        st.session_state.rows = []  # Forçar recálculo das linhas
with col2:
    if st.button("🔴 Vermelho"):
        st.session_state.history.insert(0, "🔴")
        st.session_state.rows = []
with col3:
    if st.button("🟡 Empate"):
        st.session_state.history.insert(0, "🟡")
        st.session_state.rows = []

# Atualizar linhas sempre que o histórico mudar
if not st.session_state.rows and st.session_state.history:
    # Criar linhas completas de 9 resultados
    temp_history = st.session_state.history.copy()
    st.session_state.rows = []
    
    while temp_history:
        # Pegar os próximos 9 resultados (mais recentes primeiro)
        row = temp_history[:9]
        # Completar a linha se necessário
        if len(row) < 9:
            row += ["-"] * (9 - len(row))
        st.session_state.rows.insert(0, row)  # Inserir no início para manter ordem
        temp_history = temp_history[9:]

# Exibir histórico em linhas de 9 resultados
st.subheader("🎯 Histórico em Linhas de 9 (Mais Recente no Topo)")
if st.session_state.rows:
    # Exibir linhas em ordem reversa (mais recente primeiro)
    for idx, row in enumerate(reversed(st.session_state.rows)):
        st.markdown(f"**Linha {idx+1}**")
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
    # Obter as linhas necessárias
    linha_atual = st.session_state.rows[-1]  # Linha mais recente
    linha_4_anterior = st.session_state.rows[-4]  # 4ª linha anterior
    
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

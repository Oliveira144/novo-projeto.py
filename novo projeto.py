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

# Exibir histórico em linha horizontal contínua
st.subheader("🎯 Histórico (Mais Recente na Esquerda)")
if st.session_state.history:
    # Criar uma grade flexível
    cols = st.columns(9 * len(st.session_state.history) // 9 + 1)
    
    # Exibir todos os resultados em uma única linha horizontal
    for i, result in enumerate(st.session_state.history):
        col_index = i % 9
        row_index = i // 9
        
        if i % 9 == 0 and i > 0:
            # Adicionar espaço entre as linhas
            st.write("")
            
        with cols[col_index]:
            st.markdown(
                f"<div style='text-align:center;font-size:40px;margin-bottom:20px;'>{result}</div>",
                unsafe_allow_html=True
            )
else:
    st.info("Nenhum resultado ainda. Adicione os primeiros resultados.")

# Gerar linhas de 9 resultados para análise
rows = []
temp = st.session_state.history.copy()
while temp:
    row = temp[:9]
    if len(row) < 9:
        row += ["-"] * (9 - len(row))
    rows.append(row)
    temp = temp[9:]

# Análise: Comparação com a 4ª linha anterior
st.subheader("🔍 Análise: Comparação com a 4ª Linha Anterior")
if len(rows) >= 4:
    # Linhas: [0] = mais recente, [3] = 4ª linha anterior
    linha_atual = rows[0]
    linha_4_anterior = rows[3]
    
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
    st.experimental_rerun()

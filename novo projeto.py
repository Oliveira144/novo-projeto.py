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

# Gerar linhas de 9 resultados
rows = []
temp = st.session_state.history.copy()
while temp:
    row = temp[:9]
    if len(row) < 9:
        row += ["-"] * (9 - len(row))
    rows.append(row)
    temp = temp[9:]

# Exibir histórico em linhas de 9 resultados
st.subheader("🎯 Histórico em Linhas de 9 (Mais Recente na Esquerda)")
if rows:
    # Exibir do mais recente para o mais antigo (linha 1 = mais recente)
    for idx, row in enumerate(rows, 1):
        st.markdown(f"**Linha {idx}**")
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

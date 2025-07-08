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

if st.session_state.history:
    # Criar HTML para o histórico
    history_html = '<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">'
    
    # Adicionar todos os resultados
    for i, result in enumerate(st.session_state.history):
        # Adicionar quebra de linha a cada 9 itens
        if i > 0 and i % 9 == 0:
            history_html += '</div><div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 20px;">'
        
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
            background-color: #f8f9fa;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            {result}
        </div>
        """
    
    history_html += "</div>"
    
    st.markdown(history_html, unsafe_allow_html=True)
else:
    st.info("Nenhum resultado ainda. Adicione os primeiros resultados.")

# Gerar linhas completas para análise
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
    # Linha atual = mais recente (rows[0])
    # 4ª linha anterior = rows[3]
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
    
    # Exibir tabela de análise
    colunas = st.columns(4)
    with colunas[0]:
        st.markdown("**Posição**")
    with colunas[1]:
        st.markdown("**Linha Atual**")
    with colunas[2]:
        st.markdown("**4ª Linha Anterior**")
    with colunas[3]:
        st.markdown("**Resultado**")
    
    for item in analise:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.text(item["Posição"])
        with col2:
            st.markdown(f"<div style='font-size:24px;text-align:center'>{item['Linha Atual']}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div style='font-size:24px;text-align:center'>{item['4ª Linha Anterior']}</div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div style='font-size:24px;text-align:center'>{item['Resultado']}</div>", unsafe_allow_html=True)
else:
    st.info("🔄 Aguardando pelo menos 4 linhas completas para comparar...")

# Botão de reset
if st.button("🧹 Limpar Histórico"):
    st.session_state.history = []
    st.experimental_rerun()

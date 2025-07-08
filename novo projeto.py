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
    history_html = """
    <div style="
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-bottom: 30px;
    ">
    """
    
    # Adicionar todos os resultados
    for i, result in enumerate(st.session_state.history):
        # Quebra visual a cada 9 itens
        if i > 0 and i % 9 == 0:
            history_html += "</div><div style='display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;'>"
        
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
    
    # Criar tabela de análise
    analise_html = """
    <style>
        .analysis-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .analysis-table th, .analysis-table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: center;
        }
        .analysis-table th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        .match { background-color: #e6ffe6; }
        .mismatch { background-color: #ffe6e6; }
    </style>
    
    <table class="analysis-table">
        <tr>
            <th>Posição</th>
            <th>Linha Atual</th>
            <th>4ª Linha Anterior</th>
            <th>Resultado</th>
        </tr>
    """
    
    for pos in range(9):
        match = linha_atual[pos] == linha_4_anterior[pos]
        row_class = "match" if match else "mismatch"
        
        analise_html += f"""
        <tr class="{row_class}">
            <td>{pos + 1}</td>
            <td style="font-size: 24px;">{linha_atual[pos]}</td>
            <td style="font-size: 24px;">{linha_4_anterior[pos]}</td>
            <td style="font-size: 24px;">{"✅" if match else "❌"}</td>
        </tr>
        """
    
    analise_html += "</table>"
    
    st.markdown(analise_html, unsafe_allow_html=True)
    
    # Estatísticas resumidas
    total_matches = sum(1 for pos in range(9) if linha_atual[pos] == linha_4_anterior[pos])
    match_percentage = (total_matches / 9) * 100
    
    st.metric(label="**Taxa de Acertos**", value=f"{match_percentage:.1f}%")
    st.progress(match_percentage / 100)
    
else:
    st.info("🔄 Aguardando pelo menos 4 linhas completas para comparar...")

# Botão de reset
if st.button("🧹 Limpar Histórico", type="primary"):
    st.session_state.history = []
    st.experimental_rerun()

# Informações adicionais
st.divider()
st.info("💡 **Instruções:** Clique nos botões para adicionar resultados. O histórico é exibido em linhas de 9 resultados, "
        "com os mais recentes aparecendo no canto superior esquerdo. A análise compara a linha atual com a 4ª linha anterior.")

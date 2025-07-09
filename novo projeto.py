# Exibir histórico: mais recente na primeira linha, da esquerda para a direita
st.divider()
st.subheader("📋 Histórico de Jogadas (esquerda → direita, mais recentes no topo)")

# Divide o histórico em blocos de 9, mantendo a ordem direta
linhas = []
for i in range(0, len(st.session_state.historico), 9):
    linha = st.session_state.historico[i:i+9]
    linhas.append(linha)

# Inverte a ordem para mostrar as linhas mais recentes no topo
linhas_exibidas = linhas[::-1]

for idx, linha in enumerate(linhas_exibidas):
    st.markdown(f"**Linha {idx+1}:** " + " ".join(linha))

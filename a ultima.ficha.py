import streamlit as st

# Mapeamento visual
cores = {
    "C": "🔴",  # Casa
    "V": "🔵",  # Visitante
    "E": "🟡",  # Empate
}

# Estado da sessão
if "historico" not in st.session_state:
    st.session_state.historico = []

# Layout e título
st.set_page_config(page_title="FS Colunas Pro", layout="centered")
st.title("🔍 FS Colunas Pro – Análise de Reescrita com Previsão")

# Botões para adicionar jogadas
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🔴 Casa"):
        st.session_state.historico.insert(0, "C")
with col2:
    if st.button("🔵 Visitante"):
        st.session_state.historico.insert(0, "V")
with col3:
    if st.button("🟡 Empate"):
        st.session_state.historico.insert(0, "E")
with col4:
    if st.button("↩️ Desfazer") and st.session_state.historico:
        st.session_state.historico.pop(0)
with col5:
    if st.button("🧹 Limpar"):
        st.session_state.historico = []

st.divider()

# Mostrar histórico
st.markdown("### 📋 Histórico (últimos 27 resultados)")
visual = [cores.get(x, x) for x in st.session_state.historico[:27]]
st.markdown(" ".join(visual))

# Se houver 27 resultados, formar as colunas
if len(st.session_state.historico) >= 27:
    ultimos_27 = st.session_state.historico[:27]

    # Dividir em 3 linhas
    linha1 = ultimos_27[0:9]
    linha2 = ultimos_27[9:18]
    linha3 = ultimos_27[18:27]

    # Formar colunas verticais (3 por coluna)
    colunas = []
    for i in range(9):
        coluna = [linha1[i], linha2[i], linha3[i]]
        colunas.append(coluna)

    st.markdown("### 🧱 Colunas formadas:")
    for i, col in enumerate(colunas, 1):
        estrutura = " ".join([cores.get(c, c) for c in col])
        st.markdown(f"Coluna {i}: {estrutura}")

    # Codificação simbólica da estrutura
    def codificar_coluna(coluna):
        mapa = {}
        codigo = []
        letra_atual = "A"
        for cor in coluna:
            if cor not in mapa:
                mapa[cor] = letra_atual
                letra_atual = chr(ord(letra_atual) + 1)
            codigo.append(mapa[cor])
        return "".join(codigo)

    # Análise de reescrita
    coluna_alvo = colunas[0]
    estrutura_alvo = codificar_coluna(coluna_alvo)
    reescrita_detectada = None
    proxima_cor = None

    for i in range(1, len(colunas)):
        estrutura_i = codificar_coluna(colunas[i])
        if estrutura_i == estrutura_alvo:
            # Verifica qual jogada veio após a coluna original no histórico
            posicao_inicio = i * 3
            if posicao_inicio - 1 < len(st.session_state.historico):
                proxima_cor = st.session_state.historico[posicao_inicio - 1]
            reescrita_detectada = {
                "indice": i + 1,
                "coluna_antiga": colunas[i],
                "estrutura": estrutura_i,
            }
            break

    st.divider()
    st.markdown("### 🔎 Detecção de Reescrita por Estrutura")

    if reescrita_detectada:
        estrutura_antiga = " ".join([cores[c] for c in reescrita_detectada["coluna_antiga"]])
        estrutura_nova = " ".join([cores[c] for c in coluna_alvo])
        st.success(f"🔁 A **coluna 1** reescreve a **coluna {reescrita_detectada['indice']}** com mesma estrutura `{reescrita_detectada['estrutura']}`")
        st.write(f"🔹 Coluna antiga: {estrutura_antiga}")
        st.write(f"🔹 Coluna atual:  {estrutura_nova}")

        if proxima_cor:
            st.markdown("### 🧠 Sugestão baseada no padrão anterior")
            cor_sugerida = cores.get(proxima_cor, proxima_cor)
            st.info(f"🧭 A próxima jogada provável é: **{cor_sugerida}**")

    else:
        st.warning("Nenhuma reescrita estrutural detectada por enquanto.")

else:
    st.info("Adicione pelo menos 27 resultados para ativar a análise por colunas (3 linhas de 9).")

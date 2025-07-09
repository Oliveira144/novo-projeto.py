import streamlit as st
from collections import Counter

# Inicializa histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# Constantes
RESULTADOS_POR_LINHA = 7
MAX_LINHAS_HISTORICO = 80
MAX_JOGADAS = RESULTADOS_POR_LINHA * MAX_LINHAS_HISTORICO

# Funções de lógica
def cores_opostas(c1, c2):
    return (c1 == "🔴" and c2 == "🔵") or (c1 == "🔵" and c2 == "🔴")

def padrao_reescrito(linha1, linha2):
    if len(linha1) != len(linha2):
        return False
    for a, b in zip(linha1, linha2):
        if a == "🟡" or b == "🟡":
            continue
        if not cores_opostas(a, b):
            return False
    return True

def colunas_semelhantes(c1, c2):
    if len(c1) != len(c2):
        return False
    for a, b in zip(c1, c2):
        if a == "🟡" or b == "🟡":
            continue
        if not cores_opostas(a, b):
            return False
    return True

def inserir(cor):
    st.session_state.historico.insert(0, cor)
    if len(st.session_state.historico) > MAX_JOGADAS:
        st.session_state.historico = st.session_state.historico[:MAX_JOGADAS]

def desfazer():
    if st.session_state.historico:
        st.session_state.historico.pop(0)

def limpar():
    st.session_state.historico.clear()

# Configuração visual
st.set_page_config(page_title="FS Análise Pro", layout="centered")

st.title("📊 FS Análise Pro")
st.caption("Detecção de padrões reescritos e sugestões inteligentes para o jogo Football Studio Live")

# Botões de entrada
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔴 Casa", use_container_width=True): inserir("🔴")
with col2:
    if st.button("🔵 Visitante", use_container_width=True): inserir("🔵")
with col3:
    if st.button("🟡 Empate", use_container_width=True): inserir("🟡")

# Controles
col4, col5, col6 = st.columns(3)
with col4:
    if st.button("↩️ Desfazer", use_container_width=True): desfazer()
with col5:
    if st.button("🧹 Limpar", use_container_width=True): limpar()
with col6:
    # Botão para mostrar/ocultar histórico completo
    mostrar_historico_completo = st.toggle("Mostrar histórico completo", value=True)

# Exibir histórico
st.markdown("---")
st.subheader(f"📋 Histórico de Jogadas (últimas {MAX_LINHAS_HISTORICO} linhas)")

historico_limitado = st.session_state.historico[:MAX_JOGADAS]
linhas = []
for i in range(0, len(historico_limitado), RESULTADOS_POR_LINHA):
    linha = historico_limitado[i:i+RESULTADOS_POR_LINHA]
    linhas.append(linha)

# Exibe apenas as últimas N linhas ou todo o histórico
if mostrar_historico_completo:
    linhas_exibidas = linhas[:MAX_LINHAS_HISTORICO]
else:
    # Mostra apenas as últimas 5 linhas por padrão
    linhas_exibidas = linhas[:5] 

# Container com rolagem
with st.container(height=400):
    for idx, linha in enumerate(linhas_exibidas, 1):
        st.markdown(f"**Linha {idx}:** " + " ".join(linha))

# Frequência
st.markdown("---")
st.subheader("📊 Frequência de Cores")
contagem = Counter(historico_limitado)
st.write(f"🔴 Casa: {contagem['🔴']} | 🔵 Visitante: {contagem['🔵']} | 🟡 Empate: {contagem['🟡']}")

# Análise por linhas (padrão reescrito) - RESTAURADA
st.markdown("---")
st.subheader("🧠 Detecção de Padrão Reescrito")

linhas_completas = [l for l in linhas if len(l) == RESULTADOS_POR_LINHA]

if len(linhas_completas) >= 2:
    linha_recente = linhas_completas[0]
    linha_anterior = linhas_completas[1]

    if padrao_reescrito(linha_recente, linha_anterior):
        ultima_jogada = linha_recente[-1]
        if ultima_jogada == "🔴":
            jogada_sugerida = "🔵"
        elif ultima_jogada == "🔵":
            jogada_sugerida = "🔴"
        else:
            jogada_sugerida = "🟡"
            
        st.success(f"""
        🔁 **Padrão reescrito com inversão cromática detectado!**
        \nÚltima jogada: {ultima_jogada}
        \n🎯 **Sugestão:** Jogar {jogada_sugerida}
        """)
    else:
        st.info("⏳ Nenhum padrão reescrito identificado entre as duas últimas linhas completas.")
else:
    st.warning(f"⚠️ Registre pelo menos 2 linhas completas de {RESULTADOS_POR_LINHA} jogadas para ativar a análise.")

# Análise por colunas verticais - RESTAURADA E MELHORADA
st.markdown("---")
st.subheader("🧬 Análise por Colunas Verticais")

# Seleciona as últimas 3 linhas completas
linhas_para_colunas = [l for l in linhas_completas[:3] if len(l) == RESULTADOS_POR_LINHA]

if len(linhas_para_colunas) >= 3:
    matriz_3x7 = linhas_para_colunas[:3]
    colunas = list(zip(*matriz_3x7))

    # Verificação de segurança
    if len(colunas) >= 5:
        ref_coluna_antiga = colunas[3]
        nova_coluna = colunas[0]

        if colunas_semelhantes(ref_coluna_antiga, nova_coluna):
            coluna_apos_ref = colunas[4]
            if coluna_apos_ref: 
                proxima_sugestao = coluna_apos_ref[0]
                if proxima_sugestao == "🔴":
                    sugestao_convertida = "🔵"
                elif proxima_sugestao == "🔵":
                    sugestao_convertida = "🔴"
                else:
                    sugestao_convertida = "🟡"

                st.success(f"""
                🔂 Estrutura de colunas repetida detectada!
                \n📌 Padrão: Coluna 4 ≈ Coluna 1
                \n💡 Após coluna 4 veio: **{proxima_sugestao}**
                \n🎯 **Sugestão:** Jogar {sugestao_convertida}
                """)
            else:
                st.info("🔍 Padrão detectado, mas sem sugestão disponível")
        else:
            st.info("📊 Nenhum padrão de colunas repetido encontrado")
    else:
        st.warning("⚠️ Dados insuficientes para análise completa de colunas")
else:
    st.warning(f"⚠️ Registre 3 linhas completas de {RESULTADOS_POR_LINHA} jogadas para análise de colunas")

# Visualização das colunas verticais - RESTAURADA
if len(linhas_para_colunas) >= 3:
    st.markdown("---")
    st.subheader("🧱 Visualização das Colunas (Últimas 3 Linhas)")

    # Cria uma matriz para visualização
    matriz_exibicao = linhas_para_colunas[:3]
    colunas_exibicao = list(zip(*matriz_exibicao))
    
    # Cria colunas para exibição
    cols = st.columns(len(colunas_exibicao))
    
    for i, coluna in enumerate(colunas_exibicao):
        with cols[i]:
            st.markdown(f"**Coluna {i+1}**")
            for elemento in coluna:
                # Cores de fundo
                bg_color = "#ffcccc" if elemento == "🔴" else "#cce0ff" if elemento == "🔵" else "#ffffcc"
                st.markdown(
                    f'<div style="background-color: {bg_color}; padding: 10px; margin: 5px; border-radius: 5px; text-align: center;">{elemento}</div>',
                    unsafe_allow_html=True
                )

# Botão para análise de tendências - NOVA FUNCIONALIDADE
st.markdown("---")
st.subheader("📈 Análise de Tendências")

if len(linhas_completas) > 0:
    # Calcula a porcentagem de cada cor nas últimas 5 linhas
    ultimas_jogadas = [item for sublist in linhas_completas[:5] for item in sublist]
    if ultimas_jogadas:
        contagem_tendencia = Counter(ultimas_jogadas)
        total = len(ultimas_jogadas)
        
        st.write("**Distribuição nas últimas jogadas:**")
        col_casa, col_visit, col_empate = st.columns(3)
        with col_casa:
            percent_casa = (contagem_tendencia["🔴"] / total) * 100
            st.metric("🔴 Casa", f"{percent_casa:.1f}%")
        with col_visit:
            percent_visit = (contagem_tendencia["🔵"] / total) * 100
            st.metric("🔵 Visitante", f"{percent_visit:.1f}%")
        with col_empate:
            percent_empate = (contagem_tendencia["🟡"] / total) * 100
            st.metric("🟡 Empate", f"{percent_empate:.1f}%")
else:
    st.info("Registre jogadas para ver as tendências")

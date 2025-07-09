import streamlit as st
from collections import Counter

# Inicializa histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# Constantes
RESULTADOS_POR_LINHA = 7
MAX_LINHAS_HISTORICO = 80  # 80 linhas de histórico
MAX_JOGADAS = RESULTADOS_POR_LINHA * MAX_LINHAS_HISTORICO  # 560 jogadas

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
    # Mantém até 560 jogadas (80 linhas)
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
col4, col5 = st.columns(2)
with col4:
    if st.button("↩️ Desfazer", use_container_width=True): desfazer()
with col5:
    if st.button("🧹 Limpar", use_container_width=True): limpar()

# Exibir histórico (até 80 linhas)
st.markdown("---")
st.subheader(f"📋 Histórico de Jogadas (últimas {MAX_LINHAS_HISTORICO} linhas, 7 por linha)")

# Divide em linhas de 7
historico_limitado = st.session_state.historico[:MAX_JOGADAS]
linhas = []
for i in range(0, len(historico_limitado), RESULTADOS_POR_LINHA):
    linha = historico_limitado[i:i+RESULTADOS_POR_LINHA]
    linhas.append(linha)

# Exibe até as últimas 80 linhas completas
linhas_exibidas = linhas[:MAX_LINHAS_HISTORICO]

# Cria container com rolagem
with st.container(height=400):  # Altura fixa com scroll
    for idx, linha in enumerate(linhas_exibidas, 1):
        st.markdown(f"**Linha {idx}:** " + " ".join(linha))

# Frequência
st.markdown("---")
st.subheader("📊 Frequência de Cores")
contagem = Counter(historico_limitado)
st.write(f"🔴 Casa: {contagem['🔴']} | 🔵 Visitante: {contagem['🔵']} | 🟡 Empate: {contagem['🟡']}")

# Análise por linhas (padrão reescrito)
st.markdown("---")
st.subheader("🧠 Detecção de Padrão Reescrito")

# Filtra apenas linhas completas
linhas_completas = [l for l in linhas_exibidas if len(l) == RESULTADOS_POR_LINHA]

if len(linhas_completas) >= 2:
    # Duas linhas mais recentes
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

# Análise por colunas verticais
st.markdown("---")
st.subheader("🧬 Análise por Colunas Verticais")

# Seleciona as últimas 3 linhas completas
linhas_para_colunas = [l for l in linhas_completas[:3] if len(l) == RESULTADOS_POR_LINHA]

if len(linhas_para_colunas) == 3:
    # Monta matriz 3x7
    matriz_3x7 = linhas_para_colunas
    
    # Transpõe para colunas
    colunas = list(zip(*matriz_3x7))

    # Referência: Coluna 4 (índice 3) e Nova Coluna (índice 0)
    if len(colunas) >= 5:  # Garante que temos coluna 4 e 5
        ref_coluna_antiga = colunas[3]
        nova_coluna = colunas[0]

        if colunas_semelhantes(ref_coluna_antiga, nova_coluna):
            coluna_apos_ref = colunas[4]
            if coluna_apos_ref:  # Verifica se tem elementos
                proxima_sugestao = coluna_apos_ref[0]
                if proxima_sugestao == "🔴":
                    sugestao_convertida = "🔵"
                elif proxima_sugestao == "🔵":
                    sugestao_convertida = "🔴"
                else:
                    sugestao_convertida = "🟡"

                st.success(f"""
                🔂 Estrutura de colunas repetida com troca de cores detectada!
                \n📌 Coluna antiga (posição 4) ≈ Nova coluna (posição 1)
                \n💡 Padrão esperado: Após a coluna 4 veio **{proxima_sugestao}**
                \n🎯 **Sugestão:** Jogar {sugestao_convertida}
                """)
            else:
                st.info("⚠️ Não foi possível gerar sugestão (coluna de referência vazia)")
        else:
            st.info("📊 Nenhum padrão repetido de colunas encontrado nas últimas 3 linhas.")
    else:
        st.warning("⚠️ Dados insuficientes para análise de colunas")
else:
    st.warning(f"⚠️ Registre 3 linhas completas de {RESULTADOS_POR_LINHA} jogadas para ativar a análise por colunas")

# Visualização das colunas verticais com cores
if len(linhas_para_colunas) == 3:
    st.subheader("🧱 Visualização das Últimas 3 Linhas (Colunas Verticais)")

    col_container = st.container()
    cols = col_container.columns(RESULTADOS_POR_LINHA)
    
    colunas_texto = list(zip(*matriz_3x7))

    for i, coluna in enumerate(colunas_texto):
        elementos_html = []
        for elemento in coluna:
            if elemento == "🔴":
                bg_color = "#ffcccc"
            elif elemento == "🔵":
                bg_color = "#cce0ff"
            else:
                bg_color = "#ffffcc"
                
            elementos_html.append(
                f'<div style="background-color: {bg_color};'
                f'padding: 8px; margin: 2px; border-radius: 5px;'
                f'text-align: center;">{elemento}</div>'
            )
        
        texto_html = f"<b>Coluna {i+1}</b><br>" + "<br>".join(elementos_html)
        if i < len(cols):  # Previne erro de índice
            cols[i].markdown(texto_html, unsafe_allow_html=True)

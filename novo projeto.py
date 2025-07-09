import streamlit as st
from collections import Counter, defaultdict
import numpy as np

# Inicializa histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# Constantes
RESULTADOS_POR_LINHA = 8
MAX_LINHAS_HISTORICO = 80
MAX_JOGADAS = RESULTADOS_POR_LINHA * MAX_LINHAS_HISTORICO

# Funções de lógica
def cores_opostas(c1, c2):
    return (c1 == "🔴" and c2 == "🔵") or (c1 == "🔵" and c2 == "🔴")

def padrao_reescrito(linha1, linha2, tolerancia=1):
    """Detecta padrão de reescrita com tolerância a variações"""
    if len(linha1) != len(linha2):
        return False
    
    diferencas = 0
    for a, b in zip(linha1, linha2):
        if a == "🟡" or b == "🟡":
            continue
        if not cores_opostas(a, b):
            diferencas += 1
            if diferencas > tolerancia:
                return False
    return diferencas <= tolerancia

def colunas_semelhantes(c1, c2, tolerancia=1):
    """Compara colunas com tolerância a variações"""
    if len(c1) != len(c2):
        return False
    
    diferencas = 0
    for a, b in zip(c1, c2):
        if a == "🟡" or b == "🟡":
            continue
        if not cores_opostas(a, b):
            diferencas += 1
            if diferencas > tolerancia:
                return False
    return diferencas <= tolerancia

def inserir(cor):
    st.session_state.historico.insert(0, cor)
    if len(st.session_state.historico) > MAX_JOGADAS:
        st.session_state.historico = st.session_state.historico[:MAX_JOGADAS]

def desfazer():
    if st.session_state.historico:
        st.session_state.historico.pop(0)

def limpar():
    st.session_state.historico.clear()

# Algoritmo avançado de varredura de colunas
def analisar_colunas(linhas_completas):
    """Realiza varredura completa em todas as colunas para identificar padrões"""
    padroes_detectados = []
    
    if len(linhas_completas) < 3:
        return padroes_detectados
    
    # Cria matriz de colunas
    matriz = linhas_completas[:3]
    colunas = list(zip(*matriz))
    total_colunas = len(colunas)
    
    # Lista para armazenar padrões encontrados
    padroes = []
    
    # Varre todas as combinações possíveis de colunas
    for j in range(total_colunas):
        for i in range(j):
            if colunas_semelhantes(colunas[i], colunas[j]):
                padroes.append((i, j))
    
    # Gera sugestões baseadas nos padrões encontrados
    for i, j in padroes:
        # Verifica se há coluna após a coluna de referência
        if i + 1 < total_colunas:
            coluna_apos_ref = colunas[i + 1]
            
            # Usa o elemento mais comum na coluna seguinte
            contagem = Counter(coluna_apos_ref)
            if contagem:
                elemento_comum = contagem.most_common(1)[0][0]
                
                # Sugestão baseada no elemento mais comum
                if elemento_comum == "🔴":
                    sugestao = "🔵"
                elif elemento_comum == "🔵":
                    sugestao = "🔴"
                else:
                    sugestao = "🟡"
                
                # Calcula confiança baseada na consistência
                confianca = len([k for k in coluna_apos_ref if k == elemento_comum]) / len(coluna_apos_ref)
                
                padroes_detectados.append({
                    "coluna_ref": i,
                    "coluna_atual": j,
                    "coluna_apos_ref": i + 1,
                    "sugestao": sugestao,
                    "elemento_referencia": elemento_comum,
                    "confianca": confianca
                })
    
    return padroes_detectados

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

# Processar histórico
historico_limitado = st.session_state.historico[:MAX_JOGADAS]
linhas = []
for i in range(0, len(historico_limitado), RESULTADOS_POR_LINHA):
    linha = historico_limitado[i:i+RESULTADOS_POR_LINHA]
    linhas.append(linha)

# Filtra linhas completas
linhas_completas = [l for l in linhas if len(l) == RESULTADOS_POR_LINHA]

# Executa análises
padroes_colunas = analisar_colunas(linhas_completas)

# =================================================================
# INTERFACE DO USUÁRIO
# =================================================================

# Exibir histórico
st.markdown("---")
st.subheader(f"📋 Histórico de Jogadas ({RESULTADOS_POR_LINHA} por linha)")

with st.container(height=400):
    for idx, linha in enumerate(linhas, 1):
        st.markdown(f"**Linha {idx}:** " + " ".join(linha))

# Frequência
st.markdown("---")
st.subheader("📊 Frequência de Cores")
contagem = Counter(historico_limitado)
st.write(f"🔴 Casa: {contagem['🔴']} | 🔵 Visitante: {contagem['🔵']} | 🟡 Empate: {contagem['🟡']}")

# Análise de padrão reescrito
st.markdown("---")
st.subheader("🧠 Detecção de Padrão Reescrito")

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
elif len(historico_limitado) < (RESULTADOS_POR_LINHA * 2):
    st.warning(f"⚠️ Registre pelo menos {RESULTADOS_POR_LINHA * 2} jogadas para ativar a análise (2 linhas de {RESULTADOS_POR_LINHA}).")
else:
    st.info("Aguardando segunda linha completa para análise.")

# Análise avançada de colunas
st.markdown("---")
st.subheader("🔍 Varredura Avançada de Colunas")

if padroes_colunas:
    st.success(f"✅ {len(padroes_colunas)} padrões de colunas detectados!")
    
    # Agrupa sugestões por tipo com confiança
    sugestoes_agrupadas = defaultdict(list)
    for padrao in padroes_colunas:
        sugestoes_agrupadas[padrao["sugestao"]].append(padrao["confianca"])
    
    # Exibe sugestões consolidadas com porcentagem de confiança
    st.subheader("🎯 Sugestões de Entrada")
    
    if sugestoes_agrupadas:
        for sugestao, confiancas in sugestoes_agrupadas.items():
            confianca_media = np.mean(confiancas) * 100
            st.metric(
                label=f"Jogar {sugestao}", 
                value=f"{confianca_media:.1f}% de confiança",
                help=f"Baseado em {len(confiancas)} padrões detectados"
            )
    
    # Mostra detalhes dos padrões detectados
    with st.expander("📝 Detalhes dos Padrões Detectados"):
        for i, padrao in enumerate(padroes_colunas, 1):
            st.write(f"**Padrão {i}:**")
            st.write(f"- Coluna de referência: {padrao['coluna_ref']+1}")
            st.write(f"- Coluna atual: {padrao['coluna_atual']+1}")
            st.write(f"- Após referência veio: {padrao['elemento_referencia']} (confiança: {padrao['confianca']*100:.1f}%)")
            st.write(f"- Sugestão: {padrao['sugestao']}")
            st.markdown("---")
else:
    if len(linhas_completas) >= 3:
        st.info("ℹ️ Nenhum padrão de reescrita entre colunas foi detectado")
    else:
        st.warning(f"⚠️ Registre 3 linhas completas de {RESULTADOS_POR_LINHA} jogadas para ativar a análise")

# Visualização das colunas verticais
if len(linhas_completas) >= 3:
    st.markdown("---")
    st.subheader("🧱 Visualização das Colunas (Últimas 3 Linhas)")
    
    matriz_3x8 = linhas_completas[:3]
    colunas = list(zip(*matriz_3x8))
    
    # Cria colunas para exibição
    cols = st.columns(RESULTADOS_POR_LINHA)
    
    for i, coluna in enumerate(colunas):
        with cols[i]:
            # Destaca colunas com padrões detectados
            em_padrao = any(p['coluna_ref'] == i or p['coluna_atual'] == i for p in padroes_colunas)
            borda = "4px solid #4CAF50" if em_padrao else "1px solid #ccc"
            bg_title = "#e8f5e9" if em_padrao else "#f5f5f5"
            
            st.markdown(f"<div style='background-color: {bg_title}; border: {borda}; border-radius: 5px; padding: 5px; margin-bottom: 10px;'>"
                        f"<b>Coluna {i+1}</b></div>", unsafe_allow_html=True)
            
            for elemento in coluna:
                bg_color = "#ffcccc" if elemento == "🔴" else "#cce0ff" if elemento == "🔵" else "#ffffcc"
                st.markdown(
                    f'<div style="background-color: {bg_color}; padding: 8px; margin: 2px; border-radius: 5px; text-align: center;">{elemento}</div>',
                    unsafe_allow_html=True
                )

# Análise de tendências
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

# Botão para exportar dados
st.markdown("---")
if st.button("💾 Exportar Dados para Análise"):
    dados = {
        "historico": st.session_state.historico,
        "linhas_completas": linhas_completas,
        "padroes_detectados": padroes_colunas
    }
    st.download_button(
        label="Baixar Dados",
        data=str(dados),
        file_name="fs_analise_dados.txt",
        mime="text/plain"
    )

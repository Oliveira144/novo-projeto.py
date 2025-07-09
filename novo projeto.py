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
    """Detecta se linha1 é uma reescrita de linha2 com cores invertidas"""
    if len(linha1) != len(linha2):
        return False
    for a, b in zip(linha1, linha2):
        if a == "🟡" or b == "🟡":
            continue
        if not cores_opostas(a, b):
            return False
    return True

def detectar_padrao_reescrita(historico):
    """Analisa o histórico para encontrar padrões de reescrita entre linhas"""
    padroes = []
    linhas_completas = [linha for linha in historico if len(linha) == RESULTADOS_POR_LINHA]
    
    for i in range(1, len(linhas_completas)):
        linha_atual = linhas_completas[i-1]  # Linha mais recente
        linha_anterior = linhas_completas[i]   # Linha anterior
        
        if padrao_reescrito(linha_atual, linha_anterior):
            # Determinar sugestão baseada no último elemento
            ultimo_elemento = linha_atual[-1]
            sugestao = "🔵" if ultimo_elemento == "🔴" else "🔴" if ultimo_elemento == "🔵" else "🟡"
            
            padroes.append({
                "linha_atual": linha_atual,
                "linha_anterior": linha_anterior,
                "sugestao": sugestao
            })
    
    return padroes

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

# Detectar padrões de reescrita
padroes_reescrita = detectar_padrao_reescrita(linhas)

# Exibir histórico com destaque para padrões
st.markdown("---")
st.subheader(f"📋 Histórico de Jogadas (Padrões Detectados)")

with st.container(height=500):
    for idx, linha in enumerate(linhas, 1):
        # Verificar se esta linha está em um padrão detectado
        em_padrao = any(linha == padrao["linha_atual"] for padrao in padroes_reescrita)
        
        if em_padrao:
            # Encontrar o padrão completo correspondente
            padrao_correspondente = next((p for p in padroes_reescrita if p["linha_atual"] == linha), None)
            
            # Exibir com destaque especial
            st.markdown(f"<div style='background-color: #e6f7ff; padding: 10px; border-radius: 5px; border-left: 4px solid #1890ff; margin-bottom: 10px;'>"
                        f"<b>Linha {idx} (Padrão Detectado):</b> " + " ".join(linha) +
                        f"<br>🎯 <b>Sugestão:</b> {padrao_correspondente['sugestao']}</div>", 
                        unsafe_allow_html=True)
        else:
            st.markdown(f"**Linha {idx}:** " + " ".join(linha))

# Análise de padrão reescrito em tempo real
st.markdown("---")
st.subheader("🧠 Detecção de Padrão de Reescreta Atual")

if len(linhas) >= 2:
    linha_atual = linhas[0]  # Linha mais recente
    linha_anterior = linhas[1]  # Segunda linha mais recente
    
    # Verificar se temos linhas completas para análise
    if len(linha_atual) == RESULTADOS_POR_LINHA and len(linha_anterior) == RESULTADOS_POR_LINHA:
        if padrao_reescrito(linha_atual, linha_anterior):
            # Determinar sugestão com base no último elemento da linha atual
            ultimo_elemento = linha_atual[-1]
            sugestao = "🔵" if ultimo_elemento == "🔴" else "🔴" if ultimo_elemento == "🔵" else "🟡"
            
            st.success(f"""
            🔁 **Padrão de reescrita detectado entre Linha 1 e Linha 2!**
            
            **Linha 1 (Atual):** {" ".join(linha_atual)}
            **Linha 2 (Anterior):** {" ".join(linha_anterior)}
            
            🎯 **Sugestão de Entrada:** {sugestao}
            """)
            
            # Mostrar visualização do padrão
            cols = st.columns(RESULTADOS_POR_LINHA)
            for i, (a, b) in enumerate(zip(linha_atual, linha_anterior)):
                with cols[i]:
                    st.markdown(f"**Posição {i+1}**")
                    st.markdown(f"{a} → {b}")
                    # Mostrar ✓ se cores opostas ou ✗ se iguais
                    if a == "🟡" or b == "🟡":
                        st.markdown("➖")
                    else:
                        st.markdown("✓" if cores_opostas(a, b) else "✗")
        else:
            st.info("⏳ Ainda não foi detectado um padrão de reescrita entre a Linha 1 e Linha 2.")
    else:
        st.warning(f"⚠️ Complete ambas as linhas com {RESULTADOS_POR_LINHA} jogadas para análise")
else:
    st.warning("⚠️ Registre pelo menos 2 linhas para análise de padrões")

# Estatísticas de padrões detectados
if padroes_reescrita:
    st.markdown("---")
    st.subheader("📈 Estatísticas de Padrões de Reescreta")
    
    total_padroes = len(padroes_reescrita)
    st.write(f"**Total de padrões detectados:** {total_padroes}")
    
    # Mostrar últimos padrões detectados
    st.write("**Últimos padrões detectados:**")
    for padrao in padroes_reescrita[:3]:
        st.caption(f"- Linha atual: {' '.join(padrao['linha_atual'])} | Sugestão: {padrao['sugestao']}")

# Frequência
st.markdown("---")
st.subheader("📊 Frequência de Cores")
contagem = Counter(historico_limitado)
st.write(f"🔴 Casa: {contagem['🔴']} | 🔵 Visitante: {contagem['🔵']} | 🟡 Empate: {contagem['🟡']}")

# Visualização avançada de padrões
if padroes_reescrita:
    st.markdown("---")
    st.subheader("🔍 Visualização de Padrões de Reescreta")
    
    # Selecionar o último padrão detectado
    ultimo_padrao = padroes_reescrita[0]
    
    st.write("**Comparação de Linhas:**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Linha Atual**")
        for elemento in ultimo_padrao["linha_atual"]:
            bg_color = "#ffcccc" if elemento == "🔴" else "#cce0ff" if elemento == "🔵" else "#ffffcc"
            st.markdown(f'<div style="background-color: {bg_color}; padding: 10px; margin: 5px; border-radius: 5px; text-align: center;">{elemento}</div>', 
                        unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Linha Anterior**")
        for elemento in ultimo_padrao["linha_anterior"]:
            bg_color = "#ffcccc" if elemento == "🔴" else "#cce0ff" if elemento == "🔵" else "#ffffcc"
            st.markdown(f'<div style="background-color: {bg_color}; padding: 10px; margin: 5px; border-radius: 5px; text-align: center;">{elemento}</div>', 
                        unsafe_allow_html=True)
    
    st.markdown(f"**Sugestão Gerada:** {ultimo_padrao['sugestao']}")

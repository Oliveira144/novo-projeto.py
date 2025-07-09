import streamlit as st
from collections import Counter
import numpy as np

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
        linha_atual = linhas_completas[i-1]  # Linha mais recente (índice 0)
        linha_anterior = linhas_completas[i]   # Linha anterior (índice 1)
        
        if padrao_reescrito(linha_atual, linha_anterior):
            posicao_reescrita = len(linha_atual)  # Posição atual da reescrita
            padroes.append({
                "linha_atual": linha_atual,
                "linha_anterior": linha_anterior,
                "posicao": posicao_reescrita,
                "sugestao": "🔵" if linha_atual[-1] == "🔴" else "🔴" if linha_atual[-1] == "🔵" else "🟡"
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
            linha_anterior = padrao_correspondente["linha_anterior"]
            
            # Exibir com destaque especial
            st.markdown(f"<div style='background-color: #e6f7ff; padding: 10px; border-radius: 5px; border-left: 4px solid #1890ff; margin-bottom: 10px;'>"
                        f"<b>Linha {idx} (Padrão Detectado):</b> " + " ".join(linha) +
                        f"<br><b>Linha {idx+1}:</b> " + " ".join(linha_anterior) +
                        f"<br>🎯 <b>Sugestão:</b> {padrao_correspondente['sugestao']}</div>", 
                        unsafe_allow_html=True)
        else:
            st.markdown(f"**Linha {idx}:** " + " ".join(linha))

# Análise de padrão reescrito em tempo real
st.markdown("---")
st.subheader("🧠 Detecção de Padrão de Reescreta Atual")

if len(linhas) >= 2:
    linha_atual = linhas[0]  # Linha mais recente (primeira linha)
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
                    st.markdown("✅" if cores_opostas(a, b) or "🟡" in [a, b] else "❌")
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
    sugestoes_corretas = sum(1 for p in padroes_reescrita 
                            if p["sugestao"] == p["linha_atual"][0] if len(p["linha_atual"]) > 0 else False)
    
    st.write(f"**Total de padrões detectados:** {total_padroes}")
    st.write(f"**Taxa de acerto das sugestões:** {sugestoes_corretas/total_padroes:.0%}" if total_padroes > 0 else "N/A")
    
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
    
    # Agrupar padrões por linha de referência
    padroes_por_linha = {}
    for padrao in padroes_reescrita:
        chave = tuple(padrao["linha_anterior"])
        if chave not in padroes_por_linha:
            padroes_por_linha[chave] = []
        padroes_por_linha[chave].append(padrao)
    
    # Exibir os padrões mais comuns
    st.write("**Padrões mais frequentes:**")
    for linha_ref, padroes in list(padroes_por_linha.items())[:3]:
        st.write(f"- Linha de referência: {' '.join(linha_ref)}")
        st.write(f"  Padrões detectados: {len(padroes)}")
        st.write(f"  Sugestões mais comuns: {Counter(p['sugestao'] for p in padroes).most_common(1)[0][0]}")

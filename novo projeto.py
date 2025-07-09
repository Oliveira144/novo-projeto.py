import streamlit as st
from collections import Counter

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

def padrao_reescrito(linha1, linha2):
    """Detecta se linha1 é uma reescrita de linha2 com cores invertidas"""
    if len(linha1) != len(linha2):
        return False
    
    for a, b in zip(linha1, linha2):
        # Se ambos forem iguais, não é reescrita
        if a == b and a != "🟡":
            return False
            
        # Se forem cores diferentes mas não opostas
        if a != b and a != "🟡" and b != "🟡" and not cores_opostas(a, b):
            return False
            
    return True

def detectar_padrao_reescrita(historico_linhas):
    """Analisa o histórico para encontrar padrões de reescrita entre linhas CONSECUTIVAS"""
    padroes = []
    linhas_completas = [linha for linha in historico_linhas if len(linha) == RESULTADOS_POR_LINHA]
    
    if len(linhas_completas) < 2:
        return padroes
    
    # Compara linhas consecutivas (n e n-1)
    for i in range(1, len(linhas_completas)):
        linha_atual = linhas_completas[i]      # Linha mais recente na comparação
        linha_anterior = linhas_completas[i-1]  # Linha imediatamente anterior
        
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

# Exibir histórico simplificado
st.markdown("---")
st.subheader(f"📋 Histórico de Jogadas ({RESULTADOS_POR_LINHA} por linha)")

for idx, linha in enumerate(linhas, 1):
    # Verificar se esta linha está em um padrão detectado
    em_padrao = any(linha == padrao["linha_atual"] for padrao in padroes_reescrita)
    
    if em_padrao:
        padrao_correspondente = next((p for p in padroes_reescrita if p["linha_atual"] == linha), None)
        # Exibição simplificada sem HTML complexo
        st.success(f"**Linha {idx} (Padrão Detectado):** " + " ".join(linha))
        st.info(f"🎯 **Sugestão:** {padrao_correspondente['sugestao']}")
    else:
        st.markdown(f"**Linha {idx}:** " + " ".join(linha))

# Análise de padrão reescrito em tempo real
st.markdown("---")
st.subheader("🧠 Detecção de Padrão de Reescreta Atual")

if len(linhas) >= 2:
    linha_atual = linhas[0]
    linha_anterior = linhas[1]
    
    # Verificar se temos linhas completas para análise
    if len(linha_atual) == RESULTADOS_POR_LINHA and len(linha_anterior) == RESULTADOS_POR_LINHA:
        if padrao_reescrito(linha_atual, linha_anterior):
            # Determinar sugestão com base no último elemento da linha atual
            ultimo_elemento = linha_atual[-1]
            sugestao = "🔵" if ultimo_elemento == "🔴" else "🔴" if ultimo_elemento == "🔵" else "🟡"
            
            st.success(f"""
            🔁 **PADRÃO DETECTADO! Reescreta confirmada entre Linha 1 e Linha 2**
            
            **Linha 1 (Atual):** {" ".join(linha_atual)}
            **Linha 2 (Anterior):** {" ".join(linha_anterior)}
            
            🎯 **Sugestão de Entrada:** {sugestao}
            """)
            
            # Mostrar visualização detalhada do padrão
            st.subheader("🔍 Comparação Posicional")
            cols = st.columns(RESULTADOS_POR_LINHA)
            for i, (a, b) in enumerate(zip(linha_atual, linha_anterior)):
                with cols[i]:
                    # Determinar status da comparação
                    if a == "🟡" or b == "🟡":
                        status = "🟡 Empate"
                        cor = "gray"
                    elif cores_opostas(a, b):
                        status = "✓ Opostos"
                        cor = "green"
                    else:
                        status = "✗ Iguais"
                        cor = "red"
                    
                    st.markdown(f"**Posição {i+1}**")
                    st.markdown(f"{a} → {b}")
                    st.markdown(f":{cor}[{status}]")
        else:
            st.error("""
            ⚠️ **Padrão não detectado!** 
            
            Possíveis razões:
            1. As linhas não são opostas posição por posição
            2. Muitos empates interferindo na comparação
            3. Padrão não se encaixa na definição de reescrita
            """)
    else:
        st.warning(f"⚠️ Complete ambas as linhas com {RESULTADOS_POR_LINHA} jogadas para análise")
else:
    st.warning("⚠️ Registre pelo menos 2 linhas completas para análise de padrões")

# Estatísticas de padrões detectados
if padroes_reescrita:
    st.markdown("---")
    st.subheader("📈 Estatísticas de Padrões Detectados")
    
    total_padroes = len(padroes_reescrita)
    st.write(f"**Total de padrões detectados:** {total_padroes}")
    
    # Mostrar últimos padrões detectados
    st.write("**Últimos padrões detectados:**")
    for padrao in padroes_reescrita[:3]:
        st.write(f"- Linha: {' '.join(padrao['linha_atual'])} | Sugestão: {padrao['sugestao']}")

# Frequência
st.markdown("---")
st.subheader("📊 Frequência de Cores")
contagem = Counter(historico_limitado)
st.write(f"🔴 Casa: {contagem['🔴']} | 🔵 Visitante: {contagem['🔵']} | 🟡 Empate: {contagem['🟡']}")

# Visualização de tendências
st.markdown("---")
st.subheader("📈 Análise de Tendências")

if len(linhas) > 0:
    # Calcula a porcentagem de cada cor nas últimas 3 linhas completas
    ultimas_jogadas = []
    for linha in linhas[:3]:
        if len(linha) == RESULTADOS_POR_LINHA:
            ultimas_jogadas.extend(linha)
    
    if ultimas_jogadas:
        total = len(ultimas_jogadas)
        contagem_tendencia = Counter(ultimas_jogadas)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            percent_casa = (contagem_tendencia.get("🔴", 0) / total) * 100
            st.metric("🔴 Casa", f"{percent_casa:.1f}%")
        with col2:
            percent_visit = (contagem_tendencia.get("🔵", 0) / total) * 100
            st.metric("🔵 Visitante", f"{percent_visit:.1f}%")
        with col3:
            percent_empate = (contagem_tendencia.get("🟡", 0) / total) * 100
            st.metric("🟡 Empate", f"{percent_empate:.1f}%")
    else:
        st.info("Nenhuma jogada completa registrada nas últimas 3 linhas")
else:
    st.info("Registre jogadas para ver as tendências")

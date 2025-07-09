import streamlit as st
from collections import Counter, defaultdict
import numpy as np
from itertools import combinations

# Inicializa histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# Constantes
RESULTADOS_POR_LINHA = 8
MAX_LINHAS_HISTORICO = 80
MAX_JOGADAS = RESULTADOS_POR_LINHA * MAX_LINHAS_HISTORICO

# Funções de lógica aprimoradas
def cores_opostas(c1, c2):
    return (c1 == "🔴" and c2 == "🔵") or (c1 == "🔵" and c2 == "🔴")

def analisar_padrao_reescrito(linha1, linha2, limite=0.7):
    """Analisa padrão de reescrita com diagnóstico detalhado e filtros"""
    resultado = {
        "match": False,
        "diferencas": [],
        "porcentagem_match": 0,
        "total_comparacoes": 0,
        "matches": 0,
        "tipo_padrao": None,
        "confianca": 0
    }
    
    if len(linha1) != len(linha2):
        return resultado
    
    total_posicoes = 0
    matches = 0
    diferencas = []
    
    for pos, (a, b) in enumerate(zip(linha1, linha2)):
        if a == "🟡" or b == "🟡":
            continue
            
        total_posicoes += 1
        sao_opostas = cores_opostas(a, b)
        
        if sao_opostas:
            matches += 1
        else:
            diferencas.append({
                "posicao": pos + 1,
                "valor1": a,
                "valor2": b,
                "opostas": False
            })
    
    porcentagem = matches / total_posicoes if total_posicoes > 0 else 0
    
    # Classificação do padrão
    tipo_padrao = None
    confianca = 0
    
    if porcentagem >= 0.9:
        tipo_padrao = "Forte"
        confianca = 95
    elif porcentagem >= 0.75:
        tipo_padrao = "Moderado"
        confianca = 80
    elif porcentagem >= limite:
        tipo_padrao = "Fraco"
        confianca = 65
    
    # Atualiza resultado
    resultado.update({
        "total_comparacoes": total_posicoes,
        "matches": matches,
        "porcentagem_match": porcentagem,
        "match": porcentagem >= limite,
        "tipo_padrao": tipo_padrao,
        "confianca": confianca,
        "diferencas": diferencas
    })
    
    return resultado

def analisar_colunas(linhas_completas, limite_confianca=70):
    """Realiza varredura avançada em todas as colunas"""
    padroes_detectados = []
    
    if len(linhas_completas) < 3:
        return padroes_detectados
    
    # Cria matriz de colunas com as últimas 5 linhas para melhor análise
    matriz = linhas_completas[:5]
    colunas = list(zip(*matriz))
    total_colunas = len(colunas)
    
    # Análise de sequência temporal por coluna
    padroes_sequencia = []
    for col_idx, coluna in enumerate(colunas):
        # Analisa sequência de cores na coluna
        sequencia = list(coluna)
        padrao_seq = detectar_sequencia(sequencia)
        if padrao_seq:
            padroes_sequencia.append({
                "coluna": col_idx,
                "padrao": padrao_seq,
                "tipo": "sequencia",
                "confianca": calcular_confianca_sequencia(padrao_seq)
            })
    
    # Combina padrões de sequência com padrões de reescrita
    padroes_combinados = []
    
    # Varredura de padrões entre colunas
    for i, j in combinations(range(total_colunas), 2):
        analise = analisar_padrao_reescrito(colunas[i], colunas[j])
        
        if analise["match"] and analise["confianca"] >= limite_confianca:
            # Verifica se há coluna após a coluna de referência
            if i + 1 < total_colunas:
                coluna_apos_ref = colunas[i + 1]
                elemento_comum = Counter(coluna_apos_ref).most_common(1)[0][0]
                
                # Sugestão baseada em lógica aprimorada
                if elemento_comum == "🔴":
                    sugestao = "🔵"
                    logica = "Oposto ao comum após referência (🔴→🔵)"
                elif elemento_comum == "🔵":
                    sugestao = "🔴"
                    logica = "Oposto ao comum após referência (🔵→🔴)"
                else:
                    sugestao = "🟡"
                    logica = "Empate detectado após referência"
                
                padroes_combinados.append({
                    "tipo": "reescrita",
                    "coluna_ref": i,
                    "coluna_atual": j,
                    "confianca": analise["confianca"],
                    "sugestao": sugestao,
                    "elemento_referencia": elemento_comum,
                    "logica": logica,
                    "detalhes": analise
                })
    
    # Combina com padrões de sequência
    for seq in padroes_sequencia:
        if seq["confianca"] >= limite_confianca:
            # Lógica para sugestão baseada em sequência
            ultimo = seq["padrao"][-1]
            if ultimo == "🔴":
                sugestao = "🔵"
                logica = "Sequência: oposto ao último elemento"
            elif ultimo == "🔵":
                sugestao = "🔴"
                logica = "Sequência: oposto ao último elemento"
            else:
                sugestao = "🟡"
                logica = "Sequência: empate detectado"
            
            padroes_combinados.append({
                "tipo": "sequencia",
                "coluna": seq["coluna"],
                "confianca": seq["confianca"],
                "sugestao": sugestao,
                "logica": logica,
                "padrao": seq["padrao"]
            })
    
    # Filtra e classifica os padrões
    padroes_combinados = sorted(padroes_combinados, key=lambda x: x["confianca"], reverse=True)
    
    # Agrupa sugestões similares
    sugestoes_agrupadas = defaultdict(list)
    for padrao in padroes_combinados:
        chave = (padrao["sugestao"], padrao["logica"])
        sugestoes_agrupadas[chave].append(padrao["confianca"])
    
    # Cria resultado final consolidado
    for (sugestao, logica), confiancas in sugestoes_agrupadas.items():
        confianca_media = np.mean(confiancas)
        padroes_detectados.append({
            "sugestao": sugestao,
            "confianca": confianca_media,
            "logica": logica,
            "padroes_similares": len(confiancas)
        })
    
    return padroes_detectados

def detectar_sequencia(sequencia):
    """Detecta padrões em sequências de cores"""
    if len(sequencia) < 3:
        return None
    
    # Verifica padrões simples
    ultimos = sequencia[-3:]
    
    # Padrão alternado
    if all(cores_opostas(ultimos[i], ultimos[i+1]) for i in range(2)):
        return "alternado"
    
    # Padrão repetido
    if len(set(ultimos)) == 1:
        return "repetido"
    
    # Padrão específico
    if ultimos == ["🔴", "🔵", "🔴"]:
        return "🔴🔵🔴"
    elif ultimos == ["🔵", "🔴", "🔵"]:
        return "🔵🔴🔵"
    
    return None

def calcular_confianca_sequencia(padrao):
    """Calcula confiança baseada no tipo de padrão"""
    confianca = {
        "alternado": 85,
        "repetido": 90,
        "🔴🔵🔴": 80,
        "🔵🔴🔵": 80
    }
    return confianca.get(padrao, 70)

# Funções de UI e manipulação de dados mantidas...

# =================================================================
# INTERFACE DO USUÁRIO ATUALIZADA
# =================================================================

# Configuração visual
st.set_page_config(page_title="FS Análise Pro+", layout="centered")

st.title("📊 FS Análise Pro+")
st.caption("Sistema avançado de detecção de padrões para Football Studio Live")

# Botões de entrada
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔴 Casa", use_container_width=True, key="casa"): inserir("🔴")
with col2:
    if st.button("🔵 Visitante", use_container_width=True, key="visit"): inserir("🔵")
with col3:
    if st.button("🟡 Empate", use_container_width=True, key="empate"): inserir("🟡")

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

# Executa análises com limite de confiança ajustável
limite_confianca = st.sidebar.slider("Limite de Confiança (%)", 50, 95, 70, 5)
padroes_colunas = analisar_colunas(linhas_completas, limite_confianca)

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
st.write(f"- [ ] Casa: {contagem['🔴']}  \n- [ ] Visitante: {contagem['🔵']}  \n- [ ] Empate: {contagem['🟡']}")

# Análise de padrão reescrito aprimorada
st.markdown("---")
st.subheader("🧠 Detecção de Padrão Reescrito")

if len(linhas_completas) >= 2:
    linha_recente = linhas_completas[0]
    linha_anterior = linhas_completas[1]

    analise = analisar_padrao_reescrito(linha_recente, linha_anterior)
    
    if analise["match"]:
        # Sugestão baseada em análise mais robusta
        ultimas_3 = [linhas_completas[i] for i in range(min(3, len(linhas_completas)))]
        tendencia = Counter([x for sublist in ultimas_3 for x in sublist])
        
        if tendencia["🔴"] > tendencia["🔵"] + 2:
            jogada_sugerida = "🔵"
            logica = "Tendência de 🔴 (jogar oposto)"
        elif tendencia["🔵"] > tendencia["🔴"] + 2:
            jogada_sugerida = "🔴"
            logica = "Tendência de 🔵 (jogar oposto)"
        else:
            jogada_sugerida = "🟡" if linha_recente[-1] != "🟡" else "🔴"
            logica = "Padrão equilibrado (jogar seguro)"
        
        st.success(f"""
        ### 🔍 **Padrão {analise['tipo_padrao']} Detectado** ({analise['porcentagem_match']:.0%})
        📊 **Confiança:** {analise['confianca']}%  
        🎯 **Sugestão:** Jogar {jogada_sugerida}  
        🧠 **Lógica:** {logica}
        """)
        
        # Gráfico de tendência
        st.subheader("📈 Tendência Recente")
        cols = st.columns(3)
        cols[0].metric("🔴 Casa", tendencia["🔴"])
        cols[1].metric("🔵 Visitante", tendencia["🔵"])
        cols[2].metric("🟡 Empate", tendencia["🟡"])
        
    else:
        st.error(f"⚠️ **Padrão não detectado** (correspondência: {analise['porcentagem_match']:.0%})")
        
        # Sugestão alternativa baseada em frequência
        st.subheader("💡 Sugestão por Frequência")
        freq_total = sum(contagem.values())
        if freq_total > 0:
            percent_red = contagem["🔴"] / freq_total
            percent_blue = contagem["🔵"] / freq_total
            
            if abs(percent_red - percent_blue) > 0.15:  # Diferença significativa
                sugestao = "🔵" if percent_red > percent_blue else "🔴"
                st.warning(f"Diferença de frequência detectada: Sugerimos jogar {sugestao}")
            else:
                st.info("Frequências equilibradas - Sugerimos 🟡 Empate")
    
    # Visualização da comparação (mantida da versão anterior)
    # ... (código de visualização permanece o mesmo)

# Seção de sugestões aprimorada
st.markdown("---")
st.subheader("🎯 Sugestões Inteligentes")

if padroes_colunas:
    # Agrupa por tipo de sugestão
    sugestoes_agrupadas = defaultdict(list)
    for padrao in padroes_colunas:
        sugestoes_agrupadas[padrao["sugestao"]].append((padrao["confianca"], padrao["logica"]))
    
    # Exibe as melhores sugestões
    st.success("### 🍟️ Melhores Sugestões")
    
    for sugestao, dados in sugestoes_agrupadas.items():
        confiancas = [d[0] for d in dados]
        logicas = [d[1] for d in dados]
        confianca_media = np.mean(confiancas)
        
        # Mostra apenas sugestões com alta confiança
        if confianca_media >= limite_confianca:
            st.markdown(f"""
            **Jogar {sugestao}**  
            🔍 {max(logicas, key=len)}  
            📊 **{confianca_media:.1f}%** de confiança  
            🎯 **Padrões similares:** {len(dados)}  
            """)
            
            # Botão para jogar diretamente
            if st.button(f"Jogar {sugestao}", key=f"btn_{sugestao}"):
                inserir(sugestao)
                st.experimental_rerun()
            
            st.markdown("---")
    
    # Detalhes dos padrões
    with st.expander("🔍 Detalhes dos Padrões Detectados"):
        for i, padrao in enumerate(padroes_colunas, 1):
            if padrao["confianca"] >= limite_confianca:
                st.markdown(f"""
                ### Padrão {i} ({padrao['tipo'] if 'tipo' in padrao else 'reescrita'})
                - 🎯 **Sugestão:** {padrao["sugestao"]}
                - 📊 **Confiança:** {padrao["confianca"]:.1f}%
                - 🧠 **Lógica:** {padrao["logica"]}
                """)
                if "detalhes" in padrao:
                    st.write(f"🔍 **Match:** {padrao['detalhes']['porcentagem_match']:.0%}")
                st.markdown("---")

# Análise de tendências aprimorada
st.markdown("---")
st.subheader("📈 Análise de Tendências Avançada")

if len(linhas_completas) > 0:
    # Calcula a porcentagem de cada cor nas últimas 5 linhas
    ultimas_jogadas = [item for sublist in linhas_completas[:5] for item in sublist]
    if ultimas_jogadas:
        contagem_tendencia = Counter(ultimas_jogadas)
        total = len(ultimas_jogadas)
        
        # Calcula desvio padrão para determinar volatilidade
        valores = [1 if x == "🔴" else -1 if x == "🔵" else 0 for x in ultimas_jogadas]
        volatilidade = np.std(valores)
        
        st.write("**Distribuição nas últimas jogadas:**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            percent_casa = (contagem_tendencia["🔴"] / total) * 100
            st.metric("🔴 Casa", f"{percent_casa:.1f}%")
        
        with col2:
            percent_visit = (contagem_tendencia["🔵"] / total) * 100
            st.metric("🔵 Visitante", f"{percent_visit:.1f}%")
        
        with col3:
            percent_empate = (contagem_tendencia["🟡"] / total) * 100
            st.metric("🟡 Empate", f"{percent_empate:.1f}%")
        
        with col4:
            st.metric("📊 Volatilidade", f"{volatilidade:.2f}", 
                     help="Medida de variação entre resultados (maior = mais imprevisível)")
        
        # Sugestão baseada em análise de tendência
        st.subheader("📌 Sugestão por Tendência")
        
        if volatilidade < 0.5:
            st.success("Baixa volatilidade - Padrões estáveis detectados")
        elif volatilidade > 1.0:
            st.warning("Alta volatilidade - Resultados imprevisíveis")
        
        if percent_casa > 50:
            st.warning(f"Tendência forte para 🔴 Casa ({percent_casa:.1f}%) - Sugerimos 🔵 Visitante")
        elif percent_visit > 50:
            st.warning(f"Tendência forte para 🔵 Visitante ({percent_visit:.1f}%) - Sugerimos 🔴 Casa")
        else:
            st.info("Nenhuma tendência dominante detectada - Jogue com cautela")

# Restante do código mantido...

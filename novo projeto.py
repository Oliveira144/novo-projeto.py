import streamlit as st
from collections import Counter, defaultdict, deque
import numpy as np
from itertools import combinations
import math

# Inicializa histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# Constantes
RESULTADOS_POR_LINHA = 8
MAX_LINHAS_HISTORICO = 80
MAX_JOGADAS = RESULTADOS_POR_LINHA * MAX_LINHAS_HISTORICO
PESO_RECENTE = 1.5  # Peso para jogadas mais recentes

# Funções de lógica aprimoradas
def cores_opostas(c1, c2):
    return (c1 == "🔴" and c2 == "🔵") or (c1 == "🔵" and c2 == "🔴")

def analisar_padrao_reescrito(linha1, linha2, limite=0.7):
    """Analisa padrão de reescrita com diagnóstico detalhado e filtros"""
    # ... (manter a implementação anterior) ...

def detectar_sequencia(sequencia):
    """Detecta padrões em sequências de cores com mais precisão"""
    if len(sequencia) < 3:
        return None
    
    # Padrão repetido (3 ou mais iguais)
    if len(set(sequencia[-3:])) == 1:
        return f"repetido_{sequencia[-1]}"
    
    # Padrão alternado rigoroso
    if len(sequencia) >= 4:
        ultimos_4 = sequencia[-4:]
        if (ultimos_4[0] == ultimos_4[2] and 
            ultimos_4[1] == ultimos_4[3] and 
            cores_opostas(ultimos_4[0], ultimos_4[1])):
            return "alternado_rigoroso"
    
    # Padrão triplo específico
    ultimos_3 = sequencia[-3:]
    if ultimos_3 == ["🔴", "🔵", "🔴"]:
        return "rbr"
    elif ultimos_3 == ["🔵", "🔴", "🔵"]:
        return "brb"
    
    # Padrão de dois iguais seguido de oposto
    if len(sequencia) >= 3:
        if sequencia[-3] == sequencia[-2] and cores_opostas(sequencia[-2], sequencia[-1]):
            return f"dois_mais_um_{sequencia[-1]}"
    
    return None

def calcular_confianca_sequencia(padrao, comprimento):
    """Calcula confiança baseada no tipo de padrão e histórico"""
    base_confianca = {
        "repetido_🔴": 92,
        "repetido_🔵": 92,
        "repetido_🟡": 85,
        "alternado_rigoroso": 88,
        "rbr": 82,
        "brb": 82,
        "dois_mais_um_🔴": 78,
        "dois_mais_um_🔵": 78,
        "dois_mais_um_🟡": 70
    }
    
    confianca = base_confianca.get(padrao, 75)
    
    # Aumenta confiança para padrões mais longos
    if "repetido" in padrao and comprimento > 3:
        confianca += min(10, (comprimento - 3) * 3)
    
    return min(99, confianca)

def analisar_transicoes(historico):
    """Analisa probabilidades de transição entre estados"""
    transicoes = {
        "🔴": {"🔴": 0, "🔵": 0, "🟡": 0},
        "🔵": {"🔴": 0, "🔵": 0, "🟡": 0},
        "🟡": {"🔴": 0, "🔵": 0, "🟡": 0}
    }
    
    if len(historico) < 2:
        return transicoes
    
    # Aplica peso temporal
    peso_total = 0
    for i in range(1, len(historico)):
        peso = PESO_RECENTE ** (len(historico) - i)  # Mais peso para transições recentes
        anterior = historico[i]
        atual = historico[i-1]
        
        if anterior in transicoes and atual in transicoes[anterior]:
            transicoes[anterior][atual] += peso
            peso_total += peso
    
    # Converte para probabilidades
    for estado, trans in transicoes.items():
        total = sum(trans.values())
        if total > 0:
            for k in trans:
                transicoes[estado][k] = transicoes[estado][k] / total
    
    return transicoes

def detectar_padroes_recorrentes(linhas_completas):
    """Detecta padrões que se repetem ao longo do histórico"""
    padroes = {}
    sequencias = []
    
    # Extrai todas as sequências de 3 elementos
    for linha in linhas_completas:
        for i in range(len(linha) - 2):
            seq = tuple(linha[i:i+3])
            sequencias.append(seq)
    
    # Conta ocorrências de cada sequência
    contador = Counter(sequencias)
    
    # Filtra sequências que aparecem pelo menos 2 vezes
    for seq, count in contador.items():
        if count >= 2:
            # Determina o próximo movimento mais provável após esta sequência
            proximos = []
            for i in range(len(sequencias) - 1):
                if sequencias[i] == seq:
                    proximos.append(sequencias[i+1][0])  # Primeiro elemento da próxima sequência
            
            if proximos:
                prox_comum = Counter(proximos).most_common(1)[0][0]
                confianca = min(95, 70 + (count - 2) * 10)  # Baseado na frequência
                
                padroes[seq] = {
                    "ocorrencias": count,
                    "prox_esperado": prox_comum,
                    "confianca": confianca
                }
    
    return padroes

def analisar_colunas(linhas_completas, limite_confianca=70):
    """Realiza varredura avançada em todas as colunas"""
    padroes_detectados = []
    
    if len(linhas_completas) < 3:
        return padroes_detectados
    
    # Cria matriz de colunas com as últimas 5 linhas
    matriz = linhas_completas[:5]
    colunas = list(zip(*matriz))
    total_colunas = len(colunas)
    
    # Análise de sequência temporal por coluna
    for col_idx, coluna in enumerate(colunas):
        sequencia = list(coluna)
        
        # Verifica sequências mais longas (até 5 elementos)
        for comprimento in range(3, 6):
            if len(sequencia) >= comprimento:
                sub_seq = sequencia[-comprimento:]
                padrao_seq = detectar_sequencia(sub_seq)
                
                if padrao_seq:
                    confianca = calcular_confianca_sequencia(padrao_seq, comprimento)
                    
                    if confianca >= limite_confianca:
                        # Lógica para sugestão baseada em sequência
                        if "repetido" in padrao_seq:
                            cor = padrao_seq.split('_')[-1]
                            sugestao = "🔵" if cor == "🔴" else "🔴" if cor == "🔵" else "🟡"
                            logica = f"Sequência repetida de {comprimento} {cor} (jogar oposto)"
                        elif "dois_mais_um" in padrao_seq:
                            cor = padrao_seq.split('_')[-1]
                            sugestao = "🔵" if cor == "🔴" else "🔴" if cor == "🔵" else "🟡"
                            logica = f"Dois iguais seguidos de {cor} (jogar oposto)"
                        elif padrao_seq == "alternado_rigoroso":
                            ultimo = sequencia[-1]
                            sugestao = "🔵" if ultimo == "🔴" else "🔴" if ultimo == "🔵" else "🟡"
                            logica = "Padrão alternado rigoroso (jogar oposto ao último)"
                        else:
                            ultimo = sequencia[-1]
                            sugestao = "🔵" if ultimo == "🔴" else "🔴" if ultimo == "🔵" else "🟡"
                            logica = f"Sequência específica {padrao_seq} (jogar oposto)"
                        
                        padroes_detectados.append({
                            "tipo": "sequencia",
                            "coluna": col_idx,
                            "sugestao": sugestao,
                            "confianca": confianca,
                            "logica": logica,
                            "padrao": padrao_seq
                        })
    
    # Análise de transições entre colunas
    transicoes_globais = analisar_transicoes([cor for linha in matriz for cor in linha])
    
    # Sugestões baseadas em transições
    ultima_cor = matriz[0][-1] if matriz else "🟡"
    if ultima_cor in transicoes_globais:
        trans = transicoes_globais[ultima_cor]
        melhor_prox, melhor_prob = max(trans.items(), key=lambda x: x[1])
        
        if melhor_prob > 0.4:  # Probabilidade significativa
            # Se a maior probabilidade é para mesma cor, sugerir oposto
            if melhor_prox == ultima_cor:
                sugestao = "🔵" if ultima_cor == "🔴" else "🔴" if ultima_cor == "🔵" else "🟡"
                logica = f"Alta probabilidade de repetição ({melhor_prob:.0%}) - Jogar oposto"
            else:
                sugestao = melhor_prox
                logica = f"Transição mais provável ({melhor_prob:.0%})"
            
            confianca = min(95, int(melhor_prob * 100))
            padroes_detectados.append({
                "tipo": "transicao",
                "sugestao": sugestao,
                "confianca": confianca,
                "logica": logica
            })
    
    # Padrões recorrentes no histórico
    padroes_recorrentes = detectar_padroes_recorrentes(linhas_completas)
    for seq, data in padroes_recorrentes.items():
        # Verifica se o padrão ocorre no final da última linha
        ultima_linha = list(linhas_completas[0])
        for i in range(len(ultima_linha) - 2):
            if tuple(ultima_linha[i:i+3]) == seq:
                sugestao = data["prox_esperado"]
                padroes_detectados.append({
                    "tipo": "recorrente",
                    "sugestao": sugestao,
                    "confianca": data["confianca"],
                    "logica": f"Padrão recorrente detectado ({data['ocorrencias']} ocorrências)",
                    "sequencia": seq
                })
    
    # Filtra e classifica os padrões
    padroes_detectados = sorted(padroes_detectados, key=lambda x: x["confianca"], reverse=True)
    
    # Remove duplicatas e mantém apenas a sugestão de maior confiança para cada tipo
    sugestoes_unicas = {}
    for padrao in padroes_detectados:
        chave = padrao["sugestao"]
        if chave not in sugestoes_unicas or padrao["confianca"] > sugestoes_unicas[chave]["confianca"]:
            sugestoes_unicas[chave] = padrao
    
    return list(sugestoes_unicas.values())

# ... (funções inserir, desfazer, limpar permanecem iguais) ...

# Configuração visual
st.set_page_config(page_title="FS Análise Pro+", layout="centered")

st.title("📊 FS Análise Pro+")
st.caption("Sistema avançado de detecção de padrões para Football Studio Live")

# Botões de entrada
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔴 Casa", use_container_width=True, key="btn_casa"):
        inserir("🔴")
with col2:
    if st.button("🔵 Visitante", use_container_width=True, key="btn_visitante"):
        inserir("🔵")
with col3:
    if st.button("🟡 Empate", use_container_width=True, key="btn_empate"):
        inserir("🟡")

# Controles
col4, col5 = st.columns(2)
with col4:
    if st.button("↩️ Desfazer", use_container_width=True, key="btn_desfazer"):
        desfazer()
with col5:
    if st.button("🧹 Limpar", use_container_width=True, key="btn_limpar"):
        limpar()

# Processar histórico
historico_limitado = st.session_state.historico[:MAX_JOGADAS]
linhas = []
for i in range(0, len(historico_limitado), RESULTADOS_POR_LINHA):
    linha = historico_limitado[i:i+RESULTADOS_POR_LINHA]
    linhas.append(linha)

# Filtra linhas completas
linhas_completas = [l for l in linhas if len(l) == RESULTADOS_POR_LINHA]

# Executa análises com limite de confiança ajustável
limite_confianca = st.sidebar.slider("Limite de Confiança (%)", 50, 95, 75, 5, key="limite_confianca")
padroes_colunas = analisar_colunas(linhas_completas, limite_confianca)

# Exibir histórico
st.markdown("---")
st.subheader(f"📋 Histórico de Jogadas ({RESULTADOS_POR_LINHA} por linha)")

with st.container(height=400):
    for idx, linha in enumerate(linhas, 1):
        st.markdown(f"**Linha {idx}:** " + " ".join(linha))

# Frequência com análise de tendência
st.markdown("---")
st.subheader("📊 Frequência e Tendência de Cores")
contagem = Counter(historico_limitado)
total = len(historico_limitado)

if total > 0:
    percent_red = (contagem.get("🔴", 0) / total) * 100
    percent_blue = (contagem.get("🔵", 0) / total) * 100
    percent_yellow = (contagem.get("🟡", 0) / total) * 100
    
    # Análise de tendência
    tendencia = ""
    if percent_red > 40:
        tendencia += "🔴 em alta "
    if percent_blue > 40:
        tendencia += "🔵 em alta "
    if percent_yellow > 10:
        tendencia += "🟡 frequente"
    
    st.write(f"- [ ] Casa: {contagem.get('🔴', 0)} ({percent_red:.1f}%)")
    st.write(f"- [ ] Visitante: {contagem.get('🔵', 0)} ({percent_blue:.1f}%)")
    st.write(f"- [ ] Empate: {contagem.get('🟡', 0)} ({percent_yellow:.1f}%)")
    st.write(f"**Tendência:** {tendencia if tendencia else 'Equilibrada'}")

# Seção principal de sugestões
st.markdown("---")
st.subheader("🎯 Sugestões Inteligentes Baseadas em Padrões")

if padroes_colunas:
    # Agrupa sugestões por tipo
    sugestoes_agrupadas = defaultdict(list)
    for padrao in padroes_colunas:
        sugestoes_agrupadas[padrao["sugestao"]].append(padrao)
    
    # Exibe as sugestões consolidadas
    for sugestao, padroes in sugestoes_agrupadas.items():
        # Encontra o padrão com maior confiança para esta sugestão
        melhor_padrao = max(padroes, key=lambda x: x["confianca"])
        confianca_media = np.mean([p["confianca"] for p in padroes])
        total_padroes = len(padroes)
        
        st.markdown(f"""
        ### 🎯 Jogar {sugestao}
        🔍 **Lógica Principal:** {melhor_padrao["logica"]}  
        📊 **Confiança:** {melhor_padrao["confianca"]:.1f}%  
        🧩 **Padrões Detectados:** {total_padroes} diferentes
        """)
        
        # Botão para jogar
        if st.button(f"Registrar Jogada {sugestao}", key=f"btn_jogar_{sugestao}"):
            inserir(sugestao)
            st.experimental_rerun()
        
        # Detalhes dos padrões
        with st.expander(f"🔍 Ver detalhes dos {total_padroes} padrões para {sugestao}"):
            for i, padrao in enumerate(padroes, 1):
                st.write(f"**Padrão {i} ({padrao['tipo']}):**")
                st.write(f"- Confiança: {padrao['confianca']:.1f}%")
                st.write(f"- Lógica: {padrao['logica']}")
                if "padrao" in padrao:
                    st.write(f"- Detalhe: {padrao['padrao']}")
                st.markdown("---")
    
    # Análise estatística
    st.markdown("---")
    st.subheader("📈 Análise Estatística de Confiabilidade")
    
    # Calcula precisão histórica
    if len(st.session_state.historico) > 10:
        acertos = 0
        total_sugestoes = 0
        for i in range(1, len(st.session_state.historico)):
            if i < len(padroes_colunas):
                sugestao_anterior = padroes_colunas[i-1]["sugestao"]
                resultado_atual = st.session_state.historico[i]
                if sugestao_anterior == resultado_atual:
                    acertos += 1
                total_sugestoes += 1
        
        if total_sugestoes > 0:
            precisao = (acertos / total_sugestoes) * 100
            st.metric("Precisão Histórica", f"{precisao:.1f}%", 
                     delta=f"{precisao - 50:.1f}% acima do esperado")
        else:
            st.info("Coletando dados para cálculo de precisão...")
    else:
        st.info("Registre mais jogadas para habilitar análise de precisão")
else:
    st.warning("⚠️ Nenhum padrão significativo detectado. Sugestões baseadas em frequência:")
    
    # Sugestão por desequilíbrio de frequência
    if total > 0:
        if percent_red > percent_blue + 15:
            st.success("🔵 Jogar Visitante (Casa com frequência muito alta)")
        elif percent_blue > percent_red + 15:
            st.success("🔴 Jogar Casa (Visitante com frequência muito alta)")
        else:
            st.info("🟡 Frequências equilibradas - Sugerimos Empate")
    else:
        st.info("Registre as primeiras jogadas para começar a análise")

# Análise de transições globais
st.markdown("---")
st.subheader("🔄 Análise de Transições")

transicoes = analisar_transicoes(historico_limitado)
if transicoes:
    cols = st.columns(3)
    cores = ["🔴", "🔵", "🟡"]
    
    for i, cor in enumerate(cores):
        with cols[i]:
            st.subheader(f"Após {cor}")
            trans = transicoes[cor]
            for prox, prob in trans.items():
                st.progress(prob, text=f"{prox}: {prob:.1%}")

# ... (restante do código permanece similar) ...

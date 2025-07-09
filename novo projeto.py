import streamlit as st
from collections import Counter, defaultdict
import numpy as np
import pandas as pd
import math

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

def analisar_padroes_avancados(historico, linhas_completas):
    """Analisa padrões com múltiplas técnicas combinadas"""
    resultados = []
    
    # 1. Análise de sequências imediatas
    if len(historico) >= 3:
        ultimos = historico[:3]
        
        # Padrão de repetição
        if ultimos[0] == ultimos[1]:
            sugestao = "🔵" if ultimos[0] == "🔴" else "🔴" if ultimos[0] == "🔵" else "🟡"
            confianca = 85
            resultados.append({
                "sugestao": sugestao,
                "confianca": confianca,
                "logica": f"Repetição de {ultimos[0]} (jogar oposto)",
                "tipo": "sequencia"
            })
        
        # Padrão alternado
        if cores_opostas(ultimos[0], ultimos[1]) and cores_opostas(ultimos[1], ultimos[2]):
            sugestao = "🔵" if ultimos[2] == "🔴" else "🔴" if ultimos[2] == "🔵" else "🟡"
            confianca = 80
            resultados.append({
                "sugestao": sugestao,
                "confianca": confianca,
                "logica": "Sequência alternada (jogar oposto)",
                "tipo": "sequencia"
            })
    
    # 2. Análise de frequência ponderada
    if historico:
        contagem = Counter(historico)
        total = len(historico)
        pesos = [1.5**i for i in range(len(historico))]  # Peso maior para resultados recentes
        
        freq_ponderada = defaultdict(float)
        for i, cor in enumerate(historico):
            freq_ponderada[cor] += pesos[i]
        
        soma_pesos = sum(pesos)
        for cor in freq_ponderada:
            freq_ponderada[cor] /= soma_pesos
        
        # Sugestão baseada em frequência ponderada
        cor_mais_frequente = max(freq_ponderada, key=freq_ponderada.get)
        if freq_ponderada[cor_mais_frequente] > 0.4:  # Limite de significância
            sugestao = "🔵" if cor_mais_frequente == "🔴" else "🔴" if cor_mais_frequente == "🔵" else "🟡"
            confianca = min(90, int(freq_ponderada[cor_mais_frequente] * 100))
            resultados.append({
                "sugestao": sugestao,
                "confianca": confianca,
                "logica": f"Frequência alta de {cor_mais_frequente} (jogar oposto)",
                "tipo": "frequencia"
            })
    
    # 3. Análise de linhas completas (reescrita)
    if len(linhas_completas) >= 2:
        linha_atual = linhas_completas[0]
        linha_anterior = linhas_completas[1]
        
        matches = 0
        comparacoes = 0
        for a, b in zip(linha_atual, linha_anterior):
            if a != "🟡" and b != "🟡":
                comparacoes += 1
                if cores_opostas(a, b):
                    matches += 1
        
        if comparacoes > 0:
            porcentagem = matches / comparacoes
            if porcentagem >= 0.7:
                sugestao = "🔵" if linha_atual[-1] == "🔴" else "🔴" if linha_atual[-1] == "🔵" else "🟡"
                confianca = min(95, int(porcentagem * 100))
                resultados.append({
                    "sugestao": sugestao,
                    "confianca": confianca,
                    "logica": f"Padrão reescrito detectado ({int(porcentagem*100)}%)",
                    "tipo": "reescrita"
                })
    
    # 4. Análise de colunas verticais
    if len(linhas_completas) >= 3:
        colunas = list(zip(*linhas_completas[:3]))
        
        for idx, coluna in enumerate(colunas):
            if len(coluna) >= 3:
                # Padrão de repetição vertical
                if coluna[0] == coluna[1] == coluna[2]:
                    sugestao = "🔵" if coluna[0] == "🔴" else "🔴" if coluna[0] == "🔵" else "🟡"
                    resultados.append({
                        "sugestao": sugestao,
                        "confianca": 88,
                        "logica": f"Repetição vertical na coluna {idx+1}",
                        "tipo": "coluna"
                    })
                
                # Padrão alternado vertical
                if (cores_opostas(coluna[0], coluna[1]) and 
                    cores_opostas(coluna[1], coluna[2])):
                    sugestao = "🔵" if coluna[2] == "🔴" else "🔴" if coluna[2] == "🔵" else "🟡"
                    resultados.append({
                        "sugestao": sugestao,
                        "confianca": 82,
                        "logica": f"Alternância vertical na coluna {idx+1}",
                        "tipo": "coluna"
                    })
    
    # 5. Análise de tendência de longo prazo
    if len(historico) > 20:
        tamanho_janela = min(20, len(historico))
        janela_recente = historico[:tamanho_janela]
        janela_anterior = historico[tamanho_janela:2*tamanho_janela]
        
        if janela_anterior:
            contagem_recente = Counter(janela_recente)
            contagem_anterior = Counter(janela_anterior)
            
            mudanca_vermelho = contagem_recente.get("🔴", 0) - contagem_anterior.get("🔴", 0)
            mudanca_azul = contagem_recente.get("🔵", 0) - contagem_anterior.get("🔵", 0)
            
            if abs(mudanca_vermelho) > 5 or abs(mudanca_azul) > 5:
                if mudanca_vermelho > mudanca_azul:
                    sugestao = "🔴"
                    logica = "Tendência crescente para Casa"
                else:
                    sugestao = "🔵"
                    logica = "Tendência crescente para Visitante"
                
                confianca = min(85, 70 + abs(mudanca_vermelho - mudanca_azul))
                resultados.append({
                    "sugestao": sugestao,
                    "confianca": confianca,
                    "logica": logica,
                    "tipo": "tendencia"
                })
    
    # Consolida resultados
    resultados_consolidados = []
    if resultados:
        # Agrupa por sugestão
        sugestoes_agrupadas = defaultdict(list)
        for res in resultados:
            sugestoes_agrupadas[res["sugestao"]].append(res)
        
        # Seleciona a melhor confiança para cada sugestão
        for sugestao, grupo in sugestoes_agrupadas.items():
            melhor = max(grupo, key=lambda x: x["confianca"])
            resultados_consolidados.append(melhor)
    
    return resultados_consolidados

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
st.caption("Sistema avançado de detecção de padrões para Football Studio Live")

# Botões de entrada - CORRIGIDO
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

# Executa análises
try:
    padroes_detectados = analisar_padroes_avancados(historico_limitado, linhas_completas)
except Exception as e:
    st.error(f"Erro na análise: {str(e)}")
    padroes_detectados = []

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
total = len(historico_limitado)

if total > 0:
    st.write(f"- 🔴 Casa: {contagem.get('🔴', 0)} ({contagem.get('🔴', 0)/total:.0%})")
    st.write(f"- 🔵 Visitante: {contagem.get('🔵', 0)} ({contagem.get('🔵', 0)/total:.0%})")
    st.write(f"- 🟡 Empate: {contagem.get('🟡', 0)} ({contagem.get('🟡', 0)/total:.0%})")
else:
    st.write("Nenhum dado registrado")

# Sugestões
st.markdown("---")
st.subheader("🎯 Sugestões de Jogada")

if padroes_detectados:
    # Agrupa sugestões por tipo
    sugestoes_agrupadas = defaultdict(list)
    for padrao in padroes_detectados:
        sugestoes_agrupadas[padrao["sugestao"]].append(padrao)
    
    # Exibe as sugestões consolidadas
    for sugestao, padroes in sugestoes_agrupadas.items():
        # Encontra o padrão com maior confiança
        melhor_padrao = max(padroes, key=lambda x: x["confianca"])
        total_padroes = len(padroes)
        
        st.markdown(f"""
        <div style="border: 1px solid #4CAF50; border-radius: 10px; padding: 15px; margin: 10px 0;">
            <h3>Jogar {sugestao}</h3>
            <p>🔍 {melhor_padrao['logica']}</p>
            <p>📊 Confiança: <strong>{melhor_padrao['confianca']}%</strong></p>
            <p>🧩 Padrões similares: {total_padroes}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botão para jogar
        if st.button(f"Registrar {sugestao}", key=f"btn_jogar_{sugestao}"):
            inserir(sugestao)
            st.experimental_rerun()
    
    # Análise estatística
    st.markdown("---")
    st.subheader("📈 Análise de Confiabilidade")
    
    # Calcula precisão histórica
    if len(st.session_state.historico) > 10:
        acertos = 0
        total_sugestoes = 0
        for i in range(1, len(st.session_state.historico)):
            # Simples verificação se a jogada anterior foi sugerida
            if i < len(padroes_detectados):
                if st.session_state.historico[i] == padroes_detectados[i-1]["sugestao"]:
                    acertos += 1
                total_sugestoes += 1
        
        if total_sugestoes > 0:
            precisao = (acertos / total_sugestoes) * 100
            st.metric("Precisão Histórica", f"{precisao:.1f}%", 
                     delta=f"{precisao - 50:.1f}% acima do esperado")
    else:
        st.info("Registre mais jogadas para habilitar análise de precisão")
else:
    st.info("⚠️ Nenhum padrão significativo detectado. Sugestões baseadas em frequência:")
    
    # Sugestão por desequilíbrio de frequência
    if total > 0:
        percent_red = contagem.get("🔴", 0) / total
        percent_blue = contagem.get("🔵", 0) / total
        
        if percent_red > percent_blue + 0.15:
            st.success("🔵 Jogar Visitante (Casa com frequência muito alta)")
        elif percent_blue > percent_red + 0.15:
            st.success("🔴 Jogar Casa (Visitante com frequência muito alta)")
        else:
            st.info("🟡 Frequências equilibradas - Sugerimos Empate")
    else:
        st.info("Registre as primeiras jogadas para começar a análise")

# Visualização de tendências
st.markdown("---")
st.subheader("📈 Visualização de Tendências")

if len(linhas_completas) > 0:
    # Cria matriz para visualização
    df = pd.DataFrame(linhas_completas[:5])
    df = df.replace({"🔴": 1, "🔵": -1, "🟡": 0})
    
    # Plot de calor
    st.write("Mapa de Calor das Últimas Linhas:")
    st.dataframe(df.style.background_gradient(cmap="coolwarm", vmin=-1, vmax=1))
    
    # Análise de distribuição
    st.write("Distribuição nas Últimas Jogadas:")
    ultimas_jogadas = historico_limitado[:min(20, len(historico_limitado))]
    contagem_ultimas = Counter(ultimas_jogadas)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("🔴 Casa", contagem_ultimas.get("🔴", 0))
    col2.metric("🔵 Visitante", contagem_ultimas.get("🔵", 0))
    col3.metric("🟡 Empate", contagem_ultimas.get("🟡", 0))
    
    # Sugestão visual
    st.write("Sugestão Visual:")
    cores = ["🔴", "🔵", "🟡"]
    valores = [contagem_ultimas.get(cor, 0) for cor in cores]
    max_val = max(valores) if valores else 1
    
    for cor, val in zip(cores, valores):
        barra = "█" * math.ceil(val * 20 / max_val)
        st.write(f"{cor} {barra} {val}")
else:
    st.info("Registre jogadas completas para ver as tendências")

# Configurações
st.markdown("---")
st.subheader("⚙️ Configurações")
st.slider("Sensibilidade de Detecção", 0.5, 1.0, 0.7, 0.05, key="sensibilidade")

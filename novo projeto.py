import streamlit as st
from collections import Counter

# Inicializa histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

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
    # CORREÇÃO: Verifica tamanho igual das colunas
    if len(c1) != len(c2):
        return False
        
    for a, b in zip(c1, c2):
        if a == "🟡" or b == "🟡":
            continue
        if not cores_opostas(a, b):
            return False
    return True

def inserir(cor):
    # MELHORIA: Impede inserção além do limite
    if len(st.session_state.historico) < 27:
        st.session_state.historico.insert(0, cor)
    # Mantém apenas os últimos 27 resultados
    st.session_state.historico = st.session_state.historico[:27]

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

# Exibir histórico (máximo 27 jogadas)
st.markdown("---")
st.subheader("📋 Histórico de Jogadas (últimas 27, mais recentes no topo)")

historico_limitado = st.session_state.historico[:27]

linhas = []
for i in range(0, len(historico_limitado), 9):
    linha = historico_limitado[i:i+9]
    linhas.append(linha)

linhas_exibidas = linhas[::-1]  # Mais recentes primeiro

for idx, linha in enumerate(linhas_exibidas):
    st.markdown(f"**Linha {idx+1}:** " + " ".join(linha))

# Frequência
st.markdown("---")
st.subheader("📊 Frequência de Cores")
contagem = Counter(historico_limitado)
st.write(f"🔴 Casa: {contagem['🔴']} | 🔵 Visitante: {contagem['🔵']} | 🟡 Empate: {contagem['🟡']}")

# Análise por linhas (padrão reescrito)
st.markdown("---")
st.subheader("🧠 Detecção de Padrão Reescrito")

linhas_validas = [l for l in linhas_exibidas if len(l) == 9]

if len(linhas_validas) >= 2:
    linha1 = linhas_validas[0]
    linha2 = linhas_validas[1]

    if padrao_reescrito(linha1, linha2):
        ultima_jogada = linha1[-1]
        
        # MELHORIA: Sugestão melhorada com tratamento de empate
        if ultima_jogada == "🔴":
            jogada_sugerida = "🔵"
        elif ultima_jogada == "🔵":
            jogada_sugerida = "🔴"
        else:
            jogada_sugerida = "🟡"  # Empate
            
        st.success(f"""
        🔁 **Padrão reescrito com inversão cromática detectado!**
        \nÚltima jogada: {ultima_jogada}
        \n🎯 **Sugestão:** Jogar {jogada_sugerida}
        """)
    else:
        st.info("⏳ Nenhum padrão reescrito identificado entre as duas últimas linhas completas.")
elif len(historico_limitado) < 18:
    st.warning("⚠️ Registre pelo menos 18 jogadas para ativar a análise (2 linhas de 9).")
else:
    st.info("Aguardando segunda linha completa para análise.")

# Análise por colunas verticais
st.markdown("---")
st.subheader("🧬 Análise por Colunas Verticais")

if len(historico_limitado) == 27:
    linhas_3x9 = []
    for i in range(0, 27, 9):
        linha = historico_limitado[i:i+9]
        linhas_3x9.append(linha)

    colunas = list(zip(*linhas_3x9))  # 9 colunas de 3

    ref_coluna_antiga = colunas[3]
    nova_coluna = colunas[0]

    if colunas_semelhantes(ref_coluna_antiga, nova_coluna):
        coluna_apos_ref = colunas[4]
        proxima_sugestao = coluna_apos_ref[0]
        
        # MELHORIA: Sugestão com tratamento de empate
        if proxima_sugestao == "🔴":
            sugestao_convertida = "🔵"
        elif proxima_sugestao == "🔵":
            sugestao_convertida = "🔴"
        else:
            sugestao_convertida = "🟡"  # Empate

        st.success(f"""
        🔂 Estrutura de colunas repetida com troca de cores detectada!
        \n📌 Coluna antiga (posição 4) ≈ Nova coluna (posição 1)
        \n💡 Padrão esperado: Após a coluna 4 veio **{proxima_sugestao}**
        \n🎯 **Sugestão:** Jogar {sugestao_convertida}
        """)
    else:
        st.info("📊 Nenhum padrão repetido de colunas encontrado nas últimas 27 jogadas.")
else:
    st.warning("⚠️ Registre exatamente 27 jogadas para ativar a análise por colunas verticais.")

# Visualização das colunas verticais com cores
if len(historico_limitado) == 27:
    st.subheader("🧱 Visualização das Colunas Verticais (3x9)")

    # MELHORIA: Visualização com cores de fundo
    col_container = st.container()
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = col_container.columns(9)
    colunas_texto = list(zip(*linhas_3x9))

    for i, coluna in enumerate(colunas_texto):
        # Cria string formatada com cores
        elementos_html = []
        for elemento in coluna:
            if elemento == "🔴":
                bg_color = "#ffcccc"  # Vermelho claro
            elif elemento == "🔵":
                bg_color = "#cce0ff"  # Azul claro
            else:
                bg_color = "#ffffcc"  # Amarelo claro
                
            elementos_html.append(
                f'<div style="background-color: {bg_color};'
                f'padding: 8px; margin: 2px; border-radius: 5px;'
                f'text-align: center;">{elemento}</div>'
            )
        
        texto_html = f"<b>Coluna {i+1}</b><br>" + "<br>".join(elementos_html)
        
        # Renderiza na coluna correspondente
        match i:
            case 0: col1.markdown(texto_html, unsafe_allow_html=True)
            case 1: col2.markdown(texto_html, unsafe_allow_html=True)
            case 2: col3.markdown(texto_html, unsafe_allow_html=True)
            case 3: col4.markdown(texto_html, unsafe_allow_html=True)
            case 4: col5.markdown(texto_html, unsafe_allow_html=True)
            case 5: col6.markdown(texto_html, unsafe_allow_html=True)
            case 6: col7.markdown(texto_html, unsafe_allow_html=True)
            case 7: col8.markdown(texto_html, unsafe_allow_html=True)
            case 8: col9.markdown(texto_html, unsafe_allow_html=True)

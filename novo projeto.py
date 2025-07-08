import streamlit as st

Configuração da página

st.set_page_config(page_title="Análise Football Studio", layout="wide")

Mapeamento de cores

COLOR_MAP = { "🔵": "#3498db",  # Azul "🔴": "#e74c3c",  # Vermelho "🟡": "#f1c40f",  # Amarelo }

Inicialização do estado

if "history" not in st.session_state: st.session_state.history = []

Interface de entrada de cores

st.title("📌 Histórico (Mais Recente Primeiro)") col1, col2, col3 = st.columns(3) with col1: if st.button("🔵 Azul"): st.session_state.history.insert(0, "🔵") with col2: if st.button("🔴 Vermelho"): st.session_state.history.insert(0, "🔴") with col3: if st.button("🟡 Empate"): st.session_state.history.insert(0, "🟡")

Divide o histórico em linhas de 9 (mais recente à esquerda)

def dividir_em_linhas(lista, largura=9): linhas = [] for i in range(0, len(lista), largura): linhas.append(lista[i:i+largura]) return linhas

Gerar as 3 linhas principais e dividir em colunas (esquerda para direita)

h_linhas = dividir_em_linhas(st.session_state.history)

Separar em histórico atual (3 primeiras linhas) e antigo (as 3 anteriores)

h_atual = h_linhas[:3]  # Mais recente h_antigo = h_linhas[3:6] if len(h_linhas) >= 6 else []

Completa as linhas para que todas tenham 9 itens

for linha in h_atual: while len(linha) < 9: linha.append(" ") for linha in h_antigo: while len(linha) < 9: linha.append(" ")

Exibir lado a lado

st.subheader("🧱 Histórico Atual vs Antigo") for i in range(3): col_a, col_b = st.columns(2) with col_a: if i < len(h_atual): st.markdown("<div style='font-size:30px;'>" + "".join(h_atual[i]) + "</div>", unsafe_allow_html=True) with col_b: if i < len(h_antigo): st.markdown("<div style='font-size:30px;'>" + "".join(h_antigo[i]) + "</div>", unsafe_allow_html=True)

Botão de limpar

if st.button("🧹 Limpar Histórico"): st.session_state.history = [] st.experimental_rerun()


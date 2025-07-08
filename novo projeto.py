import streamlit as st
from typing import List
from collections import Counter

st.set_page_config(layout="wide")
st.title("🔁 Column Rewriting Analysis - Football Studio")

# Emoji to color mapping
COLOR_MAP = {
    "🔴": "red",
    "🔵": "blue",
    "🟡": "gold"
}

# --- INPUT ---
st.markdown("### 📥 Enter Game Results (latest first)")
history_input = st.text_area(
    "Paste results separated by space:",
    placeholder="🔴 🔵 🟡 🔴 🔵 🔵 🔴...",
    height=120
)

results = history_input.strip().split()
if len(results) < 36:
    st.info("Please enter at least 36 results to form 6 rows of 9.")
    st.stop()

# --- BUILD ROWS OF 9 ---
def build_rows(data):
    rows = []
    for i in range(0, len(data), 9):
        rows.append(data[i:i+9])
    return rows[:6]

rows = build_rows(results)

# --- SPLIT CURRENT AND OLD ---
current_rows = rows[:3]
old_rows = rows[3:6]

st.markdown("### 🧱 Current History (left) vs Old History (right)")
for i in range(3):
    col1, col2 = st.columns(2)
    with col1:
        if i < len(current_rows):
            st.markdown(
                "<div style='font-size:28px; text-align:center;'>" +
                " ".join(current_rows[i]) +
                "</div>", unsafe_allow_html=True
            )
    with col2:
        if i < len(old_rows):
            st.markdown(
                "<div style='font-size:28px; text-align:center;'>" +
                " ".join(old_rows[i]) +
                "</div>", unsafe_allow_html=True
            )

# --- EXTRACT COLUMNS ---
def extract_columns(rows: List[List[str]]) -> List[List[str]]:
    columns = [[] for _ in range(9)]
    for row in rows:
        for idx, val in enumerate(row):
            columns[idx].append(val)
    return columns

# --- NORMALIZE STRUCTURE (Ex: 🔴🔵🟡 → 123 or 🔵🔴🔵 → 121) ---
def normalize_pattern(col: List[str]) -> str:
    mapping = {}
    result = []
    code = 1
    for color in col:
        if color not in mapping:
            mapping[color] = str(code)
            code += 1
        result.append(mapping[color])
    return "".join(result)

# --- ANALYZE COLUMNS ---
st.markdown("### 🔍 Compare Column 1 (new) vs Column 4 (old)")

if len(rows) >= 4:
    all_columns = extract_columns(rows)
    col1 = all_columns[0]
    col4 = all_columns[3]

    exact_matches = 0
    structure_matches = 0
    comparison = []

    for i in range(3):
        a = col1[i]
        b = col4[i]
        if a == b:
            result = "✅ Exact"
            exact_matches += 1
        elif normalize_pattern([a]) == normalize_pattern([b]):
            result = "🔁 Structure"
            structure_matches += 1
        else:
            result = "❌"
        comparison.append({
            "Row": i + 1,
            "Column 1": a,
            "Column 4": b,
            "Match": result
        })

    st.markdown(f"**Exact Matches:** {exact_matches}/3  ")
    st.markdown(f"**Structural Matches:** {structure_matches}/3")
    st.table(comparison)
else:
    st.warning("You need at least 4 lines of 9 for column analysis.")

# --- SUGGESTION ---
st.markdown("### 🤖 Intelligent Suggestion")

if exact_matches >= 2:
    st.success("🧠 Column 1 appears to exactly repeat Column 4.")
    st.markdown("📌 Suggestion: Continue following Column 4's structure for predictions.")
elif structure_matches >= 2:
    st.info("🔄 Column 1 structurally repeats Column 4 with different colors.")
    st.markdown("📌 Suggestion: Consider pattern continuity despite color swaps.")
else:
    st.warning("Not enough repetition yet. Wait for more data.")

# --- STYLES ---
st.markdown(\"\"\"\n<style>\n    .stTextArea textarea {\n        font-size: 20px;\n        line-height: 1.5;\n    }\n</style>\n\"\"\", unsafe_allow_html=True)

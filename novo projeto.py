import streamlit as st from typing import List from collections import Counter

st.set_page_config(layout="wide")

st.title("🔁 Column Rewriting Analysis - Football Studio")

Color mapping

COLOR_MAP = { "🔴": "red", "🔵": "blue", "🟡": "gold" }

Input

st.markdown("### 📥 Enter Game Results (latest first)") history_input = st.text_area( "Paste results separated by space:", placeholder="🔴 🔵 🟡 🔴 🔵 🔵 🔴...", height=120 )

Validate

results = history_input.strip().split() if len(results) < 36: st.info("Please enter at least 36 results to form 6 rows of 9.") st.stop()

Create rows of 9

def build_rows(data): rows = [] for i in range(0, len(data), 9): rows.append(data[i:i+9]) return rows[:6]

rows = build_rows(results)

Divide into recent and old

current_rows = rows[:3] old_rows = rows[3:6]

st.markdown("### 🧱 Current History (left) vs Old History (right)") for i in range(3): col1, col2 = st.columns(2) with col1: if i < len(current_rows): st.markdown( "<div style='font-size:28px; text-align:center;'>" + " ".join(current_rows[i]) + "</div>", unsafe_allow_html=True ) with col2: if i < len(old_rows): st.markdown( "<div style='font-size:28px; text-align:center;'>" + " ".join(old_rows[i]) + "</div>", unsafe_allow_html=True )

Extract columns from rows

def extract_columns(rows: List[List[str]]) -> List[List[str]]: columns = [[] for _ in range(9)] for row in rows: for idx, val in enumerate(row): columns[idx].append(val) return columns

Normalize pattern (e.g. RBY -> 123, 312, etc.)

def normalize_pattern(col: List[str]) -> str: mapping = {} seq = [] code = 1 for color in col: if color not in mapping: mapping[color] = str(code) code += 1 seq.append(mapping[color]) return "".join(seq)

Column analysis

st.markdown("### 🔍 Analyze Column 1 (new) vs Column 4 (past)") if len(rows) >= 4: all_columns = extract_columns(rows) column_1 = all_columns[0] column_4 = all_columns[3]

match_count = 0
structure_match = 0
comparison = []
norm_1 = normalize_pattern(column_1)
norm_4 = normalize_pattern(column_4)

for i in range(3):
    exact = column_1[i] == column_4[i]
    struct = normalize_pattern([column_1[i]]) == normalize_pattern([column_4[i]])
    result = "✅ Exact" if exact else ("🔁 Structure" if column_1[i] != column_4[i] else "❌")
    if exact:
        match_count += 1
    elif normalize_pattern([column_1[i]]) == normalize_pattern([column_4[i]]):
        structure_match += 1
    comparison.append({
        "Index": i + 1,
        "Column 1": column_1[i],
        "Column 4": column_4[i],
        "Result": result
    })

st.markdown(f"**Exact Matches:** {match_count}/3  ")
st.markdown(f"**Structure Matches:** {structure_match}/3")
st.table(comparison)

else: st.warning("Not enough data for column analysis.")

Suggestion

st.markdown("### 🤖 Intelligent Suggestion") if match_count >= 2: st.success("🧠 Column 1 is repeating Column 4 exactly.") st.markdown("📌 Suggestion: Follow the structure from Column 4 for next prediction.") elif structure_match >= 2: st.info("🔄 Column 1 is structurally repeating Column 4 with color changes.") st.markdown("📌 Suggestion: Similar structure, consider pattern continuity with palette swap.") else: st.warning("Not enough similarity detected yet. Await more results.")

Style

st.markdown(""" <style> .stTextArea textarea { font-size: 20px; line-height: 1.5; } </style> """, unsafe_allow_html=True)


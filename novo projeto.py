import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from collections import Counter
import json
import os

# --- Configurações Iniciais ---
HISTORY_FILE = 'football_studio_history.json'
LINE_LENGTH = 9
ANALYSIS_LINE_INDEX = 3

# --- Mapeamento de Cores ---
COLOR_MAP = {
    'R': {'name': 'Casa (Home)', 'color_hex': '                                 
    '#EF4444', 'text_color': 'white'},
    'B': {'name': 'Visitante (Away)', 'color_hex': '#3B82F6', 'text_color': 'white'},
    'Y': {'name': 'Empate (Draw)', 'color_hex': '                                
}

                                          
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, '#FACC15', 'text_color': 'black'}
}

# --- Funções de Persistência Local ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_history(history):
    with open(HISTORY_FILE, 'def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

                               
def get_history_lines(history):
    lines = []
    reversed_history = history[::-1]
    for i in range(0, len(reversed_history), LINE_LENGTH):
        lines.append(reversed_history[i:i + LINE_LENGTH])
    return lines

def analyze_repeating_line_patterns(history, history_lines):
    suggestions = []
    if len(history_lines) <= ANALYSIS_LINE_INDEX:
        return suggestions
    target_line = history_lines[ANALYSIS_LINE_INDEX]
    target_line_str = "".join(target_line)
    found_matches = []
    for i, current_line in enumerate(history_lines):
        if i == ANALYSIS_LINE_INDEX:
            continue
        current_line_str = "".join(current_line)
        if target_line_str == current_line_str:
            found_matches.append({'# --- Funções de Análise ---
def get_history_lines(history):
    lines = []
    reversed_history = history[::-1]
    for i in range(0, len(reversed_history), LINE_LENGTH):
        lines.append(reversed_history[i:i + LINE_LENGTH])
    return lines

def analyze_repeating_line_patterns(history, history_lines):
    suggestions = []
    if len(history_lines) <= ANALYSIS_LINE_INDEX:
        return suggestions
    target_line = history_lines[ANALYSIS_LINE_INDEX]
    target_line_str = "".join(target_line)
    found_matches = []
    for i, current_line in enumerate(history_lines):
        if i == ANALYSIS_LINE_INDEX:
            continue
        current_line_str = "".join(current_line)
        if target_line_str == current_line_str:
            found_matches.append({'index_line': i, 'line_content': current_line, 'type': 'Exata'})
        elif target_line_str.startswith(current_line_str):
            found_matches.append({'index_line': i, 'line_content': current_line, 'type': 'Prefixo'})
    if found_matches:
        reason_base = f"A linha atual (índice {ANALYSIS_LINE_INDEX+1} - '{target_line_str}') foi detectada como similar a padrões anteriores."
        potential_next_colors = Counter()
        for match in found_matches:
            start_index_in_original = len(history) - ((match['index_line'] + 1) * LINE_LENGTH)
            end_index_in_original = start_index_in_original + len(match['line_content']) - 1
            if end_index_in_original + 1 < len(history):
                next_entry = history[end_index_in_original + 1]
                potential_next_colors[next_entry] += 1
        if potential_next_colors:
            most_likely_next, count = potential_next_colors.most_common(1)[0]
            total_next = sum(potential_next_colors.values())
            confidence = round((count / total_next) * 100)
            suggestions.append({
                'type': 'Repetição de Linha (Continuação Padrão)',
                'suggestion': most_likely_next,
                'confidence': confidence,
                'reason': f"{reason_base} Com base em ocorrências anteriores de padrões similares, a próxima cor mais comum foi **{COLOR_MAP[most_likely_next]['name']}** ({count}/{total_next} vezes)."
            })
        else:
            color_counts_target_line = Counter(target_line)
            if color_counts_target_line:
                most_common_color_in_line, _ = color_counts_target_line.most_common(1)[0]
                suggestions.append({
                    'type': 'Repetição de Linha (Cor Dominante)',
                    'suggestion': most_common_color_in_line,
                    'confidence': 60,
                    'reason': f"{reason_base} A cor dominante nesta linha repetida é **{COLOR_MAP[most_common_color_in_line]['name']}**. Pode continuar."
                })
    return suggestions

def analyze_general_patterns(history):
    suggestions = []
    if len(history) < 2:
        return suggestions
    last_color = history[-1]
    transitions = {c: Counter() for c in COLOR_MAP.keys()}
    for i in range(len(history) - 1):
        transitions[history[i]][history[i+1]] += 1
    if last_color in transitions and transitions[last_color]:
        most_likely_next_transition, count_transition = transitions[last_color].most_common(1)[0]
        total_transitions = sum(transitions[last_color].values())
        confidence = round((count_transition / total_transitions) * 100)
        suggestions.append({

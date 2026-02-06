import streamlit as st
import pandas as pd
import numpy as np

# Configurações Iniciais de Estado
if 'etapa' not in st.session_state:
    st.session_state.etapa = 'identificacao'
    st.session_state.dados_coletados = []
    st.session_state.atrasos = [7, 30, 180, 365]
    st.session_state.atraso_atual_idx = 0
    st.session_state.passo_staircase = 0
    st.session_state.valor_agora = 50.0
    st.session_state.ajuste = 25.0

st.title("🧠 Pesquisa de Tomada de Decisão (DDT)")

# --- ETAPA 1: IDENTIFICAÇÃO ---
if st.session_state.etapa == 'identificacao':
    with st.form("form_id"):
        nome = st.text_input("Nome ou Iniciais:")
        sexo = st.selectbox("Sexo:", ["M", "F"])
        idade = st.number_input("Idade:", min_value=18)
        if st.form_submit_button("Iniciar Experimento"):
            st.session_state.nome = nome
            st.session_state.sexo = sexo
            st.session_state.etapa = 'experimento'
            st.rerun()

# --- ETAPA 2: EXPERIMENTO ---
elif st.session_state.etapa == 'experimento':
    idx = st.session_state.atraso_atual_idx
    dias = st.session_state.atrasos[idx]
    
    st.subheader(f"Bloco {idx+1}/4: Recompensa em {dias} dias")
    st.write(f"Escolha uma das opções abaixo (Tentativa {st.session_state.passo_staircase + 1}/6):")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"R$ {st.session_state.valor_agora:.2f} AGORA"):
            st.session_state.valor_agora -= st.session_state.ajuste
            st.session_state.ajuste /= 2
            st.session_state.passo_staircase += 1
            if st.session_state.passo_staircase == 6:
                st.session_state.dados_coletados.append({
                    'atraso_dias': dias, 'ponto_indiferenca': st.session_state.valor_agora
                })
                st.session_state.passo_staircase = 0
                st.session_state.valor_agora = 50.0
                st.session_state.ajuste = 25.0
                st.session_state.atraso_atual_idx += 1
            st.rerun()

    with col2:
        if st.button(f"R$ 100.00 em {dias} dias"):
            st.session_state.valor_agora += st.session_state.ajuste
            st.session_state.ajuste /= 2
            st.session_state.passo_staircase += 1
            if st.session_state.passo_staircase == 6:
                st.session_state.dados_coletados.append({
                    'atraso_dias': dias, 'ponto_indiferenca': st.session_state.valor_agora
                })
                st.session_state.passo_staircase = 0
                st.session_state.valor_agora = 50.0
                st.session_state.ajuste = 25.0
                st.session_state.atraso_atual_idx += 1
            st.rerun()

    if st.session_state.atraso_atual_idx == 4:
        st.session_state.etapa = 'finalizado'
        st.rerun()

# --- ETAPA 3: FINALIZAÇÃO ---
elif st.session_state.etapa == 'finalizado':
    st.success("Obrigado! Sua participação foi registrada.")
    df_final = pd.DataFrame(st.session_state.dados_coletados)
    df_final['sujeito'] = st.session_state.nome
    
    csv = df_final.to_csv(index=False).encode('utf-8')
    st.download_button("Baixar meu resultado (.csv)", csv, f"resultado_{st.session_state.nome}.csv")
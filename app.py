import streamlit as st
import pandas as pd
import numpy as np

# 1. Configurações Iniciais de Estado (Session State)
if 'etapa' not in st.session_state:
    st.session_state.etapa = 'identificacao'
    st.session_state.dados_coletados = []
    st.session_state.atrasos = [7, 30, 180, 365]
    st.session_state.atraso_atual_idx = 0
    st.session_state.passo_staircase = 0
    st.session_state.valor_agora = 50.0
    st.session_state.ajuste = 25.0

st.title("🧠 Laboratório Virtual: Desconto Temporal")

# --- BARRA LATERAL (FERRAMENTAS DE TESTE) ---
with st.sidebar:
    st.header("Modo Desenvolvedor")
    if st.button("🧪 Pular para o Final (Teste)"):
        st.session_state.dados_coletados = [
            {'atraso_dias': 7, 'ponto_indiferenca': 50.0},
            {'atraso_dias': 30, 'ponto_indiferenca': 40.0},
            {'atraso_dias': 180, 'ponto_indiferenca': 20.0},
            {'atraso_dias': 365, 'ponto_indiferenca': 10.0}
        ]
        st.session_state.atraso_atual_idx = 4
        st.session_state.etapa = 'finalizado'
        st.rerun()
    st.write("---")
    st.caption("Use o botão acima para validar o download sem precisar responder.")

# --- ETAPA 1: IDENTIFICAÇÃO ---
if st.session_state.etapa == 'identificacao':
    st.info("Bem-vindo! Identifique-se para começar.")
    with st.form("form_id"):
        nome = st.text_input("Nome ou Iniciais:")
        sexo = st.selectbox("Sexo:", ["M", "F"])
        idade = st.number_input("Idade:", min_value=18, max_value=100)
        if st.form_submit_button("Iniciar Experimento"):
            if nome:
                st.session_state.nome = nome
                st.session_state.sexo = sexo
                st.session_state.etapa = 'experimento'
                st.rerun()
            else:
                st.warning("Por favor, insira um nome ou iniciais.")

# --- ETAPA 2: EXPERIMENTO ---
elif st.session_state.etapa == 'experimento':
    idx = st.session_state.atraso_atual_idx
    
    # Trava de segurança para evitar o IndexError
    if idx < len(st.session_state.atrasos):
        dias = st.session_state.atrasos[idx]
        
        st.subheader(f"Bloco {idx+1}/4: Recompensa em {dias} dias")
        st.write(f"**Pergunta {st.session_state.passo_staircase + 1} de 6**")
        st.write("O que você prefere receber?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"R$ {st.session_state.valor_agora:.2f} AGORA", use_container_width=True):
                st.session_state.valor_agora -= st.session_state.ajuste
                st.session_state.ajuste /= 2
                st.session_state.passo_staircase += 1
                
                if st.session_state.passo_staircase == 6:
                    st.session_state.dados_coletados.append({
                        'sujeito': st.session_state.nome,
                        'atraso_dias': dias, 
                        'ponto_indiferenca': st.session_state.valor_agora,
                        'valor_futuro': 100.0
                    })
                    st.session_state.passo_staircase = 0
                    st.session_state.valor_agora = 50.0
                    st.session_state.ajuste = 25.0
                    st.session_state.atraso_atual_idx += 1
                st.rerun()

        with col2:
            if st.button(f"R$ 100.00 em {dias} dias", use_container_width=True):
                st.session_state.valor_agora += st.session_state.ajuste
                st.session_state.ajuste /= 2
                st.session_state.passo_staircase += 1
                
                if st.session_state.passo_staircase == 6:
                    st.session_state.dados_coletados.append({
                        'sujeito': st.session_state.nome,
                        'atraso_dias': dias, 
                        'ponto_indiferenca': st.session_state.valor_agora,
                        'valor_futuro': 100.0
                    })
                    st.session_state.passo_staircase = 0
                    st.session_state.valor_agora = 50.0
                    st.session_state.ajuste = 25.0
                    st.session_state.atraso_atual_idx += 1
                st.rerun()
    else:
        st.session_state.etapa = 'finalizado'
        st.rerun()

# --- ETAPA 3: FINALIZAÇÃO ---
elif st.session_state.etapa == 'finalizado':
    st.success(f"Parabéns, {st.session_state.nome}! Você concluiu a tarefa.")
    st.write("Clique no botão abaixo para gerar o seu arquivo de resultados e envie para o pesquisador.")
    
    df_final = pd.DataFrame(st.session_state.dados_coletados)
    
    csv = df_final.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Resultados (.csv)",
        data=csv,
        file_name=f"resultado_ddt_{st.session_state.nome}.csv",
        mime="text/csv"
    )
    
    if st.button("Reiniciar Teste"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

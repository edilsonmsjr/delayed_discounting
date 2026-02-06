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



# --- ETAPA 1: IDENTIFICAÇÃO E TCLE (TERMO DE CONSENTIMENTO) ---
if st.session_state.etapa == 'identificacao':
    st.header("Estudo sobre Processos Decisórios e Percepção Temporal")
    
    # Texto do TCLE formatado para leitura clara
    st.markdown("""
    ### Termo de Consentimento Livre e Esclarecido (TCLE)
    
    Olá! Você está sendo convidado(a) a participar de um estudo acadêmico conduzido por pesquisadores do **Instituto de Psicologia da USP (IP-USP)**. 
    O objetivo desta tarefa é entender como as pessoas avaliam recompensas financeiras em diferentes períodos de tempo.

    **Como funciona?**
    Você fará uma série de escolhas simples entre duas opções: uma quantia em dinheiro disponível **hoje** ou uma quantia maior disponível no **futuro**. 
    Não existem respostas certas ou erradas; o que nos interessa é a sua preferência pessoal.

    **Informações Importantes:**
    1. **Rigor e Sigilo:** Suas respostas são anônimas. Os dados coletados serão utilizados estritamente para fins de análise estatística e pesquisa acadêmica.
    2. **Participação Voluntária:** Você tem total liberdade para desistir da tarefa a qualquer momento, bastando fechar o navegador.
    3. **Riscos e Benefícios:** Não há riscos físicos ou financeiros. O benefício é a sua contribuição para o avanço da neurociência comportamental no Brasil.
    4. **Envio de Dados:** Ao final, o sistema gerará um arquivo com seus resultados. Para colaborar com a pesquisa, pedimos que você envie esse arquivo para o pesquisador responsável.
    
    ---
    """)
    
    # Caixa de aceite obrigatória
    aceite = st.checkbox("**Eu li e aceito participar desta pesquisa.**")
    
    # Formulário de identificação
    with st.form("identificacao_participante"):
        nome = st.text_input("Insira seu nome ou iniciais para registro do arquivo:")
        sexo = st.selectbox("Sexo Biológico:", ["M", "F"])
        idade = st.number_input("Idade:", min_value=18, max_value=100, step=1)
        
        botao_iniciar = st.form_submit_button("Confirmar e Iniciar Experimento")
        
        if botao_iniciar:
            if not aceite:
                st.error("⚠️ Para prosseguir, você precisa ler e marcar que aceita o Termo de Consentimento (TCLE).")
            elif not nome:
                st.warning("⚠️ Por favor, insira um nome ou iniciais para gerar seu resultado.")
            else:
                # Se tudo estiver ok, salva na memória e muda a etapa
                st.session_state.nome = nome
                st.session_state.sexo = sexo
                st.session_state.idade = idade
                st.session_state.etapa = 'experimento'
                st.rerun()

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





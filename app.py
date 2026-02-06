# BOTÃO DE ATALHO (DEBUG) - APAGUE ANTES DE PUBLICAR OFICIALMENTE
if st.sidebar.button("🧪 Pular Teste (Preencher Automático)"):
    st.session_state.dados_coletados = [
        {'atraso_dias': 7, 'ponto_indiferenca': 50.0},
        {'atraso_dias': 30, 'ponto_indiferenca': 40.0},
        {'atraso_dias': 180, 'ponto_indiferenca': 20.0},
        {'atraso_dias': 365, 'ponto_indiferenca': 10.0}
    ]
    st.session_state.atraso_atual_idx = 4
    st.session_state.etapa = 'finalizado'
    st.rerun()
# --- ETAPA 2: EXPERIMENTO ---
elif st.session_state.etapa == 'experimento':
    idx = st.session_state.atraso_atual_idx
    
    # PROVA DE ERRO: Verifica se ainda existem blocos para fazer
    if idx < len(st.session_state.atrasos):
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
    else:
        # Se o índice passou de 4, finaliza
        st.session_state.etapa = 'finalizado'
        st.rerun()


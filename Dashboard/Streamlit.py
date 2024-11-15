from streamlit_autorefresh import st_autorefresh
import paho.mqtt.client as mqtt 
import random
import streamlit as st
import time


file_path='log.txt'

# Classe principal que controla a interface
class Aplicativo:
    def __init__(self, titulo, mensagem):
        self.titulo = titulo
        self.mensagem = mensagem
                
        if 'log' not in st.session_state:
            st.session_state.log = []            
        
        if 'pagina' not in st.session_state:
            st.session_state.pagina = 'inicial'
           
        st.title(self.titulo)  # Exibe o título na página
        st.write(self.mensagem)  # Exibe uma mensagem na página
         
        self.navbar()
             
    def navbar(self):
        st.sidebar.title("Projeto AI URA")

        # Botões para navegação
        if st.sidebar.button('Página Inicial', use_container_width=True):
            st.session_state.pagina = 'inicial'
        
        if st.sidebar.button('Gráficos', use_container_width=True):
            st.session_state.pagina = 'graficos'
        
        if st.sidebar.button('MQTT', use_container_width=True):
            st.session_state.pagina = 'MQTT'

        # Renderizar o conteúdo com base na página selecionada
        if st.session_state.pagina == 'inicial':
            self.renderiza_pagina_inicial()
        
        elif st.session_state.pagina == 'graficos':
            self.renderiza_graficos()
        elif st.session_state.pagina == 'MQTT':
            self.renderiza_mqtt() 
    
    def renderiza_pagina_inicial(self):
        # st.write('Pagina inicial')
        st.image('IA URA.png')
        
    def renderiza_graficos(self):
        st.write('Página de gráficos')
   
    def renderiza_mqtt(self):
        
        try:
        # Abre e lê o conteúdo do arquivo
            with open(file_path, "r", encoding="utf-8") as file:
                self.log_mqtt = file.read().split('\n')  
                
                # Remove o caractere '' criado na lista
                st.session_state.log = self.log_mqtt[:-1]  
                    
        except FileNotFoundError:
            st.error("Arquivo não encontrado. Verifique o caminho e tente novamente.")
            
        except Exception as e:
            st.error(f"Ocorreu um erro ao ler o arquivo: {e}")
                    
        # Criação de colunas
        col1, col2 = st.columns([1,1])

        with col1:
            st.header('Histórico de comandos')
            if len(st.session_state.log) > 0:
                for log in st.session_state.log[::-1]:
                    st.text(log)
            else: 
                st.text('Nenhum comando foi enviado')
                
        with col2:
            st.header('Último comando enviado')
            if len(st.session_state.log) > 0:
                st.text(st.session_state.log[-1])
            else: 
                st.text('Nenhum comando foi enviado')
        
        # Atualiza a página
        self.autorefresh = st_autorefresh(interval=2000, key="mqtt")        

def main():
    # Instância da classe
    app_instance = Aplicativo(titulo='Projeto AI URA', mensagem='Colaboratividade entre carrinho e drone usando inteligência artificial')
    
if __name__ == "__main__":
    main()

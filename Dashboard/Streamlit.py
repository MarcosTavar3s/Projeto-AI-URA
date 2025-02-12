from streamlit_autorefresh import st_autorefresh
import paho.mqtt.client as mqtt
import random
import streamlit as st
import time
import matplotlib.pyplot as plt
import numpy as np

file_path = 'log.txt'

# Classe principal que controla a interface
class Aplicativo:
    """
    Classe responsável por gerenciar a interface do aplicativo, incluindo a navegação e a renderização das páginas.
    """
    def __init__(self, titulo, mensagem):
        """
        Construtor da classe Aplicativo.
        Inicializa o título e a mensagem, além de configurar o estado inicial da aplicação.

        Parameters:
        titulo (str): Título da aplicação.
        mensagem (str): Mensagem a ser exibida na página inicial.
        """
        self.titulo = titulo
        self.mensagem = mensagem

        if 'log' not in st.session_state:
            st.session_state.log = []

        if 'pagina' not in st.session_state:
            st.session_state.pagina = 'inicial'

        st.title(self.titulo)  # Exibe o título na página
        st.write(self.mensagem)  # Exibe uma mensagem na página

        self.navbar()

    def limpa_estado(self):
        """
        Limpa o estado do log quando o botão de limpar log é pressionado.

        Exibe um botão de "Limpar Log" na barra lateral. Se pressionado, limpa o histórico de logs na sessão.
        """
        if st.sidebar.button("🗑️ **Limpar Log**", use_container_width=True):
            st.session_state.log = []  # Limpa o estado do log
            st.success("O estado do log foi limpo!")

    def navbar(self):
        """
        Cria a barra de navegação e gerencia as páginas disponíveis no aplicativo.

        Exibe a barra lateral com os botões para navegar entre as páginas da aplicação.
        Inclui as páginas 'inicial', 'gráficos' e 'MQTT'.
        """
        st.sidebar.title("Projeto AI URA")

        # Renderização personalizada para a navegação
        paginas = {
            "inicial": "Página Inicial",
            "graficos": "Gráficos",
            "MQTT": "MQTT",
        }

        for key, label in paginas.items():
            if st.session_state.pagina == key:
                st.sidebar.markdown(f"**⏺︎ {label}**")  # Página ativa com destaque
            else:
                if st.sidebar.button(label, key=key):
                    st.session_state.pagina = key

        # Adiciona o botão para limpar o estado do log
        self.limpa_estado()

        # Renderizar o conteúdo com base na página selecionada
        if st.session_state.pagina == 'inicial':
            self.renderiza_pagina_inicial()
        elif st.session_state.pagina == 'graficos':
            self.renderiza_graficos()
        elif st.session_state.pagina == 'MQTT':
            self.renderiza_mqtt()

    def renderiza_pagina_inicial(self):
        """
        Renderiza a página inicial, exibindo uma imagem de boas-vindas.

        Exibe uma imagem como introdução à aplicação na página inicial.
        """
        st.image('IA URA.jpeg')

    def renderiza_graficos(self):
        """ 
        Função responsável por gerar e exibir gráficos utilizando matplotlib.
        O gráfico é gerado com a função np.sin() e exibido com o Streamlit usando st.pyplot(fig).
        Não há parâmetros de entrada ou valor retornado.
        """
        
        st.write('Página de gráficos')

        # Exemplo de gráfico com matplotlib
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        fig, ax = plt.subplots()
        ax.plot(x, y, label='Seno')
        ax.set_xlabel('Eixo X')
        ax.set_ylabel('Eixo Y')
        ax.set_title('Gráfico de Seno')
        ax.legend()

        # Exibindo o gráfico no Streamlit
        st.pyplot(fig)

    def renderiza_mqtt(self):
        """ 
        Função responsável por exibir o histórico de comandos do MQTT.
        Lê o arquivo de log e exibe o histórico de comandos e o último comando enviado.
        Caso ocorra algum erro ao ler o arquivo, uma mensagem de erro é exibida.
        """
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
        col1, col2 = st.columns([1, 1])

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

        # Atualiza a página automaticamente
        self.autorefresh = st_autorefresh(interval=2000, key="mqtt")

def main():
    """
    Função principal que cria uma instância da classe Aplicativo e inicia a aplicação.
    """
    # Instância da classe
    app_instance = Aplicativo(
        titulo='Projeto AI URA',
        mensagem='Colaboratividade entre carrinho e drone usando inteligência artificial'
    )

if __name__ == "__main__":
    main()

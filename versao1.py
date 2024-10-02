
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain_community.document_loaders.chatgpt import ChatGPTLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader

from TRT4_JSON import *


st.set_page_config(page_title="LawBox", page_icon=(
    'logo.jpg'), layout='wide', initial_sidebar_state='expanded')

# INICIALIZANDO ===


def inicializacao():
    if not 'pagina_INICIAL' in st.session_state:
        # se ele iniciou e nao tem nada, fica aqui
        st.session_state.pagina_INICIAL = 'Home'
    if not 'TRT4' in st.session_state:
        st.session_state.TRT4 = ''


# MUNDANDO A PAGINA


def mudar_pagina(nome_pagina):
    st.session_state.pagina_INICIAL = nome_pagina


# PAGINA INICIAL ==
def pag_inicial():
    st.title('_Bem vindo ao LAWBOX seu assistente virtual!_')

    st.markdown('''
            LawBox é o seu assistente virtual jurídico personalizado, projetado para fornecer respostas precisas e confiáveis para suas perguntas sobre direito. Com uma vasta base de conhecimento jurídico e inteligência artificial avançada, LawBox está pronto para ajudá-lo a entender conceitos legais complexos, esclarecer dúvidas sobre processos judiciais e orientá-lo em questões legais.

    Desde perguntas sobre direito civil, penal, trabalhista até questões relacionadas à propriedade intelectual e empresarial, LawBox é sua fonte confiável de informações jurídicas acessíveis. Ele está disponível 24 horas por dia, 7 dias por semana, para oferecer suporte sempre que você precisar.

    Com uma interface amigável e intuitiva, LawBox torna a pesquisa jurídica fácil e acessível para todos, desde estudantes de direito até profissionais estabelecidos. Seja você um indivíduo buscando orientação legal ou uma empresa em busca de soluções jurídicas, LawBox está aqui para ajudar, oferecendo respostas precisas e relevantes, adaptadas às suas necessidades específicas.

    Não importa o quão complexa seja sua pergunta jurídica, LawBox está preparado para ajudá-lo a encontrar a resposta certa. Descubra uma nova maneira inteligente e eficiente de lidar com questões legais com LawBox - seu parceiro confiável no mundo jurídico.

    '''
                )

# TRT4 ============


def trt4():
    main_trt4_j()


# MAIN =============
def main():
    inicializacao()

    # Sidebar
    st.sidebar.image('logo.jpg')
    st.sidebar.divider()
    st.sidebar.button('PAGINA INICIAL', use_container_width=True,
                      on_click=mudar_pagina, args=('Home',))
    st.sidebar.button('TRT4', use_container_width=True,
                      on_click=mudar_pagina, args=('TRT4',))

    # troca de paginas
    if st.session_state.pagina_INICIAL == 'Home':
        pag_inicial()

    elif st.session_state.pagina_INICIAL == 'TRT4':
        trt4()


# executando
if __name__ == '__main__':
    main()

# IMPORTAÇÕES =========================
import streamlit as st
from langchain_community.vectorstores.faiss import FAISS
from dotenv import load_dotenv
from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters.json import RecursiveJsonSplitter
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI


# CARREGANDO CHAVE ====================


@st.cache_resource
def carregar_chave():
    load_dotenv()
    return load_dotenv


carregar_chave()


# CARREGANDO DOCUMENTO ================
@st.cache_resource
def carregar_dados():
    dados1 = 'database4'
    dados2 = 'database5'
    embeddings_model = OpenAIEmbeddings()
    db1 = FAISS.load_local(folder_path=dados1,
                           embeddings=embeddings_model,
                           allow_dangerous_deserialization=True)
    db2 = FAISS.load_local(folder_path=dados2,
                           embeddings=embeddings_model,
                           allow_dangerous_deserialization=True)
    db1.merge_from(db2)

    return db1


@st.cache_data
def retrieve_info(query):
    similar_response = carregar_dados().max_marginal_relevance_search(
        query, k=3, fetch_k=10)
    return [doc.page_content for doc in similar_response]


@st.cache_resource
def ML():
    llm = ChatOpenAI(temperature=0.2, model='gpt-4o-mini')
    return llm


template = '''
Você se chama LAWBOX é um assistente juridico que realiza pesquisas no documento apresentado e responde para advogados.
siga todas as regras:
1/ responda com base no documento, com no máximo 650 caracteres.
2/ Sempre dê a resposta com base na decisão com a data mais recente, de preferência do Pleno.
3/ sempre apresente a resposta da seguinte forma:
- coloque primeiro o número do processo, a data do julgamento e o link;
- explicação da decisão;
- mostre a ementa da decisão;
- Se houver decisão divergencia, apresente a decisão divergente, informe o número do processo e a data;
- No caso de várias decisões sobre o mesmo tema da pergunta, apresente, por fim, o número do processo das últimas 3 decisões.
4/ Se não houver resposta em seu banco de dados, responde que não tem a resposta perfeita para essa pergunta.
5/ Caso houver a pergunta sobre uma lista de decisões recentes sobre um tema específico, liste as últimas 10 decisões sobre o tema perguntado, sendo que neste caso não precisa explicar a decisão, trazendo tão somente o número do processo.
Aqui esta a pergunta do advogado.
{message}
Aqui vai responder.
{best_practice}

Escreva a melhor resposta.
'''


@st.cache_resource
def prompt_funcao():
    prompt_template = PromptTemplate(
        input_variables=["message", "best_practice"],
        template=template
    )
    return prompt_template


# ainda posso mudar aqui
def chain_def():
    chain = LLMChain(llm=ML(), prompt=prompt_funcao())
    return chain


@st.cache_resource
def generate_response(message):
    best_practice = retrieve_info(message)
    response = chain_def().run(message=message, best_practice=best_practice)
    return response


def main_trt4_j():

    st.header("Escreve sua pergunta")
    message = st.text_area("pergunta do usuario")
    enviar = st.button(label='Perguntar')

    if enviar:
        st.write("gerando uma resposta")
        result = generate_response(message)
        st.info(result)

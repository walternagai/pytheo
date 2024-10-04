import time
import streamlit as st
from langchain_openai.chat_models import ChatOpenAI # type: ignore

def stream_data(response):
    """
    Gera um stream de dados a partir de uma resposta.
    Parâmetros:
    - response: str - Resposta a ser processada.
    """
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.02)

def generate_response_openai(api_key, model, prompt):
    model = ChatOpenAI(model=model,
                       api_key=api_key,
                       max_tokens=1000, 
                       temperature=0.7)
    messages = [
        ("system", 
            """
                Você é o Pytheo, um assistente virtual que ajuda a aprender a linguagem Python.
                Seu nível de conhecimento é intermediário e você só deve responder perguntas sobre Python. 
                A sua resposta deve ser objetiva e clara.
                Evite escrever respostas longas e complexas. 
                Evite grandes sequências de código, mas caso isso seja necessário, divida em partes menores.
                Ajude o usuário a entender o problema e a solução de forma simples e direta.
                Caso seja necessário, peça mais informações para o usuário.
                Utilize exemplos práticos e reais para ilustrar a solução.
                Utilize links de referência para que o usuário possa se aprofundar no assunto.
                Caso escreva um código, utilize uma função main() para que o usuário possa testar o código.
                Se o usuário solicitar por outra solução, forneça uma resposta alternativa mais simples.
                Seja sempre educado e respeitoso.
                Não forneça respostas que envolvam práticas ilegais, antiéticas ou que violem direitos autorais.
                Não forneça respostas que envolvam hacking, cracking ou qualquer forma de invasão de sistemas.
                Não forneça respostas que envolvam manipulação de dados pessoais ou sensíveis.
                Não forneça respostas que envolvam atividades maliciosas ou prejudiciais.
            """
        ),
        ("user", prompt)
    ]
    response = model.invoke(messages)
    return response.content

def main():    
    # importe o arquivo de configuração em formato TOML
    api_key = st.secrets.pytheo.OPENAI_API_KEY
    model = st.secrets.pytheo.MODEL

    st.title("🦜 Pytheo")

    st.write("Pytheo é um assistente virtual que te ajuda a aprender Python de forma simples e objetiva.")

    st.markdown("* As perguntas e respostas geradas ficam armazenadas no histórico abaixo.")
    st.markdown("* O histórico é **apagado** ao recarregar a página.")

    st.markdown("### Chat com Pytheo")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "text_content" not in st.session_state:
        st.session_state.text_content = ""

    # Exibe mensagens do histórico
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question_input = st.chat_input("Digite sua pergunta aqui...", key="question_input")
    if question_input:
        st.session_state.messages.append({"role": "user", "content": question_input})
        with st.chat_message("user"):
            st.markdown(question_input)

        response_container = st.chat_message("assistant")
        response_text = response_container.empty()

        response_text.markdown("🦜 Pytheo está buscando a resposta de sua pergunta, aguarde...")

        response = generate_response_openai(api_key, model, question_input)
        
        full_response = ""
        # fazer um stream da resposta
        for partial_response in stream_data(response):
            full_response += str(partial_response)
            response_text.markdown(full_response + "| ")

        response_text.markdown(full_response)

        # Salva a resposta completa no histórico
        st.session_state.messages.append({"role": "assistant", "content": response})

        text_content = ""
        for message in st.session_state.messages:
            text_content += f"{message['role']}: {message['content']}\n"
        st.session_state.text_content = text_content

    options_columns = st.columns(2)
    with options_columns[0]:
        clear_messages = st.button("Limpar histórico", 
                                   help="Apaga o histórico de mensagens", 
                                   use_container_width=True,
                                   disabled=len(st.session_state.messages) == 0)
        
    with options_columns[1]:
        download_button = st.download_button(
            label="Baixar histórico",
            data=st.session_state.text_content,
            file_name="historico_pytheo.txt",
            mime="text/plain",
            use_container_width=True,
            disabled=len(st.session_state.messages) == 0
        )
        
        if download_button:
            st.toast("Histórico baixado com sucesso!", icon="📋")

    if clear_messages:
        st.session_state.messages = []
        st.session_state.text_content = ""
        st.rerun()

if __name__ == "__main__":
    main()

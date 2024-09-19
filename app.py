import streamlit as st
import toml
from langchain_openai.chat_models import ChatOpenAI

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
            Seja sempre educado e respeitoso."""
        ),
        ("user", prompt)
    ]
    response = model.invoke(messages)
    return response.content

def main():    
    # importe o arquivo de configuração em formato TOML
    enterprise = st.secrets.pytheo.ENTERPRISE
    api_key = st.secrets.pytheo.OPENAI_API_KEY
    model = st.secrets.pytheo.MODEL

    st.title("🦜 Pytheo")

    st.write("Pytheo é um assistente virtual que te ajuda a aprender Python de forma simples e objetiva.")

    st.markdown("""
                ### Aviso de Privacidade\n
                * Este aplicativo não armazena suas perguntas e respostas.\n
                * Evite perguntas ofensivas ou que possam violar a privacidade de outras pessoas.
    """)
    with st.form(key="my_form"):
        text = st.text_area("Escreva sua dúvida da linguagem Python:")
        submitted = st.form_submit_button("Enviar")
        if submitted:
            st.write("🦜 Pytheo diz:")
            if enterprise == "openai":
                response = generate_response_openai(api_key, model, text)
                st.write(response)

if __name__ == "__main__":
    main()

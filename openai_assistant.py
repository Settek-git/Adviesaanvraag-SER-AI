import streamlit as st
import openai
import time
import os

#https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
assistent_id = st.secrets["ASSISTENT_ID"]
    
client = openai.OpenAI()

def get_assistant_response(assistant_id, thread, message_content):

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message_content
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )
    status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    while status.status != "completed":
        time.sleep(5)
        print("waiting for response")
        status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
        limit=10
    )
    return messages.data[0].content[0].text.value    

def main():
    # https://github.com/SagarDangal/openai_assistant_chat

    st.title("Text Chat for Adviesaanvraag SER AI")

    thread = client.beta.threads.create()

    # Text chat
    user_input = st.text_input("User: ")

    if st.button("Send"):
        #create a thread
        response = get_assistant_response(assistent_id, thread, user_input)
        st.write(f"Assistant: {response}")
        
if __name__ == "__main__":
    main()

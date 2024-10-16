import streamlit as st
from langchain_openai import AzureChatOpenAI

#Initialize LLM using AzureChat
llm = AzureChatOpenAI(
    openai_api_version = st.secrets["AZURE_OPENAI"]["AZURE_OPENAI_API_VERSION"],
    azure_endpoint= st.secrets["AZURE_OPENAI"]["AZURE_OPENAI_ENDPOINT"],
    api_key= st.secrets["AZURE_OPENAI"]["AZURE_OPENAI_APIKEY"],
    azure_deployment= st.secrets["AZURE_OPENAI"]["DEPLOYMENT_NAME"],
    temperature=1,
    model= st.secrets["AZURE_OPENAI"]["DEPLOYMENT_NAME"]
)

st.set_page_config(page_title="ChatBot", page_icon= ":books:")
st.title(":books: AskNarelle")
# st.header("This is a header")
# st.markdown("Hello world :sunglasses:")
with st.sidebar:
    st.header("Profile")
    gender = st.radio(
        label = "Gender",
        options = ("Male", "Female")
    )
    if gender == "Male":
        st.header("Welcome guys :boy:")
    else:
        st.header("Welcome Girls :girl:")


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Hardcoded responses
hardcode_responses = {
    "hello": "Hello! How can I help you today?",
    "how are you?": "I'm a chatbot, What can I help you?",
    "what is your name?": "I'm a simple chatbot.",
    "bye": "Goodbye! Have a great day!",
}


from langchain_core.prompts.chat import ChatPromptTemplate

# Get user input
prompt = st.chat_input("Tell me something...")
if prompt:
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    chat_history = [
        {"role" : m["role"] , "content" : m["content"]}
        for m in st.session_state.messages
    ]
    print("Hist",chat_history)
    # chat_prompt = [(m["role"] , m["content"]) for m in st.session_state.messages]
    # print("prompt",chat_prompt)
    chat_template = ChatPromptTemplate.from_messages([(m["role"] , m["content"]) for m in st.session_state.messages])

    prompt_messages = chat_template.format_messages()
    # Generate a hardcoded response based on user input
    response = llm.invoke(prompt_messages)
    response_content = response.content
    # Display assistant message in chat message container
    responder_role = "counter_lady"
    with st.chat_message("assistant"):
        st.markdown(response_content)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

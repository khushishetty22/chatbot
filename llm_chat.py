import streamlit as st
import cohere

# Initialize session states for API key, messages, and API key validation status
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = None

st.title("Chatbot with Cohere")

# Step 1: Ask for the Cohere API Key if it's not entered yet
if not st.session_state.api_key_valid:
    st.session_state.api_key = st.text_input("Enter your Cohere API Key", type="password")

    # Step 2: Validate the API key on user input
    if st.session_state.api_key:
        try:
            # Attempt a basic API call to test the key
            co = cohere.Client(st.session_state.api_key)
            response = co.generate(  # Minimal generate call to test the key
                model='command-xlarge-nightly',
                prompt="Test",
                max_tokens=1,
            )
            
            # If valid, set the key as valid
            st.session_state.api_key_valid = True
            st.success("API Key is valid! You can start chatting now.")
        except Exception:
            st.session_state.api_key_valid = False
            st.error("Invalid API Key. Please try again.")

# Proceed only if the API key is valid
if st.session_state.api_key_valid:
    co = cohere.Client(st.session_state.api_key)

    # Display initial assistant message when the app loads
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.write("Hello, how can I assist you today?")

    # Display all chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input box at the bottom
    prompt = st.chat_input("Ask anything")

    # If the user has entered a prompt, process it
    if prompt:
        # Display user's message in the chat
        with st.chat_message("user"):
            st.markdown(prompt)

        # Save user's message to the session state
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Create conversation history prompt for Cohere
        conversation_history = "\n".join(
            [f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages]
        ) + "\nAssistant:"

        try:
            # Call Cohere's generate API with conversation history
            response = co.generate(
                model='command-xlarge-nightly',
                prompt=conversation_history,
                max_tokens=100,
                temperature=0.7
            )
            assistant_response = response.generations[0].text.strip()

        except Exception as e:
            assistant_response = f"Error: {str(e)}"

        # Display the assistant's response in the chat
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        # Save assistant's message to the session state
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

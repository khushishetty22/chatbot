import streamlit as st

# Initialize session state for chat history and input
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

# Handle chat input
def handle_input():
    if st.session_state.user_input:
        bot_response = f"Thank you for telling me '{st.session_state.user_input}'"
        st.session_state["chat_history"].append(("User", st.session_state.user_input))
        st.session_state["chat_history"].append(("Bot", bot_response))
        st.session_state.user_input = ""  # Clear the input field

# Layout the app
st.title("Chat Interface")

# Display the chat history
st.write("### Chat History")
for sender, message in st.session_state["chat_history"]:
    if sender == "User":
        st.write(f"**User:** {message}")
    else:
        st.write(f"**Bot:** {message}")

# Display the chat input field at the bottom
st.text_input("You: ", key="user_input", on_change=handle_input, placeholder="Type a message...")

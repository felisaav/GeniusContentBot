from openai import OpenAI
import streamlit as st

st.title("Genius Content Bot","Let's create the best content ever, through a conversation I can create a great content to improve your's company brand reputation")
st.markdown("Elevate your brand effortlessly with tailored, conversational content across diverse channels. Crafted for impact, simplicity, and authenticity",
           help="Make it uniquely yours! Customize the style, length, language, and all the fun stuff that speaks to your vibe. Let your content shine with your awesome personality!") 
st.markdown("""---""")

#sidebar
def reset_conversation():
  st.session_state.messages = []  # Clear the conversation
  st.session_state.conversation = None
  st.session_state.chat_history = None

st.sidebar.markdown('*Parameters*',help='Here you can reset and start a new conversation, or you can download your last answer')
st.sidebar.button('Start with a new content chat', on_click=reset_conversation)

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets.key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Define the system role and content
system_role = "assistant"
system_content = '''I manage and curate content for a company's social media, aiming to build a strong online presence, 
engage the audience, and establish the brand as an industry authority. The focus is on boosting visibility, addressing 
audience needs, and driving engagement through diverse content.'''

# Initialize messages with the system role and content
if "messages" not in st.session_state or not st.session_state.messages:
    st.session_state.messages = [{"role": system_role, "content": system_content}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What content do you want to generate?"):
  # Append user input to messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)
  
    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Append assistant response to messages
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # Add download button for the last response
    st.sidebar.download_button('Download Last Response', full_response)

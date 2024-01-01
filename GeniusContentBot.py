from openai import OpenAI
import streamlit as st

st.title("ChatGPT-like clone")

client = OpenAI(api_key=st.secrets.key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Define the system role and content
system_role = "assistant"
system_content = '''I manage and curate content for a company's social media, aiming to build a strong online presence, 
engage the audience, and establish the brand as an industry authority. The focus is on boosting visibility, addressing 
audience needs, and driving engagement through diverse content.'''

# Initialize messages with the system role and content
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": system_role, "content": system_content}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What content do you want to generate?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
    st.session_state.messages.append({"role": "assistant", "content": full_response})




'''
# Interactive loop for user feedback
user_feedback = ""
while True:
    # Print the current response content
    print(f"\nCurrent Response:\n{response_content}")

    # Prompt the user for feedback
    user_feedback = input("\nPlease provide your feedback or type 'done' if you are satisfied: ")

    if user_feedback.lower() == 'done':
        break  # Exit the loop if the user is satisfied

    # Update the response content based on user feedback
    response_content += f"\nUser Feedback: {user_feedback}\n"
    response_content = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        messages=[{"role": "system", "content": final_role},
                  {"role": "user", "content": response_content}]
    )["choices"][0]["message"]["content"].strip()

# Print the final response after user interaction
print(f"\nFinal Response:\n{response_content}")


# ### Now, since you have a text, you can customized to different platforms, to create a multichannel message

# In[13]:


# Function to generate content for a specific platform using GPT-3.5-turbo chat model
def generate_platform_content(prompt, max_characters=None):
    if max_characters:
        prompt += f". You have to limit the response to {max_characters} characters"
        
    prompt +="Return your output in {language}".format(language=input_3)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": final_role},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

# Function to customize content for different social media platforms
def customize_content(response_content, platform, max_characters=None):
    # Placeholder for platform-specific content
    platform_content = ""

    # Add platform-specific formatting
    if platform == "twitter":
        prompt = f"Generate a Twitter-friendly version:\n{response_content}"
        platform_content = generate_platform_content(prompt, 240)  
    elif platform == "linkedin":
        prompt = f"Generate a LinkedIn-friendly version:\n{response_content}"
        platform_content = generate_platform_content(prompt, max_characters)
    elif platform == "facebook":
        prompt = f"Generate a Facebook-friendly version:\n{response_content}"
        platform_content = generate_platform_content(prompt, max_characters)
    elif platform == "instagram":
        prompt = f"Generate an Instagram-friendly version:\n{response_content}"
        platform_content = generate_platform_content(prompt, max_characters)

    return platform_content


# Example usage
#platforms = ["twitter", "linkedin", "facebook", "instagram"]
#for platform in platforms:
#    platform_specific_content = customize_content(response_content, platform)
#    print(f"\nContent for {platform.capitalize()}:\n{platform_specific_content}")


'''



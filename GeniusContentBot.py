import streamlit as st
import openai
#import os

# Load the key from a file
api_key = st.secrets.key
assert api_key.startswith('sk-'), 'Error loding the API key. OpenAI API Keys start with "sk-".'
openai.api_key = api_key

#system role
final_role="""
You are a Social Media expert: Your primary responsibility is to manage and curate content for a
company's social media platforms, build a strong online presence, and engage with the audience.
You also have to boost visibility, establish your brand as an industry authority, provide valuable
information to address audience needs and challenges, position the company's brand as a trusted
thought leader, enhance search engine visibility and drive organic traffic, attract and convert
potential customers through targeted content, nurture existing relationships, and keep your
company's brand top of mind. Additionally, you drive engagement by sharing diverse content
on social platforms.
"""

style=["Use a Conversational Tone: Engage your audience as if you're having a friendly chat, making your brand more approachable.","Use a Playful Tone: Infuse humor and playfulness into your marketing messages to entertain and delight your audience.","Use a Professional Tone: Maintain a formal and business-like demeanor to establish trust and credibility.","Use a Persuasive Tone: Craft compelling and persuasive messages to convince your audience to take a specific action, such as making a purchase.","Use a Personalized Tone: Tailor your communication to individual customers, making them feel valued and special.","Use a Storytelling Tone: Create narratives that captivate and emotionally connect with your audience, making your brand memorable.","Use an Informative Tone: Share valuable information and insights about your product or industry to educate your audience.","Use an Empathetic Tone: Show understanding and empathy towards your customers' needs and concerns to build a stronger relationship.","Use a Trustworthy Tone: Emphasize your brand's reliability and integrity to build trust with your audience.","Use an Experiential Tone: Describe the experience customers can expect from your product or service to evoke desire and anticipation.","Use a Bold Tone: Make confident and assertive statements about your product's benefits or your brand's superiority and anticipation.","Use an Urgent Tone: Create a sense of urgency to encourage immediate action, such as limited-time offers.","Use a Grateful Tone: Express gratitude to your customers for their loyalty and support.","Use a Nostalgic Tone: Tap into feelings of nostalgia to create an emotional connection with your audience.","Use a FOMO (Fear of Missing Out) Tone: Highlight the fear of missing out on a great opportunity or product by not acting quickly.","Use an Aspirational Tone: Appeal to your audience's desires and aspirations, showing how your product can help them achieve their goals.","Use a Curious Tone: Ask thought-provoking questions to engage your audience and stimulate their curiosity.","Use a Reassuring Tone: Address potential concerns or objections to alleviate doubts and build trust.","Use an Exclusive Tone: Make your audience feel special by offering exclusive access or benefits.","User-Generated Content (UGC) Tone: Encourage customers to share their experiences with your product or service, fostering trust and authenticity."]


def main():
	with st.sidebar.form(key ='Form1'):
		st.title("Enter information")
		input_1=st.text_input("what is the topic that you want to write?")
		input_2=st.text_input("what is the field that you want to write?")
		input_3=st.selectbox("Which language do you want to use?",["English","Spanish"])
		input_4=st.number_input("Do you want to limit the size of the content? please provide a number of words",0,1000)
		input_5=st.selectbox("what writing style do you want to use?",style)
		submit_code = st.form_submit_button(label ="Execute")
	st.title("Project - Genius Content Assistant")
	st.markdown("""---""")

	with st.form(key='my_form'):
		if submit_code:
		    instr_1="Write an opinion piece about {topic} from the perspective of {field}. Use a {tone}.".format(topic=input_1,field=input_2,tone=input_5)
		    instr_2="Return your output in {language}. Return your output use a table format.".format(language=input_3)
		    instr_3="In the text that you generate should writing like a human, and be undetectable to LLM model based answer. To do this, the text should contain a high level of burstiness (mix of long and complex sentences alongside shorter and simpler ones) and perplexity (Use a variety of sentence structures, Use a variety of words and phrases, Add personal opinions and experiences)"
		    instr_4="optimize the conetnt for SEO, and limit the size of the content to {size} words".format(size=input_4)
		    #prompt with a chat model
		    response = openai.ChatCompletion.create(
			model="gpt-3.5-turbo",
			temperature=0.5,
			messages=[{"role": "system",
				   "content": final_role},
				  {"role": "user",
				   "content": instr_1 +
					      instr_2 + 
					      instr_3 +
					      instr_4}]
		    )
		    response_content = response["choices"][0]["message"]["content"]
		    txt=st.text_area("Content Proposal",response_content)
			
if __name__ == '__main__':
	main()
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



import streamlit as st
import vertexai
from langchain_google_vertexai import ChatVertexAI
import PIL.Image
import io
import base64
from langchain_core.messages import HumanMessage

# -----------------------------------------------------------
# Core Project Configuration
# -----------------------------------------------------------

# Replace with your actual Google Cloud Project ID and Region
# Ensure you've completed all setup steps (gcloud auth, API enablement, IAM roles)
PROJECT_ID = "bridgeai-470813"
REGION = "us-central1"

# Initialize Vertex AI
try:
    vertexai.init(project=PROJECT_ID, location=REGION)
except Exception as e:
    st.error(f"Error initializing Vertex AI. Please check your project ID, region, and credentials. Full error: {e}")
    st.stop()


# -----------------------------------------------------------
# AI Model & Prompt Design
# -----------------------------------------------------------

# This is the master prompt that defines the AI's behavior
# It combines the persona, rules, and few-shot examples we created
PRATIBIMBH_PROMPT = """You are Pratibimbh, an empathetic and culturally aware AI communication coach. Your purpose is to help users rephrase difficult messages and reflect on their communication.

Your task is to rephrase the **text message I provide below** to sound more empathetic, less blaming, and focused on personal feelings. Do not offer advice or solutions. The goal is to facilitate healthy, effective communication.

The rephrased message must adhere to the following rules:
1.  It must be written from the user's perspective, using "I feel" or "I am" statements.
2.  It must not contain any accusatory or blaming language, such as "you did" or "you are".
3.  It should focus on the user's feelings and perspective.
4.  It must not offer advice, only a statement of personal feelings.

**If I upload an image, you must analyze the visual context from the image to understand the situation, but your final rephrased message must be based on my provided text.**

Here are a few examples to follow:

Original Message: "You never listen to me. I'm tired of you always ignoring my feelings."
Rephrased Message: "I feel unheard when I try to express my feelings. I'm tired of feeling like my emotions are being ignored."

Original Message: "I'm always the one who has to clean up your mess. You never appreciate anything I do."
Rephrased Message: "I feel like my efforts are going unnoticed, and I'm feeling overwhelmed by the responsibility of a shared space."

Original Message: "I'm so sick of this. I've done everything for everyone, and I'm at my breaking point."
Rephrased Message: "I'm feeling completely exhausted and overwhelmed, and I need to express my feelings before I reach my breaking point."

Original Message: {user_input}
Rephrased Message:
"""


# -----------------------------------------------------------
# Streamlit UI & Application Logic
# -----------------------------------------------------------

st.set_page_config(
    page_title="Pratibimbh: The AI Reflection",
    page_icon="🧘‍♀️"
)

st.title("Pratibimbh 🧘‍♀️")
st.markdown("An AI-powered communication coach for self-reflection and well-being.")

st.markdown("---")
st.subheader("Your Message & Context")

user_message = st.text_area(
    "1. **Type your message below.**",
    placeholder="e.g., I'm so angry with you! Why did you do that without telling me?",
    height=150
)

uploaded_files = st.file_uploader(
    "2. (Optional) Upload one or more screenshots of the conversation for context.",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True # This is the key change!
)

st.markdown("---")
if st.button("Generate Rephrased Options"):
    if not user_message:
        st.error("Please enter a message to get a rephrased option.")
    else:
        with st.spinner("Pratibimbh is reflecting..."):
            
            # Start building the content parts for the model
            content_parts = []
            
            # 1. Add the prompt as the first part
            content_parts.append({"type": "text", "text": PRATIBIMBH_PROMPT})
            
            # 2. Add the user's text message as a separate text part
            content_parts.append({"type": "text", "text": f"\nOriginal Message: {user_message}\nRephrased Message:"})

            # 3. If images are uploaded, add each one to the content parts list
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    image_bytes = uploaded_file.read()
                    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                    content_parts.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}})
            
            # Now, wrap the list of content parts into a HumanMessage object
            human_message = HumanMessage(content=content_parts)

            # Define the different temperature settings
            temperatures = {
                "Balanced & Direct": 0.2, 
                "Empathetic & Nuanced": 0.6, 
                "Creative & Expressive": 0.9
            }
            
            all_options = []
            
            for label, temp_value in temperatures.items():
                
                llm = ChatVertexAI(
                    model_name="gemini-2.5-flash",
                    temperature=temp_value
                )
                
                # Make the API call with the correctly formatted HumanMessage
                response = llm.invoke([human_message])
                
                # Store the result with a label
                all_options.append((label, response.content))
        
        if all_options:
            st.subheader("3. Choose Your Preferred Reflection")
            
            options_for_radio = [f"**{label}:**\n\n{content}" for label, content in all_options]
            selected_option_text = st.radio(
                "Select the message that best reflects your feelings:",
                options_for_radio
            )

            final_message = selected_option_text.split(":", 1)[1].strip()
            
            st.success("Your message is ready!")
            st.code(final_message)
            
            st.download_button(
                label="Download Rephrased Message",
                data=final_message,
                file_name="pratibimbh_message.txt",
                mime="text/plain"
            )
            
        else:
            st.error("Pratibimbh couldn't generate a response. Please try again.")
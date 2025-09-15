import streamlit as st
import vertexai
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage, SystemMessage
from PIL import Image
import io

# Initialize Vertex AI with supported region
vertexai.init(project="bridgeai-470813", location="us-east1")

# Use the up-to-date Gemini model
llm = ChatVertexAI(
    model="gemini-2.5-flash",  # Latest stable fast model
    project="bridgeai-470813",
    location="us-east1",
    temperature=0.2,
)

# Streamlit UI
st.set_page_config(layout="wide")
st.title("Bridge AI 🤝")
st.markdown("Rephrase your thoughts to build bridges, not walls.")
st.divider()

# Text Rephraser
st.subheader("Text Rephraser")
user_message = st.text_area("Enter a message you want to rephrase:")

if st.button("Rephrase Message"):
    if user_message:
        with st.spinner("Rephrasing..."):
            response = llm.invoke([
                SystemMessage(content=(
                    """You are an empathetic communication assistant. Your task is to rephrase a message from a user to a person they are in conflict with.

                    The rephrased message must adhere to the following rules:
                    1.  It must be written from the user's perspective, using \"I feel\" or \"I am\" statements.
                    2.  It must not contain any accusatory or blaming language, such as \"you did\" or \"you are\".
                    3.  It should focus on the user's feelings and perspective.
                    4.  It must not offer advice, only a statement of personal feelings.

                    Here are a few example to follow:

                    Original Message: \"You never listen to me. I'm tired of you always ignoring my feelings.\"
                    Rephrased Message: \"I feel unheard when I try to express my feelings. I'm tired of feeling like my emotions are being ignored.\"

                    Original Message: \"I'm always the one who has to clean up your mess. You never appreciate anything I do.\"
                    Rephrased Message: \"I feel like my efforts are going unnoticed, and I'm feeling overwhelmed by the responsibility of a shared space.\"

                    Original Message: \"Why do you always have to tell me what to do? You treat me like a child and I can't stand it.\"
                    Rephrased Message: \"I feel like my decisions aren't being trusted, and I'm struggling with a feeling of being controlled.\"

                    Original Message: \"You never have time for me. It's like I'm not important to you anymore.\"
                    Rephrased Message: \"I've been feeling disconnected from you, and I miss spending quality time together. I'm afraid that I'm not as important to you as I used to be.\"

                    Original Message: \"I'm so sick of this. I've done everything for everyone, and I'm at my breaking point.\"
                    Rephrased Message: \"I'm feeling completely exhausted and overwhelmed, and I need to express my feelings before I reach my breaking point.\""""
                )),
                HumanMessage(content=user_message)
            ])
            st.subheader("Your New Message:")
            st.markdown(f"**{response.content}**")

st.divider()

# Multimodal RAG (Image + Text)
st.subheader("Family Album Insight (Multimodal Analysis)")
st.markdown("Upload a photo to get a thoughtful conversation starter.")
uploaded_file = st.file_uploader(
    "Upload a family photo",
    type=["png", "jpg", "jpeg"],
    label_visibility="collapsed"
)

if uploaded_file:
    image_data = uploaded_file.read()
    image = Image.open(io.BytesIO(image_data))
    st.image(image, use_column_width=True)
    st.success("Photo uploaded.")

    prompt_for_image = st.text_area("What conversation would you like to have about this photo?")

    if st.button("Get Multimodal Conversation Starter") and prompt_for_image:
        with st.spinner("Generating conversation starter..."):
            multimodal_response = llm.invoke([
                SystemMessage(content=(
                    "You are an empathetic assistant helping families connect over their photos."
                )),
                HumanMessage(content=[
                    {"type": "text", "text": prompt_for_image},
                    {"type": "image_bytes", "data": image_data, "mime_type": "image/jpeg"}
                ])
            ])
            st.subheader("Conversation Starter:")
            st.markdown(f"**{multimodal_response.content}**")
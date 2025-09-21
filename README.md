# Pratibimbh: An AI Communication Coach for Youth Mental Wellness

### **Project by:** Team [Your Team Name]

## 💡 **Inspiration & Problem Statement**

In a world driven by digital communication, Indian youth often face social and emotional challenges when navigating difficult conversations. The stigma around seeking mental health support, combined with the lack of tools to communicate feelings constructively, leads to heightened anxiety and unresolved conflicts. Pratibimbh was created to address this gap by providing a private, non-judgmental space to reflect on and rephrase messages.

## ✨ **Features**

* **Multimodal Communication Analysis:** Our key innovation. Pratibimbh uses a multimodal AI model to analyze the visual context from conversation screenshots, allowing it to understand the full tone and flow of a dialogue.
* **Context-Aware Rephrasing:** It intelligently rephrases emotionally charged, accusatory messages into empathetic "I-statements," promoting healthier communication habits.
* **Multiple Rephrasing Options:** The user is provided with three distinct rephrasing options—Balanced, Empathetic, and Creative—empowering them to choose the tone that best reflects their feelings.
* **Confidential & Secure:** The application offers a private platform for self-reflection, ensuring user data is not stored, thus building trust and encouraging honest emotional expression.
* **Scalable Architecture:** Built on a modern serverless stack, the prototype is ready for wider adoption and can scale to meet the demands of a large user base.

## ⚙️ **How It Works**

1.  **User Input:** The user uploads a screenshot of a conversation and types their message.
2.  **Multimodal Analysis:** The application sends both the text and the image to the **Google Gemini 1.5 Pro API** via LangChain.
3.  **Contextual Rephrasing:** The AI model analyzes the visual context from the screenshot to understand the background of the conflict.
4.  **Generates Options:** The AI generates three unique rephrased messages at different `temperature` settings.
5.  **User Chooses:** The user selects the best rephrased message and can copy it to use in their conversation.

## 💻 **Technical Stack**

* **Generative AI:** Google Vertex AI, Gemini 1.5 Pro
* **Frontend:** Streamlit
* **Backend & Hosting:** Google Cloud Run
* **Frameworks:** LangChain
* **Libraries:** PIL, `base64`

## 🚀 **Getting Started (Local Development)**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your_username/pratibimbh.git](https://github.com/your_username/pratibimbh.git)
    cd pratibimbh
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up Google Cloud Credentials:** Ensure you have the necessary authentication set up for Vertex AI. You may need to run `gcloud auth application-default login`.
5.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 🌐 **Deployment**

The prototype is deployed on **Google Cloud Run**, providing a serverless and scalable solution.

## 🛣️ **Future Roadmap**

* **User Authentication:** Implementing secure user accounts with Firebase.
* **Session History:** Storing rephrased conversations (with user consent) for future reflection and journaling.
* **Multilingual Support:** Expanding to support multiple Indian languages to reach a wider audience.
* **Voice-to-Text Feature:** Allowing users to speak their message for an even more intuitive experience.

---
**Thank you for your consideration.**
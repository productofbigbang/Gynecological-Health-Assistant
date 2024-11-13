


# 🏥 Gynecological Health Assistant

This repository contains a **Gynecological Health Assistant** built using **Gradio** and **Google's Generative AI**, which provides general health information related to gynecology. This AI-powered chatbot can answer questions, provide relevant medical context, and guide users on various topics such as menstrual health, pregnancy, and more. It is designed to be empathetic and informative but is not a substitute for professional medical advice.

## Features

- **Interactive Chatbot**: Users can ask health-related questions, and the chatbot provides responses based on the knowledge base.
- **Patient Information Input**: Users can input their age, height, and weight to personalize the responses.
- **Relevant Medical Context**: The assistant retrieves relevant medical information from a pre-loaded Wikipedia dataset on gynecology.
- **Clear Disclaimer**: The assistant clearly states that it is not a substitute for professional medical advice.
- **Customizable UI**: The interface includes custom CSS for styling and a user-friendly layout.

## How It Works

1. **Data Loading**: The assistant loads gynecological data from a pre-scraped Wikipedia dataset (`wikipedia_gynecology_data.json`).
2. **Embedding Generation**: It uses the `SentenceTransformer` model (`all-MiniLM-L6-v2`) to generate embeddings for the knowledge base.
3. **Context Retrieval**: When a user asks a question, the assistant retrieves relevant context using cosine similarity between the query and the knowledge base embeddings.
4. **Response Generation**: The chatbot generates responses using Google's `GenerativeModel` with the `gemini-pro` model.
5. **Conversation History**: The assistant maintains conversation history to provide context in ongoing interactions.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/gynecological-health-assistant.git
   cd gynecological-health-assistant
   ```

2. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   
   - Create a `.env` file in the root directory with your Google Generative AI API key:

     ```
     API_KEY=your_google_genai_api_key_here
     ```

4. Ensure you have the Wikipedia data file (`wikipedia_gynecology_data.json`) in the project directory.

## Usage

1. Run the application:

   ```bash
   python app.py
   ```

2. The Gradio interface will launch, and you can access it through your browser.

3. Input your age, height, and weight, then type your health-related question in the chatbox.

4. Example questions:
   - "What are common symptoms of PCOS?"
   - "How often should I get a pap smear?"
   - "What are normal menstrual cycle lengths?"

5. Clear the conversation history at any time using the "Clear Chat" button.

## Example Interface

The interface includes:
- A section for entering patient information (age, height, weight).
- A chat interface where users can ask questions.
- Example questions to guide users on what they can ask.
- Disclaimers about the chatbot's limitations.



## Important Notes

- This AI assistant provides general health information only.
- It is not intended to replace professional medical advice or diagnosis.
- Always consult healthcare providers for medical decisions.
- For emergencies, contact emergency services immediately.

## Customization

You can modify the chatbot's behavior by:
- Changing the Wikipedia dataset used for knowledge retrieval.
- Adjusting the prompt used in `generate_response()` to alter how the assistant responds.
- Customizing the UI with different themes or CSS styles.

## License

This project is licensed under the MIT License.
```


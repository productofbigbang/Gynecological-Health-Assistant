


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

## Performance Metrics
To measure the performance of your **Gynecological Health Assistant chatbot**, you can use a variety of metrics that assess both the **technical efficiency** and **user experience**. Here are some key performance indicators (KPIs) that you can track:

## 1. **Response Accuracy**
   - **Definition**: Measures how often the chatbot provides correct and relevant answers to user queries.
   - **How to Measure**: You can manually review conversations or use feedback from users to determine if the responses were accurate based on the provided context.
   - **Importance**: High response accuracy ensures that the chatbot is providing valuable information, which is critical for health-related inquiries.

## 2. **User Satisfaction (CSAT)**
   - **Definition**: Measures how satisfied users are with their interaction with the chatbot.
   - **How to Measure**: Use post-chat surveys, star ratings, or emoticons to gather feedback from users after each conversation.
   - **Importance**: Helps assess the overall user experience and identify areas for improvement in conversational flow or response quality.

## 3. **Goal Completion Rate (GCR)**
   - **Definition**: Tracks how often users successfully complete their intended task, such as getting a satisfactory answer to a health-related question.
   - **How to Measure**: Monitor whether users receive relevant answers or are able to resolve their queries without needing human intervention.
   - **Importance**: A high GCR indicates that the chatbot is effectively fulfilling its purpose.

## 4. **Average Response Time**
   - **Definition**: Measures how quickly the chatbot responds to user queries.
   - **How to Measure**: Track the time between when a user submits a question and when they receive a response.
   - **Importance**: Fast response times are crucial for maintaining user engagement and satisfaction, especially in healthcare contexts where timely information is important.

## 5. **Conversation Duration**
   - **Definition**: The average length of time users spend interacting with the chatbot.
   - **How to Measure**: Track the total duration of each conversation session.
   - **Importance**: A balance is necessary—too short may indicate insufficient engagement, while too long could suggest inefficiency in resolving queries.

## 6. **Missed Utterances / Non-response Rate**
   - **Definition**: Tracks how often the chatbot fails to understand or respond appropriately to user queries.
   - **How to Measure**: Monitor instances where users receive fallback responses like "I don’t understand" or where no relevant context is retrieved.
   - **Importance**: A high non-response rate indicates gaps in the chatbot's Natural Language Processing (NLP) capabilities, requiring improvements in training data or response logic.

## 7. **Human Takeover Rate**
   - **Definition**: Measures how often the chatbot needs to escalate issues to a human agent for resolution.
   - **How to Measure**: Track instances where users request or are directed to human support due to unresolved queries.
   - **Importance**: A low takeover rate suggests that the chatbot is handling most queries effectively on its own

## 8. **Retention Rate**
   - **Definition**: Tracks how many users return to interact with the chatbot after their initial session.
   - **How to Measure**: Monitor repeat interactions from unique users over time.
   - **Importance**: A high retention rate indicates that users find value in interacting with the chatbot, which is crucial for long-term engagement.

   

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


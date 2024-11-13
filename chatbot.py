import gradio as gr
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables and configure API
load_dotenv()
genai.configure(api_key='Enter your API key here')
model = genai.GenerativeModel('gemini-pro')
conversation_history = []

# Load the scraped Wikipedia data
def load_wiki_data(filename='wikipedia_gynecology_data.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Initialize sentence transformer model for embeddings
encoder = SentenceTransformer('all-MiniLM-L6-v2')

# Prepare knowledge base
wiki_data = load_wiki_data()
knowledge_base = []
embeddings = []

# Process wiki data into chunks
for article in wiki_data:
    if 'introduction' in article:
        for intro_text in article['introduction']:
            knowledge_base.append({
                'content': intro_text,
                'source': article['title'],
                'type': 'introduction'
            })
    
    if 'sections' in article:
        for section_title, section_content in article['sections'].items():
            if 'text' in section_content:
                for text in section_content['text']:
                    knowledge_base.append({
                        'content': text,
                        'source': f"{article['title']} - {section_title}",
                        'type': 'section'
                    })

# Generate embeddings for all knowledge base entries
for entry in knowledge_base:
    embedding = encoder.encode(entry['content'], convert_to_tensor=False)
    embeddings.append(embedding)

embeddings = np.array(embeddings)

def retrieve_relevant_context(query, top_k=3):
    query_embedding = encoder.encode(query, convert_to_tensor=False)
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    relevant_contexts = []
    for idx in top_indices:
        relevant_contexts.append({
            'content': knowledge_base[idx]['content'],
            'source': knowledge_base[idx]['source'],
            'similarity': similarities[idx]
        })
    
    return relevant_contexts

def generate_response(age, height, weight, message, history):
    global conversation_history
    
    if not conversation_history:
        user_details = f"User Details - Age: {age}, Height: {height} cm, Weight: {weight} kg\n"
        conversation_history.append(user_details)
    
    relevant_contexts = retrieve_relevant_context(message)
    context_text = "\n\nRelevant medical information:\n"
    for ctx in relevant_contexts:
        context_text += f"- {ctx['content']}\n"
    
    prompt = """You are a professional and empathetic gynecological education chatbot. 
    Provide accurate, clear, and helpful responses based on the medical information provided.
    If you're unsure or if the question requires direct medical attention, advise consulting a healthcare provider.
    
    User details and conversation history:
    """
    prompt += "\n".join(conversation_history)
    prompt += f"\nUser: {message}"
    prompt += context_text
    prompt += "\nResponse:"

    try:
        response = model.generate_content(prompt)
        conversation_history.append(f"User: {message}")
        conversation_history.append(f"Assistant: {response.text}")
        return response.text
    except Exception as e:
        return f"I apologize, but I encountered an error. Please try rephrasing your question. Error: {str(e)}"

def format_response(age, height, weight, message, history):
    if not message.strip():
        return history, ""
    
    try:
        bot_response = generate_response(age, height, weight, message, history)
        
        if history is None:
            history = []
        
        # Using the correct tuple format for chatbot
        history.append([message, bot_response])
        
        return history, ""
    except Exception as e:
        if history is None:
            history = []
        history.append([message, f"Error: {str(e)}"])
        return history, ""

def clear_conversation():
    global conversation_history
    conversation_history = []
    return [], ""

# Custom CSS
custom_css = """
.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}
.main-header {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(to right, #d0a3d6, #d4a0db);
    border-radius: 10px;
    margin-bottom: 2rem;
}
.chat-container {
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.disclaimer {
    font-size: 0.8em;
    color: #666;
    text-align: center;
    margin-top: 1rem;
    padding: 0.5rem;
    background-color: #f5f5f5;
    border-radius: 5px;
}
"""

# Create custom theme
custom_theme = gr.themes.Base(
    primary_hue="teal",
    secondary_hue="blue",
    neutral_hue="slate",
    font=("Inter", "sans-serif")
)

# Create Gradio interface
with gr.Blocks(theme=custom_theme, css=custom_css) as demo:
    with gr.Column():
        gr.HTML("""
            <div class="main-header">
                <h1>🏥 Gynecological Health Assistant</h1>
                <p>Your trusted AI companion for gynecological health information</p>
            </div>
        """)
        
        with gr.Row():
            # Patient Information Column
            with gr.Column(scale=1):
                with gr.Group():
                    gr.Markdown("### 📋 Patient Information")
                    age = gr.Slider(
                        label="Age",
                        minimum=0,
                        maximum=120,
                        value=25,
                        step=1,
                        interactive=True
                    )
                    height = gr.Slider(
                        label="Height (cm)",
                        minimum=120,
                        maximum=220,
                        value=170,
                        step=1,
                        interactive=True
                    )
                    weight = gr.Slider(
                        label="Weight (kg)",
                        minimum=30,
                        maximum=200,
                        value=70,
                        step=1,
                        interactive=True
                    )
                
                with gr.Accordion("ℹ️ Important Information", open=False):
                    gr.Markdown("""
                        - This AI assistant provides general health information only
                        - Not a substitute for professional medical advice
                        - Always consult healthcare providers for medical decisions
                        - For emergencies, contact emergency services immediately
                    """)

            # Chat Interface Column
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(
                    value=[],
                    height=500,
                    show_label=False,
                    avatar_images=("👤", "👩‍⚕️"),
                    elem_classes="chat-container",
                    bubble_full_width=False
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        show_label=False,
                        placeholder="Type your health-related question here...",
                        container=False,
                        scale=8
                    )
                    submit_btn = gr.Button(
                        "Send",
                        variant="primary",
                        scale=1,
                        min_width=100
                    )
                
                with gr.Row():
                    clear_btn = gr.Button(
                        "🗑️ Clear Chat",
                        variant="secondary",
                        size="sm"
                    )

        # Example questions
        gr.Examples(
            examples=[
                "What are common symptoms of PCOS?",
                "How often should I get a pap smear?",
                "What are normal menstrual cycle lengths?",
                "What are the early signs of pregnancy?",
                "How can I manage menstrual cramps naturally?"
            ],
            inputs=msg,
            label="📝 Example Questions"
        )

        gr.HTML("""
            <div class="disclaimer">
                <p>⚠️ For medical emergencies, please call your local emergency services immediately.</p>
                <p>This AI assistant is for informational purposes only and should not be used for diagnosis or treatment.</p>
            </div>
        """)

    # Event handlers
    msg.submit(
        fn=format_response,
        inputs=[age, height, weight, msg, chatbot],
        outputs=[chatbot, msg]
    )
    
    submit_btn.click(
        fn=format_response,
        inputs=[age, height, weight, msg, chatbot],
        outputs=[chatbot, msg]
    )
    
    clear_btn.click(
        fn=clear_conversation,
        outputs=[chatbot, msg]
    )

if __name__ == "__main__":
    demo.launch(share=True)
from flask import Flask, render_template, request, jsonify
import google.generativeai as ai

# Configure the Gemini API
API_KEY = 'AIzaSyCA1fPpo59Z7X3k6hWymhIJP75r0QnNkJM'  # Replace with your real API key
ai.configure(api_key=API_KEY)

# Create a model and start a chat session
model = ai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

# Store conversation history
history = []

# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': "No message received"}), 400

    # Add user message to history
    history.append(f"User: {user_message}")

    # Send message to Gemini model
    response = chat.send_message('\n'.join(history))
    bot_message = response.text

    # Add response to history
    history.append(f"Chatbot: {bot_message}")

    return jsonify({'response': bot_message})

if __name__ == '__main__':
    app.run(threaded=False)


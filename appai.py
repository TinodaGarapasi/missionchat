#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, request, jsonify, render_template
from functools import lru_cache
import json
import os
import re
from openai import OpenAI

app = Flask(__name__)

# Route to serve the HTML interface
@app.route('/')
def index():
    return render_template('index.html')

# OpenAI API key
client = OpenAI(api_key="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")

@lru_cache(maxsize=1)
def get_context():
    return context

# Load JSON file once at startup
with open("Bcombined_data.json", "r", encoding="utf-8") as file:
    pdf_content = json.load(file)

# Flatten the nested dictionaries into a single string for context
context = []
for value in pdf_content.values():
    if isinstance(value, dict):
        context.append(' '.join(str(v) for v in value.values()))
    else:
        context.append(str(value))
context = "\n".join(context)
context = get_context()

@app.route('/ask', methods=['POST'])
def ask_question():
    user_question = request.json.get('question')
    
    # Load JSON file
   # with open("combined_data.json", "r", encoding="utf-8") as file:
       # pdf_content = json.load(file)
    
    # Flatten the nested dictionaries into a single string for context
    #context = []
    #for value in pdf_content.values():
      #  if isinstance(value, dict):
            # If the value is a dictionary, join all its values
           # context.append(' '.join(str(v) for v in value.values()))
      #  else:
            # If not a dictionary, just add the value directly
          #  context.append(str(value))
    
   # context = "\n".join(context)

     # Handle general greetings
    general_greetings = ["hi", "hello", "hey", "how are you", "good morning", "good afternoon", "good evening"]
    if any(greeting in user_question.lower() for greeting in general_greetings):
        return jsonify({"answer": "Hello! How can I assist you with the Adventist Mission today?"})
    
    # Handle general conversational words
    general_words = ["thank you", "that's great", "great", "goodbye", "thanks", "have a great day", "awesome"]
    if any(greeting in user_question.lower() for greeting in general_words):
        return jsonify({"answer": "I'm always here to help. God bless you as you do His work."})
    
    # Handle requests for contacts, phone numbers, or emails
   # contact_keywords = ["contact", "phone number", "email", "enquiries", "support", "assist me with contacts"]
   # if any(keyword in user_question.lower() for keyword in contact_keywords):
      #  return jsonify({
        #    "answer": "For further assistance, you can contact Zina Tsvetanova at email: ztsvetanova@ted.adventist.org."
       # })

    # Define a prompt to check if the question is relevant to the domain
    relevance_check_prompt = f"""
    The following is a question from a user. Please determine if it is relevant to the Adventist Mission or if it can be answered using common sense based on the context provided. 
    If it is relevant or can be reasonably inferred from the context, respond with 'relevant'. If it is completely unrelated, respond with 'not relevant'.

    Question: {user_question}
    Context: {context}
    """

    # Check if the question is relevant to the domain or can be answered with common sense
    relevance_check = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": relevance_check_prompt}
        ]
    )

    relevance_response = relevance_check.choices[0].message.content.strip().lower()
   
    if relevance_response == 'not relevant':
        return jsonify({"answer": "Sorry, I can only answer questions related to the Adventist Mission or those that can be inferred from its context."})

    # If the question is relevant or can be answered with common sense, generate a response
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a chatbot based on the following content: {context}. Use common sense when appropriate, but always try to stay within the scope of the Adventist Mission."},
            {"role": "user", "content": user_question}
        ]
    )
    
  
    
    return jsonify({"answer": completion.choices[0].message.content})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


# In[ ]:





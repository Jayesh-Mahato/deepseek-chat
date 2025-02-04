import sys
import pyttsx3
from ollama import chat
import random
import re

# Initialize TTS engine
engine = pyttsx3.init()

# Set TTS properties (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

def speak(text):
    """Function to speak the text using TTS."""
    engine.say(text)
    engine.runAndWait()

def get_answer_and_question(question):
    """Function to get an answer and follow-up question from the model."""
    # Stream the chat with a system prompt to generate both an answer and a follow-up question
    stream = chat(
        model='deepseek-r1:14b',
        messages=[
            {'role': 'user', 'content': question},
            {'role': 'system', 'content': 'Answer the question and then ask a relevant follow-up question based on your answer. Continue the conversation naturally.'}
        ],
        stream=True,
    )
    
    reasoning_content = ""
    content = ""
    next_question = ""
    in_thinking = False

    # Iterate through the chunks from the stream and assemble the response
    for chunk in stream:
        if chunk and 'message' in chunk and chunk['message'].content:
            # Get the content from the chunk
            chunk_content = chunk['message'].content
            
            # Print the content immediately, without newline
            sys.stdout.write(chunk_content)
            sys.stdout.flush()
            
            # Store in appropriate buffer
            if chunk_content.startswith('<think>'):
                in_thinking = True
            elif chunk_content.startswith('</think>'):
                in_thinking = False
            else:
                if 'in_thinking' in locals() and in_thinking:
                    reasoning_content += chunk_content
                else:
                    content += chunk_content
    
    print("\n\nReasoning:", reasoning_content)
    print("\nFinal Answer & Next Question:", content)

    # Check if there's an answer and a follow-up question
    if content.strip():
        # Assume that the answer and question are separated by a newline (or similar)
        # The first part of the content should be the answer, the second part the question.
        # If the model outputs the answer and question in one response, try splitting on "\n" or any delimiter.
        split_content = content.split("\n", 1)
        answer = split_content[0].strip() if len(split_content) > 0 else ""
        next_question = split_content[1].strip() if len(split_content) > 1 else ""
    else:
        answer = ""
        next_question = "Can you tell me more about that?"

    # If the answer is empty, fallback to a default response
    if not answer:
        answer = "Sorry, I didn't catch that. Could you clarify?"

    return answer, next_question

def infinite_conversation():
    """Function to keep the conversation going infinitely."""
    question = "Let's have a random conversation! What would you like to discuss?"  # Initial question

    while True:
        print(f"User: {question}")
        
        # Get the answer and follow-up question from the model
        answer, next_question = get_answer_and_question(question)
        
        # Output the answer
        print(f"Answer: {answer}")
        
        # Speak the answer
        speak(answer)
        
        # Output and speak the next follow-up question
        print(f"Next Question: {next_question}")
        speak(next_question)
        
        # The next question is now the follow-up question from the system
        question = next_question

# Start the conversation
infinite_conversation()

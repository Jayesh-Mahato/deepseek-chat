import sys
import pyttsx3
from ollama import chat

# Initialize TTS engine
engine = pyttsx3.init()

# Set TTS properties (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

def speak(text):
    """Function to speak the text using TTS."""
    engine.say(text)
    engine.runAndWait()

def get_answer(question):
    """Function to get an answer to a question from the model."""
    stream = chat(
        model='deepseek-r1:14b',
        messages=[{'role': 'user', 'content': question}],
        stream=True,
    )
    
    reasoning_content = ""
    content = ""
    in_thinking = False

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
    print("\nFinal Answer:", content)
    
    return content.strip()

def infinite_conversation():
    """Function to keep the conversation going infinitely."""
    question = "Let us start a random conversation"  # Initial question
    
    while True:
        print(f"User: {question}")
        
        # Get the answer from the model
        answer = get_answer(question)
        
        # Output the answer
        print(f"Answer: {answer}")
        
        # Speak the answer
        speak(answer)
        
        # Create the next question based on the answer
        question = f"Tell me more about {answer[:200]}..."  # Example: Use first 20 characters of the answer

# Start the conversation
infinite_conversation()


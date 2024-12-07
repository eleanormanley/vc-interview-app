#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install openai


# In[2]:


#pip install --upgrade pip


# In[1]:


import openai
import os

# Set up your OpenAI API key from an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Test the API connection
try:
    response = openai.Model.list()
    print("API connection successful. Available models:")
    for model in response['data']:
        print(model['id'])
except Exception as e:
    print(f"An error occurred: {e}")


# In[2]:


# Function to dynamically generate a new case study
def generate_case_study():
    """
    Generates a relevant case study focused on early-stage startups with fewer than 20 paying enterprise customers.
    """
    case_study_prompt = (
        "Generate a realistic and challenging case study for a venture capital interview. "
        "The startup should be an early-stage B2B SaaS company with the following constraints:\n"
        "- The company must have fewer than 20 paying enterprise customers.\n"
        "- Focus on early-stage challenges such as customer acquisition, proving product/market fit, and managing burn rate.\n"
        "- Include:\n"
        "   - Founders' background and roles.\n"
        "   - Market opportunity (TAM, SAM, growth potential).\n"
        "   - Product/market fit and traction.\n"
        "   - Early financial metrics (ARR, gross margin, burn rate, runway).\n"
        "   - Competitors and unique selling proposition (USP).\n"
        "   - Early-stage unit economics (CAC, LTV).\n"
        "   - Funding needs and planned use of funds.\n"
        "Make it specific, challenging, and concise."
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional case study generator."},
                {"role": "user", "content": case_study_prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        
        case_study = response['choices'][0]['message']['content']
        return case_study
    except Exception as e:
        return f"An error occurred while generating the case study: {e}"

# Function to initialize the conversation
def initialize_conversation():
    """
    Initializes the conversation history with a system message and a dynamically generated case study.
    """
    case_study = generate_case_study()
    return [
        {
            "role": "system",
            "content": (
                "You are a General Partner at a B2B SaaS-focused Venture Capital firm that invests in early-stage startups. "
                "Your role is to interview candidates for an associate position through a case study format. "
                "Focus on exploring all aspects of due diligence, including the team, market opportunity, product/market fit, "
                "customers and traction, financial metrics, competitors, unit economics, and burn rate. "
                "Ask detailed and relevant follow-up questions based on the candidate's response to test their understanding."
            )
        },
        {
            "role": "assistant",
            "content": f"Hello, and thank you for your interest in the associate position. "
                       f"Today, we're going to go through a challenging case study to evaluate your approach to due diligence. "
                       f"Here is your case study:\n\n{case_study}\n\n"
                       f"To begin, let's evaluate the founders and the team. What are the key factors you would consider when analyzing their strengths and weaknesses?"
        }
    ]

# Function to interact with the VC agent
def interact_with_vc_agent(candidate_input=None):
    """
    Handles the interaction between the AI agent (VC interviewer) and the user (candidate).
    Updates the conversation history dynamically with relevant follow-ups.
    """
    global conversation_history
    
    if candidate_input:
        conversation_history.append({"role": "user", "content": candidate_input})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation_history,
            temperature=0.7,
            max_tokens=500
        )
        
        ai_response = response['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response
    
    except Exception as e:
        return f"An error occurred: {e}"

# Function to save the conversation log
def save_conversation(conversation_history):
    """
    Saves the conversation history to a text file for review.
    """
    try:
        with open("vc_interview_log.txt", "a") as log_file:
            log_file.write("\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in conversation_history]))
            log_file.write("\n\n--- End of Session ---\n\n")
        print("Conversation has been saved to vc_interview_log.txt.")
    except Exception as e:
        print(f"An error occurred while saving the conversation: {e}")

# Function to generate final evaluation
def generate_final_evaluation(conversation_history):
    """
    Generates a final evaluation based on the conversation history.
    """
    try:
        evaluation_prompt = (
            "Based on the following conversation, provide a detailed evaluation of the candidate's performance. "
            "Highlight their strengths, areas of improvement, and give actionable feedback:\n\n"
            + "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in conversation_history])
        )
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert venture capital interviewer providing candidate evaluations."},
                {"role": "user", "content": evaluation_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"An error occurred while generating the evaluation: {e}"


# In[ ]:


if __name__ == "__main__":
    conversation_history = initialize_conversation()

    print("Welcome to the VC Interview Agent! Type 'quit' to exit.")
    while True:
        # If the first message is from the AI, display it
        if len(conversation_history) == 2:  # Case study is already provided
            print(f"VC: {conversation_history[1]['content']}")

        candidate_input = input("Candidate: ")
        if candidate_input.lower() == "quit":
            print("Exiting the session. Generating final evaluation...")
            evaluation = generate_final_evaluation(conversation_history)
            print("\nFinal Evaluation:\n")
            print(evaluation)
            save_conversation(conversation_history)
            break

        # Get AI response
        ai_response = interact_with_vc_agent(candidate_input)
        print(f"VC: {ai_response}")


# In[ ]:


import streamlit as st

# Streamlit App
def main():
    st.title("VC Interview Agent")
    st.write("Simulate a venture capital case study interview with dynamic scenarios.")

    if "conversation_history" not in st.session_state:
        case_study = generate_case_study()
        st.session_state.conversation_history = [
            {"role": "system", "content": "You are a VC interviewer."},
            {"role": "assistant", "content": case_study}
        ]

    conversation_history = st.session_state.conversation_history

    st.markdown(f"### Case Study:\n{conversation_history[1]['content']}")

    candidate_input = st.text_input("Your Response:", key="candidate_input")
    if st.button("Submit"):
        if candidate_input.lower() == "quit":
            st.write("Ending the session...")
            evaluation = generate_final_evaluation(conversation_history)
            st.markdown("### Final Evaluation:")
            st.write(evaluation)
            st.stop()
        else:
            ai_response = interact_with_vc_agent(conversation_history, candidate_input)
            st.markdown(f"### VC Response:\n{ai_response}")

if __name__ == "__main__":
    main()


# In[ ]:





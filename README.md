# vc-interview-app

## Overview
This repository provides a Python-based tool to simulate a Venture Capital (VC) interview for associate candidates. The simulator dynamically generates realistic case studies focused on early-stage B2B SaaS startups and evaluates candidates based on their ability to conduct due diligence.

## Features
- **Dynamic Case Study Generation**: Uses OpenAI's GPT-4 model to generate challenging and realistic case studies.  
- **Interactive Simulation**: Engage in a mock VC interview as the candidate.  
- **Performance Evaluation**: Automatically generates a detailed evaluation based on the interaction.  
- **Conversation Log**: Saves the entire session for later review.  
- **Streamlit Web App**: A user-friendly interface to simulate the interview process. (coded but not launched).

## Installation
**Clone the Repository**  

**Install Dependencies**
bash
pip install -r requirements.txt

**Set Up OpenAI API Key**

## Usage
Run the simulation in your terminal:
bash
Copy code
python main.py

Streamlit Web App (not launched yet)
Launch a Streamlit app:
bash
Copy code
streamlit run main.py

## File Structure
- **main.py**: Entry point for CLI and Streamlit app.
- **vc_interview.py**: Core functions for interaction and evaluation.
- **requirements**.txt: List of Python dependencies.
- **README.md**: Project documentation.

## Key Features
**1. Case Study Generation**
Generates a case study focused on:
Team: Founders' backgrounds and roles.
Market Opportunity: TAM, SAM, and growth potential.
Traction: Product/market fit and early metrics.
Financial Metrics: ARR, burn rate, runway.
Competitors: Analysis of competition and USP.
Unit Economics: CAC, LTV, and other early-stage metrics.
Funding: Investment needs and planned use of funds.

**2. Interactive Q&A**
Simulates an interview with:
Follow-up questions based on candidate responses.
Challenges designed to test strategic thinking and analysis.

**3. Performance Evaluation**
Automatically generates a detailed report highlighting:
Candidate strengths.
Areas for improvement.
Actionable feedback.

**4. Conversation Log**
Saves the session in a structured format for review.

## License
This project is licensed under the MIT License. See LICENSE for details.

## Acknowledgements
Powered by OpenAI's GPT-4.
Inspired by real-world venture capital interview processes.




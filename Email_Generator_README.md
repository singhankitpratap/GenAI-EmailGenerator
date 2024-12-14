
# Email Generator

## Overview
The **Email Generator** is a Streamlit-based **GenAI application leveraging LLM (Large Language Models)** to create personalized emails from job postings. It extracts job details from a URL, matches required skills with portfolio data, and generates professional emails showcasing your capabilities.

## Features
- Extracts job postings from a URL.
- Matches job skills with portfolio examples.
- Generates tailored emails.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/email-generator.git
   cd email-generator
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the main program:
   ```bash
   streamlit run main.py
   ```

## Usage
1. Provide a URL with job postings.
2. Click **Submit** to generate emails.
3. Review the email displayed in the application.

## Dependencies
- `streamlit`
- `langchain`
- `chromadb`
- `pandas`

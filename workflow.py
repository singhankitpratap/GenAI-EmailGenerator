import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Workflow:
    def __init__(self):
        self.language_model = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

    def parse_job_postings(self, raw_text):
        job_prompt_template = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {website_content}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        extraction_chain = job_prompt_template | self.language_model
        response = extraction_chain.invoke(input={"website_content": raw_text})
        try:
            json_output_parser = JsonOutputParser()
            parsed_response = json_output_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException("Context too large. Unable to parse job postings.")
        return parsed_response if isinstance(parsed_response, list) else [parsed_response]

    def compose_email(self, job_details, portfolio_links):
        email_prompt_template = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_info}

            ### INSTRUCTION:
            You are Alex, a Business Development Executive at Firm X, a leading AI and software consulting firm that transforms businesses through smart automation and innovative solutions. 
            With a proven track record, Firm X has helped organizations achieve growth by optimizing operations, reducing costs, and driving efficiency with personalized approaches tailored to their specific goals.
            Your role is to compose an email to a potential client, highlighting Firm X's ability to address their requirements effectively. Leverage the most relevant examples from the provided portfolio links ({portfolio_list}) 
            to demonstrate the company's expertise and success stories. Maintain a professional tone, focusing on Firm X’s value proposition, and avoid unnecessary introductions or unrelated details.
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        email_chain = email_prompt_template | self.language_model
        response = email_chain.invoke({"job_info": str(job_details), "portfolio_list": portfolio_links})
        return response.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))

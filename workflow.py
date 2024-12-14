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
            You are Alex, a business development executive at Firm X. Firm X is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Firm X 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase Firm X's portfolio: {portfolio_list}
            Remember you are Alex, BDE at Firm X. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        email_chain = email_prompt_template | self.language_model
        response = email_chain.invoke({"job_info": str(job_details), "portfolio_list": portfolio_links})
        return response.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))

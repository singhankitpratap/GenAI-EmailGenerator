import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from workflow import Workflow
from portfolio_manager import PortfolioManager
from utils import clean_text_content


def generate_email_app(language_model, portfolio_manager, text_cleaner):
    st.title("Email Generator")
    url_input = st.text_input(
        "Enter a URL:",
        value="https://www.google.com/about/careers/applications/jobs/results/114056787417539270-silicon-aiml-architect-google-cloud"
    )
    submit_button = st.button("Submit")

    if submit_button:
        try:
            web_loader = WebBaseLoader([url_input])
            raw_content = web_loader.load().pop().page_content
            cleaned_content = text_cleaner(raw_content)
            portfolio_manager.initialize_portfolio()
            job_listings = language_model.parse_job_postings(cleaned_content)
            for job in job_listings:
                skillset = job.get('skills', [])
                portfolio_links = portfolio_manager.fetch_relevant_links(skillset)
                generated_email = language_model.compose_email(job, portfolio_links)
                st.code(generated_email, language='markdown')
        except Exception as error:
            st.error(f"An Error Occurred: {error}")


if __name__ == "__main__":
    workflow_model = Workflow()
    portfolio_manager = PortfolioManager()
    st.set_page_config(layout="wide", page_title="Email Generator")
    generate_email_app(workflow_model, portfolio_manager, clean_text_content)

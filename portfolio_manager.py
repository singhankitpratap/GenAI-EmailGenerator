import pandas as pd
import chromadb
import uuid

class PortfolioManager:
    def __init__(self, csv_file_path="resource/portfolio.csv"):
        self.csv_file_path = csv_file_path
        self.portfolio_data = pd.read_csv(csv_file_path)
        self.vector_client = chromadb.PersistentClient('vectorstore')
        self.skill_collection = self.vector_client.get_or_create_collection(name="portfolio_skills")

    def initialize_portfolio(self):
        if not self.skill_collection.count():
            for _, record in self.portfolio_data.iterrows():
                self.skill_collection.add(
                    documents=record["Techstack"],
                    metadatas={"links": record["Links"]},
                    ids=[str(uuid.uuid4())]
                )

    def fetch_relevant_links(self, required_skills):
        query_results = self.skill_collection.query(
            query_texts=required_skills, 
            n_results=2
        )
        return query_results.get('metadatas', [])

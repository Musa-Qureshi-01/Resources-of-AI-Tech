from utils.uploader import Loader, Chunker
from utils.helpers import Cleaner
from utils.summarizer import Summary

def run_summarization_pipeline(file_path: str):
    # Load document
    print(f"📂 Loading file: {file_path}")
    docs = Loader(file_path).upload()

    #  Clean document
    print("🧹 Cleaning text...")
    cleaned_text = Cleaner(docs).combiner().clean_legal_text().docs

    # Chunk for summarization
    print("✂️ Splitting into chunks for summarization...")
    chunks = Chunker(cleaned_text).for_summary()

    #  Run summarization
    print("🤖 Running summarization...")
    summary = Summary(chunks).summarize(chain_type="map_reduce")

    print("\n✅ Final Summary:\n")
    print(summary)

if __name__ == "__main__":
    # Example usage
    run_summarization_pipeline(r"C:\Users\musaq\OneDrive\Desktop\AI\Project\legal-advisor\legal_advisor\Documents\LEGAL OPINION ON PROPERTY MATTERS AND.pdf")  

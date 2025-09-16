from utils.uploader import Loader, Chunker
from utils.helpers import Cleaner

def run_embedidng_pipeline(file_path : str):

    print(f"📂 Loading file: {file_path}")
    docs = Loader(file_path).upload()

    print("🧹 Cleaning text...")
    cleaned_text = Cleaner(docs).combiner().clean_legal_text().docs


    print("✂️ Splitting into chunks for summarization...")
    chunks = Chunker(cleaned_text).for_embedding()

    
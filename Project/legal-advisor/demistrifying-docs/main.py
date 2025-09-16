# filename: legal_ai_langchain.py
# Python 3.10+

import os
import re
import argparse
from typing import List, Dict, Optional

from dotenv import load_dotenv
from pypdf import PdfReader
from pydantic import SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA

# -----------------------------
# Config
# -----------------------------
LLM_MODEL = "gemini-1.5-flash"
EMBED_MODEL = "models/embedding-001"

SUMMARY_PROMPT = """You are a legal explainer. Summarize the following text in clear, simple language:
- Highlight rights, obligations, penalties, renewals, dispute resolution.
- Use bullets and plain English.
TEXT:
{chunk}"""

REDUCE_PROMPT = """Combine the partial summaries into one short plain-language summary:
- Remove repetition
- Highlight critical risks (fees, penalties, termination, jurisdiction)
- End with a short checklist
PARTIAL SUMMARIES:
{partials}"""

DEFAULT_GLOSSARY = {
    "indemnity": "a promise to cover losses or damages someone else suffers",
    "waiver": "giving up a right intentionally",
    "liability": "legal responsibility for something",
    "jurisdiction": "the court or authority that can resolve disputes",
    "arbitration": "a private process to resolve disputes without court",
    "force majeure": "unforeseen events (e.g., natural disasters) that excuse obligations",
    "termination": "ending the contract",
    "auto-renewal": "the contract renews automatically unless you cancel",
    "security deposit": "money held as a guarantee against damage or unpaid dues",
    "late fee": "extra charge if you pay after the due date",
    "notice period": "how long in advance you must tell the other party before ending"
}

RISK_TERMS = [
    "penalty", "forfeit", "termination", "irrevocable", "non-refundable",
    "waiver", "indemnity", "liability", "arbitration", "jurisdiction",
    "auto-renewal", "late fee", "lock-in period", "default", "guarantee"
]

# -----------------------------
# Helpers
# -----------------------------
def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join([p.extract_text() or "" for p in reader.pages])

def read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def load_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return read_pdf(path)
    elif ext == ".txt":
        return read_txt(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def basic_clean(text: str) -> str:
    text = re.sub(r"[^\S\r\n]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()

def apply_glossary(text: str, glossary: Dict[str, str]) -> str:
    for term, meaning in glossary.items():
        pattern = r"\b" + re.escape(term) + r"\b"
        text = re.sub(pattern, f"{term} ({meaning})", text, flags=re.IGNORECASE)
    return text

def find_risks(text: str) -> List[str]:
    found = [t for t in RISK_TERMS if t in text.lower()]
    return sorted(set(found))

# -----------------------------
# Core Pipeline (LangChain)
# -----------------------------
def run_pipeline(filepath: str, question: Optional[str] = None) -> Dict:
    # 1. Load
    raw = load_file(filepath)
    cleaned = basic_clean(raw)

    # 2. Glossary simplify
    simplified = apply_glossary(cleaned, DEFAULT_GLOSSARY)

    # 3. Risks
    risks = find_risks(simplified)

    # 4. Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    docs = splitter.split_documents([Document(page_content=simplified)])

    # 5. Summarization (map-reduce manually)
    google_api_key = SecretStr(os.getenv("GOOGLE_API_KEY"))
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=google_api_key)

    partials = []
    for d in docs:
        resp = llm.invoke(SUMMARY_PROMPT.format(chunk=d.page_content))
        partials.append(resp.content if hasattr(resp, "content") else str(resp))

    resp_sum = llm.invoke(REDUCE_PROMPT.format(partials="\n\n".join(partials)))
    summary = resp_sum.content if hasattr(resp_sum, "content") else str(resp_sum)

    # 6. Embedding + RAG Q&A
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBED_MODEL, google_api_key=os.getenv("GOOGLE_API_KEY"))
    db = FAISS.from_documents(docs, embeddings)

    qa_answer = None
    if question:
        retriever = db.as_retriever(search_kwargs={"k": 5})
        qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")
        qa_answer = qa.run(question)

    return {
        "cleaned_preview": simplified[:800] + ("..." if len(simplified) > 800 else ""),
        "risks": risks,
        "summary": summary,
        "qa": qa_answer
    }

# -----------------------------
# CLI
# -----------------------------
def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Legal Document Demystifier (LangChain + Gemini)")
    parser.add_argument("--file", help="Path to PDF or TXT")
    parser.add_argument("--question", help="Optional question to ask")
    args = parser.parse_args()

    # Default to your PDF if none provided
    if not args.file:
        default_path = "LEGAL OPINION ON PROPERTY MATTERS AND.pdf"
        if os.path.exists(default_path):
            print(f"⚠️ No file provided. Using default: {default_path}")
            args.file = default_path
        else:
            print("❌ No file provided and default PDF not found. Exiting.")
            return

    out = run_pipeline(args.file, question=args.question)

    print("\n=== CLEANED PREVIEW ===\n")
    print(out["cleaned_preview"])

    print("\n=== RISKS DETECTED ===\n")
    print(", ".join(out["risks"]) or "No obvious risk terms found.")

    print("\n=== SUMMARY ===\n")
    print(out["summary"])

    if out["qa"]:
        print("\n=== Q&A ===\n")
        print(out["qa"])


if __name__ == "__main__":
    main()

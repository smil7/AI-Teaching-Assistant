import os
import csv
from datetime import datetime
from constants import EMBEDDING_MODEL_NAME
import sys

# Force import sentence_transformers directly to debug
try:
    import sentence_transformers
    print(f"Successfully imported sentence_transformers version: {sentence_transformers.__version__}")
except ImportError as e:
    print(f"Failed to import sentence_transformers: {e}")

# Import the embeddings after ensuring sentence_transformers works
from langchain_community.embeddings import HuggingFaceEmbeddings


def log_to_csv(question, answer):

    log_dir, log_file = "local_chat_history", "qa_log.csv"
    # Ensure log directory exists, create if not
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Construct the full file path
    log_path = os.path.join(log_dir, log_file)

    # Check if file exists, if not create and write headers
    if not os.path.isfile(log_path):
        with open(log_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "question", "answer"])

    # Append the log entry
    with open(log_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, question, answer])


def get_embeddings(device_type="cpu"):
    print(f"Using {EMBEDDING_MODEL_NAME} as embedding model")
    # Direct use of HuggingFaceEmbeddings with explicit model_name
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": device_type},
        encode_kwargs={"normalize_embeddings": True}
    )
    print(f"Successfully created embeddings object: {type(embeddings)}")
    return embeddings


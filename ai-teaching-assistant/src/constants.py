import os

# from dotenv import load_dotenv
from chromadb.config import Settings

# https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/excel.html?highlight=xlsx#microsoft-excel
from langchain_community.document_loaders import CSVLoader, PDFMinerLoader, TextLoader, UnstructuredExcelLoader, Docx2txtLoader
from langchain_community.document_loaders import UnstructuredFileLoader, UnstructuredMarkdownLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_community.document_loaders import PyPDFLoader

# load_dotenv()
ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Define the folder for storing database
SOURCE_DIRECTORY = f"{ROOT_DIRECTORY}/SOURCE_DOCUMENTS"

# Ensure SOURCE_DIRECTORY exists
if not os.path.exists(SOURCE_DIRECTORY):
    os.makedirs(SOURCE_DIRECTORY)

PERSIST_DIRECTORY = f"{ROOT_DIRECTORY}/DB"

MODELS_PATH = "./models"

# Can be changed to a specific number
INGEST_THREADS = os.cpu_count() or 8

# Define the Chroma settings
CHROMA_SETTINGS = Settings(
    anonymized_telemetry=False,
    is_persistent=True,
)

# Context Window and Max New Tokens
CONTEXT_WINDOW_SIZE = 4096
MAX_NEW_TOKENS = 128  # int(CONTEXT_WINDOW_SIZE/4)

#### If you get a "not enough space in the buffer" error, you should reduce the values below, start with half of the original values and keep halving the value until the error stops appearing

N_GPU_LAYERS = 100  # Llama-2-70B has 83 layers
N_BATCH = 512

### From experimenting with the Llama-2-7B-Chat-GGML model on 8GB VRAM, these values work:
# N_GPU_LAYERS = 20
# N_BATCH = 512


# https://python.langchain.com/en/latest/_modules/langchain/document_loaders/excel.html#UnstructuredExcelLoader
DOCUMENT_MAP = {
    ".csv": CSVLoader,
    ".doc": Docx2txtLoader,
    ".docx": Docx2txtLoader,
    ".html": UnstructuredHTMLLoader,
    ".md": UnstructuredMarkdownLoader,
    ".pdf": PyPDFLoader,  # Changed from UnstructuredFileLoader to PyPDFLoader
    ".txt": TextLoader,
    ".xlsx": UnstructuredExcelLoader,
}

# Default Instructor Model
#EMBEDDING_MODEL_NAME = "hkunlp/instructor-large"  # Uses 1.5 GB of VRAM (High Accuracy with lower VRAM usage)

####
#### OTHER EMBEDDING MODEL OPTIONS
####

#EMBEDDING_MODEL_NAME = "hkunlp/instructor-xl" # Uses 5 GB of VRAM (Most Accurate of all models)
# EMBEDDING_MODEL_NAME = "intfloat/e5-large-v2" # Uses 1.5 GB of VRAM (A little less accurate than instructor-large)
# EMBEDDING_MODEL_NAME = "intfloat/e5-base-v2" # Uses 0.5 GB of VRAM (A good model for lower VRAM GPUs)
#EMBEDDING_MODEL_NAME = "distilbert-base-uncased" # Simpler model that works on CPU
# EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2" # Uses 0.2 GB of VRAM (Less accurate but fastest - only requires 150mb of vram)
EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2" # Uses 0.4 GB of VRAM (Good balance of speed and accuracy)

#### SELECT AN OPEN SOURCE LLM (LARGE LANGUAGE MODEL)
# Select the Model ID and model_basename
# load the LLM for generating Natural Language responses

# MODEL_ID = "TheBloke/Llama-2-7B-Chat-GGML"
# MODEL_BASENAME = "llama-2-7b-chat.ggmlv3.q4_0.bin"

####
#### (FOR GGUF MODELS)
####

#MODEL_ID = "TheBloke/Llama-2-13b-Chat-GGUF"
#MODEL_BASENAME = "llama-2-13b-chat.Q4_K_M.gguf"

MODEL_ID = "TheBloke/Llama-2-7b-Chat-GGUF"
MODEL_BASENAME = "llama-2-7b-chat.Q4_K_M.gguf"

# MODEL_ID = "QuantFactory/Meta-Llama-3-8B-Instruct-GGUF"
# MODEL_BASENAME = "Meta-Llama-3-8B-Instruct.Q4_K_M.gguf"

####
#### (FOR HF MODELS)
####

# MODEL_ID = "NousResearch/Llama-2-7b-chat-hf"
# MODEL_BASENAME = None
# MODEL_ID = "TheBloke/vicuna-7B-1.1-HF"
# MODEL_BASENAME = None
# MODEL_ID = "TheBloke/Wizard-Vicuna-7B-Uncensored-HF"


####
#### (FOR GGML) (Quantized cpu+gpu+mps) models - check if they support llama.cpp
####

# MODEL_ID = "TheBloke/wizard-vicuna-13B-GGML"
# MODEL_BASENAME = "wizard-vicuna-13B.ggmlv3.q4_0.bin"
# MODEL_BASENAME = "wizard-vicuna-13B.ggmlv3.q6_K.bin"
# MODEL_BASENAME = "wizard-vicuna-13B.ggmlv3.q2_K.bin"
# MODEL_ID = "TheBloke/orca_mini_3B-GGML"
# MODEL_BASENAME = "orca-mini-3b.ggmlv3.q4_0.bin"

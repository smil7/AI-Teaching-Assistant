import logging
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

import torch
from langchain_community.docstore.document import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import Language, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from utils import get_embeddings

from constants import (
    CHROMA_SETTINGS,
    DOCUMENT_MAP,
    EMBEDDING_MODEL_NAME,
    INGEST_THREADS,
    PERSIST_DIRECTORY,
    SOURCE_DIRECTORY,
)

import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

class Ingestion:
    def __init__(self, course_name, instructions, course_materials, device_type="cpu"):
        print('welcome to ingestion class')
        self.course_name = course_name
        self.instructions = instructions
        self.course_materials = course_materials  # Now this is a list of file paths
        self.device_type = device_type
       
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.python_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON, chunk_size=880, chunk_overlap=200
        )
        self.embeddings = get_embeddings(device_type)

    def file_log(self, logentry):
        file1 = open("file_ingest.log", "a")
        file1.write(logentry + "\n")
        file1.close()
        print(logentry + "\n")

    def load_single_document(self, file_path: str) -> Document:
        # Loads a single document from a file path
        try:
            # Normalize path separators to be consistent
            file_path = os.path.normpath(file_path)
            
            # Verify file exists
            if not os.path.exists(file_path):
                self.file_log(f"{file_path} does not exist.")
                return None
            
            file_extension = os.path.splitext(file_path)[1].lower()  # Normalize extension to lowercase
            
            # Special handling for PDFs
            if file_extension == '.pdf':
                try:
                    loader = PyPDFLoader(file_path)
                    self.file_log(file_path + " loaded with PyPDFLoader.")
                    return loader.load()[0]  # Get the first document
                except Exception as pdf_ex:
                    self.file_log(f"PyPDFLoader failed: {pdf_ex}, trying fallback...")
                    # Fallback to text extraction
                    try:
                        import fitz  # PyMuPDF
                        doc = fitz.open(file_path)
                        text = ""
                        for page in doc:
                            text += page.get_text()
                        doc.close()
                        
                        # Create a Document object
                        return Document(
                            page_content=text,
                            metadata={"source": file_path}
                        )
                    except Exception as mupdf_ex:
                        self.file_log(f"MuPDF extraction failed: {mupdf_ex}")
                        raise
            
            # For other file types
            loader_class = DOCUMENT_MAP.get(file_extension)
            if loader_class:
                self.file_log(file_path + " loaded.")
                loader = loader_class(file_path)
            else:
                self.file_log(file_path + " document type is undefined.")
                raise ValueError(f"Document type {file_extension} is not supported")
            
            documents = loader.load()
            if documents:
                return documents[0]
            else:
                self.file_log(f"No content extracted from {file_path}")
                return None
        except Exception as ex:
            self.file_log("%s loading error: \n%s" % (file_path, ex))
            return None

    def load_document_batch(self, filepaths):
        logging.info("Loading document batch")
        # create a thread pool
        with ThreadPoolExecutor(len(filepaths)) as exe:
            # load files
            futures = [exe.submit(self.load_single_document, name) for name in filepaths]
            # collect data
            if futures is None:
                self.file_log(name + " failed to submit")
                return None
            else:
                data_list = [future.result() for future in futures]
                # return data and file paths
                return (data_list, filepaths)

    def load_documents(self, source_dir: str) -> list[Document]:
        # Loads all documents from the source documents directory, including nested folders
        paths = []
        for root, _, files in os.walk(source_dir):
            for file_name in files:
                print("Importing: " + file_name)
                file_extension = os.path.splitext(file_name)[1]
                source_file_path = os.path.join(root, file_name)
                if file_extension in DOCUMENT_MAP.keys():
                    paths.append(source_file_path)

        # Have at least one worker and at most INGEST_THREADS workers
        n_workers = min(INGEST_THREADS, max(len(paths), 1))
        chunksize = round(len(paths) / n_workers)
        docs = []
        with ProcessPoolExecutor(n_workers) as executor:
            futures = []
            # split the load operations into chunks
            for i in range(0, len(paths), chunksize):
                # select a chunk of filenames
                filepaths = paths[i : (i + chunksize)]
                # submit the task
                try:
                    future = executor.submit(self.load_document_batch, filepaths)
                except Exception as ex:
                    self.file_log("executor task failed: %s" % (ex))
                    future = None
                if future is not None:
                    futures.append(future)
            # process all results
            for future in as_completed(futures):
                # open the file and load the data
                try:
                    contents, _ = future.result()
                    docs.extend(contents)
                except Exception as ex:
                    self.file_log("Exception: %s" % (ex))

        return docs

    def split_documents(self, documents: list[Document]) -> tuple[list[Document], list[Document]]:
        # Splits documents for correct Text Splitter
        text_docs, python_docs = [], []
        for doc in documents:
            if doc is not None:
                file_extension = os.path.splitext(doc.metadata["source"])[1]
                if file_extension == ".py":
                    python_docs.append(doc)
                else:
                    text_docs.append(doc)
        return text_docs, python_docs
    
    def ingest(self):
        # Load documents directly from course_materials 
        logging.info(f"Loading documents from provided course materials")
        documents = []
        
        # Process uploaded files directly if available
        if self.course_materials and len(self.course_materials) > 0:
            logging.info(f"Processing {len(self.course_materials)} uploaded files")
            # Create a batch of paths for the uploaded files
            paths = [os.path.normpath(path) for path in self.course_materials if os.path.exists(os.path.normpath(path))]
            
            if paths:
                # Have at least one worker and at most INGEST_THREADS workers
                n_workers = min(INGEST_THREADS, max(len(paths), 1))
                chunksize = max(1, round(len(paths) / n_workers))
                
                with ProcessPoolExecutor(n_workers) as executor:
                    futures = []
                    # split the load operations into chunks
                    for i in range(0, len(paths), chunksize):
                        # select a chunk of filenames
                        filepaths = paths[i : (i + chunksize)]
                        # submit the task
                        try:
                            future = executor.submit(self.load_document_batch, filepaths)
                        except Exception as ex:
                            self.file_log(f"Executor task failed: {ex}")
                            future = None
                        if future is not None:
                            futures.append(future)
                    
                    # process all results
                    for future in as_completed(futures):
                        # open the file and load the data
                        try:
                            contents, _ = future.result()
                            if contents:
                                documents.extend([doc for doc in contents if doc is not None])
                        except Exception as ex:
                            self.file_log(f"Exception: {ex}")
        
        # Check if documents list is empty
        document_count = len([doc for doc in documents if doc is not None])
        print(f"Successfully loaded {document_count} documents")
        
        if document_count == 0:
            logging.warning("No documents found to ingest. Check your uploaded files.")
            return 0
        
        # Process the documents
        text_documents, python_documents = self.split_documents(documents)
        texts = self.text_splitter.split_documents(text_documents) if text_documents else []
        print(texts)
        print(python_documents)

        if python_documents:
            texts.extend(self.python_splitter.split_documents(python_documents))
        
        text_chunk_count = len(texts)
        print(f"Created {text_chunk_count} text chunks for embedding")
        
        if not texts:
            logging.warning("No text chunks created from documents. Check your documents content.")
            return 0
        
        try:
            # Clear the DB directory first to avoid conflicts
            import shutil
            if os.path.exists(PERSIST_DIRECTORY):
                shutil.rmtree(PERSIST_DIRECTORY)
                os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
                print(f"Cleared existing database at {PERSIST_DIRECTORY}")
            
            print(f"Using embedding model: {EMBEDDING_MODEL_NAME}")
            db = Chroma.from_documents(
                texts,
                self.embeddings,
                persist_directory=PERSIST_DIRECTORY,
                client_settings=CHROMA_SETTINGS,
            )
            db.persist()
            db = None
            print(f"Successfully stored {text_chunk_count} chunks in the vector database")
        except Exception as e:
            logging.error(f"Error creating vector database: {e}")
            raise
        
        return document_count


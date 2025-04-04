from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from ingest_class import Ingestion
from qa_retrieval_class import QARetrieval
import traceback

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use absolute path for SOURCE_DOCUMENTS to prevent path issues
ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(ROOT_DIRECTORY, 'SOURCE_DOCUMENTS')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/api/ingest', methods=['POST'])
def ingest_documents():
    try:

        course_name = request.form.get('courseName')
        instructions = request.form.get('instructions')
        files = request.files.getlist('courseMaterials')
        
        logger.debug(f"Received request with course_name: {course_name}")
        logger.debug(f"Number of files: {len(files)}")
        
        # Save uploaded files with normalized paths
        saved_files = []
        for file in files:
            if file.filename:
                # Normalize the filename to remove problematic characters
                safe_filename = os.path.basename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
                
                # Make sure the directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                # Save the file
                file.save(file_path)
                saved_files.append(file_path)
                logger.debug(f"Saved file: {file_path}")
        
        # Initialize ingestion with file paths instead of file objects
        ingestion = Ingestion(
            course_name=course_name,
            instructions=instructions,
            course_materials=saved_files,
            device_type="cpu"
        )
        
        # Process documents
        num_documents = ingestion.ingest()

        global qa_retrieval
        # Initialize QA retrieval
        qa_retrieval = QARetrieval(
            device_type="cpu",
            course_name=course_name,
            instructions=instructions,
        )
        
        return jsonify({
            "message": "the files and names are ingested",
            "num_documents": num_documents
        })
        
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        query = data.get('query', '')
        print(f"Received query: {query}")

        if not query:
            return jsonify({'answer': 'No query provided'}), 400

        # Use the QA retrieval class to get an answer
        answer = qa_retrieval.get_answer(query)
        print(f"Query: {query}")
        print(f"Answer: {answer}")
        print(f"Type of answer: {type(answer)}")

        if isinstance(answer, dict) and 'result' in answer:
            answer = answer['result']
        print(f"Answer: {answer}")

        return jsonify({'answer': answer})

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

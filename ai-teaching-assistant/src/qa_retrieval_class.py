import os
import logging
import torch
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline, LlamaCpp
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain_community.vectorstores import Chroma

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

from prompt_template_utils import get_prompt_template
from utils import get_embeddings
from transformers import GenerationConfig, pipeline
from load_models import (
    load_quantized_model_awq, load_quantized_model_gguf_ggml,
    load_full_model
)
from constants import (
    EMBEDDING_MODEL_NAME, PERSIST_DIRECTORY, MODEL_ID, MODEL_BASENAME,
    MAX_NEW_TOKENS, MODELS_PATH, CHROMA_SETTINGS
)


callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

class QARetrieval:
    def __init__(self, device_type="cpu", course_name=None, instructions=None):
        # self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME, model_kwargs={"device": device_type})
        self.embeddings = get_embeddings(device_type)
        self.course_name = course_name
        self.instructions = instructions


    def load_model(self, device_type, model_id, model_basename=None, LOGGING=logging):
        
        logging.info(f"Loading Model: {model_id}, on: {device_type}")
        logging.info("This action can take a few minutes!")
        
        if model_basename is not None:
            if ".gguf" in model_basename.lower():
                llm = load_quantized_model_gguf_ggml(model_id, model_basename, device_type, LOGGING)
                return llm
            elif ".ggml" in model_basename.lower():
                model, tokenizer = load_quantized_model_gguf_ggml(model_id, model_basename, device_type, LOGGING)
            elif ".awq" in model_basename.lower():
                model, tokenizer = load_quantized_model_awq(model_id, LOGGING)
            # else:
            #     model, tokenizer = load_quantized_model_qptq(model_id, model_basename, device_type, LOGGING)
        else:
            model, tokenizer = load_full_model(model_id, model_basename, device_type, LOGGING)

        # Load configuration from the model to avoid warnings
        generation_config = GenerationConfig.from_pretrained(model_id)
        
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=MAX_NEW_TOKENS,
            temperature=0.2,
            # top_p=0.95,
            repetition_penalty=1.15,
            generation_config=generation_config,
        )

        local_llm = HuggingFacePipeline(pipeline=pipe)
        logging.info("Local LLM Loaded")

        return local_llm


    def retrieval_qa_pipline(self,device_type, use_history, promptTemplate_type="llama"):

        logging.info(f"Loaded embeddings from {EMBEDDING_MODEL_NAME}")

        # load the vectorstore
        db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=self.embeddings, client_settings=CHROMA_SETTINGS)
        retriever = db.as_retriever()

        # get the prompt template and memory if set by the user.
        prompt, memory = get_prompt_template(promptTemplate_type=promptTemplate_type,
                                            history=use_history, 
                                            course_name=self.course_name, 
                                            instructions=self.instructions)

        # load the llm pipeline
        llm = self.load_model(device_type, model_id=MODEL_ID, model_basename=MODEL_BASENAME, LOGGING=logging)

        if use_history:
            qa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",  # try other chains types as well. refine, map_reduce, map_rerank
                retriever=retriever,
                return_source_documents=True,  # verbose=True,
                callbacks=callback_manager,
                chain_type_kwargs={"prompt": prompt, "memory": memory},
            )
        else:
            qa = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",  # try other chains types as well. refine, map_reduce, map_rerank
                retriever=retriever,
                return_source_documents=True,  # verbose=True,
                callbacks=callback_manager,
                chain_type_kwargs={
                    "prompt": prompt,
                },
            )

        return qa

    def get_answer(self, query):

        logging.info(f"Received query: {query}")

        # check if models directory do not exist, create a new one and store models here.
        if not os.path.exists(MODELS_PATH):
            os.mkdir(MODELS_PATH)

        # Assuming default values for device_type, use_history, and model_type
        device_type = "cpu"
        use_history = False
        model_type = "default"

        # Ensure course_name and instructions are not None
        # course_name = self.course_name
        # instructions = self.instructions

        qa = self.retrieval_qa_pipline(device_type, use_history, promptTemplate_type=model_type)
        answer = qa({
            "query": query
        })
        return answer
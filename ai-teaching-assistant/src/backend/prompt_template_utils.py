"""
This file implements prompt template for llama based models. 
Modify the prompt template based on the model you select. 
This seems to have significant impact on the output of the LLM.
"""

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

# this is specific to Llama-2.

system_prompt = """You are a helpful teaching assistant for the course {course_name}, your main task is to help the students navigate the 
 course content and answer any type of question that comes from them basically mirroring the behavior of a teaching assistant, you will use the
 provided context by the user to answer user questions. Read the given context before answering questions and think step by step. 
 If you can not answer a user question based on the provided context, inform the user. Do not use any other information for answering user. 
 Provide a detailed answer to the question. Notes to consider: 
 1. The user should provide a course name to you, the course name is {course_name}. Please change the 'course_name' to the actual course name.
 2. Sometimes the user will upload additional Instructions to specify what exactly they want you to assisit in. If they added instructions 
 just put the text under 'Instructions: {instructions}'. If it's empty then ignore the instructions part. """


def get_prompt_template(system_prompt=system_prompt, promptTemplate_type=None, history=False, course_name=None, instructions=None):
    print(f"Course name: {course_name}")
    print(f"Instructions: {instructions}")
    system_prompt = system_prompt.format(course_name=course_name, instructions=instructions)
    if promptTemplate_type == "llama":
        B_INST, E_INST = "[INST]", "[/INST]"
        B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
        SYSTEM_PROMPT = B_SYS + system_prompt + E_SYS
        if history:
            instruction = """
            Context: {history} \n {context}
            User: {question}"""

            prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            instruction = """
            Context: {context}
            User: {question}"""

            prompt_template = B_INST + SYSTEM_PROMPT + instruction + E_INST
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)

    elif promptTemplate_type == "llama3":

        B_INST, E_INST = "<|start_header_id|>user<|end_header_id|>", "<|eot_id|>"
        B_SYS, E_SYS = "<|begin_of_text|><|start_header_id|>system<|end_header_id|> ", "<|eot_id|>"
        ASSISTANT_INST = "<|start_header_id|>assistant<|end_header_id|>"
        SYSTEM_PROMPT = B_SYS + system_prompt + E_SYS
        if history:
            instruction = """
            Context: {history} \n {context}
            User: {question}"""

            prompt_template = SYSTEM_PROMPT + B_INST + instruction + ASSISTANT_INST
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            instruction = """
            Context: {context}
            User: {question}"""

            prompt_template = SYSTEM_PROMPT + B_INST + instruction + ASSISTANT_INST
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)

    elif promptTemplate_type == "mistral":
        B_INST, E_INST = "<s>[INST] ", " [/INST]"
        if history:
            prompt_template = (
                B_INST
                + system_prompt
                + """
    
            Context: {history} \n {context}
            User: {question}"""
                + E_INST
            )
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            prompt_template = (
                B_INST
                + system_prompt
                + """
            
            Context: {context}
            User: {question}"""
                + E_INST
            )
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
    else:
        # change this based on the model you have selected.
        if history:
            prompt_template = (
                system_prompt
                + """
    
            Context: {history} \n {context}
            User: {question}
            Answer:"""
            )
            prompt = PromptTemplate(input_variables=["history", "context", "question"], template=prompt_template)
        else:
            prompt_template = (
                system_prompt
                + """
            
            Context: {context}
            User: {question}
            Answer:"""
            )
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)

    memory = ConversationBufferMemory(input_key="question", memory_key="history")

    print(f"Here is the prompt used: {prompt}")

    return (
        prompt,
        memory,
    )

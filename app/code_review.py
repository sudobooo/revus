# app/code_review.py

import logging
from langchain.prompts import PromptTemplate
from openai import OpenAIError
from app.shared_llm import get_llm

def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return ""

def review_code(file_content):
    llm = get_llm()
    prompt_template = '''
    Perform a thorough review of the following code:

    {code}

    Please consider the following:
    1. Pay attention to any potential issues that could lead to crashes or incorrect behavior.
    2. Suggest improvements in terms of performance, style, and readability.
    3. Ensure the code follows best programming practices for the given language.
    4. If there are any security vulnerabilities in the code, point them out.

    Provide specific recommendations for fixing or improving the code.
    '''
    prompt = PromptTemplate(
        input_variables=['code'],
        template=prompt_template
    )
    chain = prompt | llm
    try:
        review = chain.invoke({'code': file_content})
        return review.content if hasattr(review, 'content') else ""
    except OpenAIError as e:
        logging.error(f"Error during code review: {e}")
        return ""

def review_code_with_hints(file_content, assessment):
    llm = get_llm()
    prompt_template = '''
    Review the following code:

    {code}

    Pay special attention to the following comments from the previous review:
    {assessment}

    Please consider the following:
    1. Address the deficiencies highlighted in the previous review and improve the recommendations.
    2. Point out any other potential issues that may have been missed.
    3. Ensure clarity, usefulness, and completeness of the recommendations.
    '''
    prompt = PromptTemplate(
        input_variables=['code', 'assessment'],
        template=prompt_template
    )
    chain = prompt | llm
    try:
        review = chain.invoke({'code': file_content, 'assessment': assessment})
        return review.content if hasattr(review, 'content') else ""
    except OpenAIError as e:
        logging.error(f"Error during follow-up review: {e}")
        return ""

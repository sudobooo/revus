# app/code_review.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAIError
from .llm_client import get_llm
from .logger import log_error


class CodeReviewer:
    SYSTEM_REVIEW_PROMPT = """
    You are an expert code reviewer. Provide in-depth analysis and recommendations for the given code.
    Use best practices and give specific suggestions for improvement.
    """

    REVIEW_PROMPT = """
    Perform a thorough review of the following code:

    {code}

    Please consider the following:
    1. Pay attention to any potential issues that could lead to crashes or incorrect behavior.
    2. Suggest improvements in terms of performance, style, and readability.
    3. Ensure the code follows best programming practices for the given language.
    4. If there are any security vulnerabilities in the code, point them out.

    Provide specific recommendations for fixing or improving the code.
    """

    HINTED_REVIEW_PROMPT = """
    Review the following code:

    {code}

    Pay special attention to the following comments from the previous assessment:
    {comments}

    Please consider the following:
    1. Address the deficiencies highlighted in the previous assessment and improve the recommendations.
    2. Point out any other potential issues that may have been missed.
    3. Ensure clarity, usefulness, and completeness of the recommendations.
    """

    def __init__(self):
        self.llm = get_llm()
        self.parser = StrOutputParser()

    def review_code(self, code, comments=None):
        if comments:
            prompt = self.HINTED_REVIEW_PROMPT
            input_variables = {"code": code, "comments": comments}
        else:
            prompt = self.REVIEW_PROMPT
            input_variables = {"code": code}

        messages = [("system", self.SYSTEM_REVIEW_PROMPT), ("user", prompt)]

        prompt_template = ChatPromptTemplate.from_messages(messages)

        chain = prompt_template | self.llm | self.parser

        try:
            review = chain.invoke(input_variables)
            return review
        except OpenAIError as e:
            log_error(f"Error during code review: {e}")
            return ""

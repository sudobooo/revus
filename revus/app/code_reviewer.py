# app/code_review.py

from langchain.prompts import PromptTemplate
from openai import OpenAIError
from .llm_client import get_llm
from .logger import log_error


class CodeReviewer:
    BASIC_PROMPT = """
    Perform a thorough review of the following code:

    {code}

    Please consider the following:
    1. Pay attention to any potential issues that could lead to crashes or incorrect behavior.
    2. Suggest improvements in terms of performance, style, and readability.
    3. Ensure the code follows best programming practices for the given language.
    4. If there are any security vulnerabilities in the code, point them out.

    Provide specific recommendations for fixing or improving the code.
    """

    HINTED_PROMPT = """
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

    def review_code(self, code, comments=None):
        if comments:
            prompt_template = self.HINTED_PROMPT
            input_variables = {"code": code, "comments": comments}
        else:
            prompt_template = self.BASIC_PROMPT
            input_variables = {"code": code}

        prompt = PromptTemplate(
            input_variables=list(input_variables.keys()), template=prompt_template
        )
        chain = prompt | self.llm
        try:
            review = chain.invoke(input_variables)
            return review.content if hasattr(review, "content") else ""
        except OpenAIError as e:
            log_error(f"Error during code review: {e}")
            return ""

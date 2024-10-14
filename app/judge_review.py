# app/judge_review.py

from langchain.prompts import PromptTemplate
from openai import OpenAIError
from app.shared_llm import get_llm
import logging

def judge_review(review_text):
    llm = get_llm()
    prompt_template = '''
    Please evaluate the quality of the following code review:

    {review}

    Evaluation criteria:
    - How clearly and precisely does the review point out errors? (Score from 0 to 10)
    - How useful are the suggestions for improving the code? (Score from 0 to 10)
    - How comprehensive is the review in covering potential issues in the code? (Score from 0 to 10)

    Return the result in the following format:
    {{
        "clarity": <score>,
        "usefulness": <score>,
        "coverage": <score>,
        "overall": <overall score from 0 to 10>,
        "comments": "<comments on improving the review>"
    }}
    '''
    prompt = PromptTemplate(
        input_variables=['review'],
        template=prompt_template
    )
    chain = prompt | llm
    try:
        assessment = chain.invoke({'review': review_text})
        return assessment.content if hasattr(assessment, 'content') else ""
    except OpenAIError as e:
        logging.error(f"Error during review quality assessment: {e}")
        return "Failed to perform assessment"

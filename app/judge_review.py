from langchain.prompts import PromptTemplate
from openai import OpenAIError
from app.shared_llm import get_llm
import logging

def judge_review(review_text):
    llm = get_llm()
    prompt_template = '''
    Пожалуйста, оцени качество следующего ревью кода:

    {review}

    Критерии оценки:
    - Насколько ясно и чётко ревью указывает на ошибки? (Оценка от 0 до 10)
    - Насколько полезны предложения по улучшению кода? (Оценка от 0 до 10)
    - Насколько полно ревью покрывает возможные проблемы в коде? (Оценка от 0 до 10)

    Верни результат в следующем формате:
    {{
        "clarity": <оценка>,
        "usefulness": <оценка>,
        "coverage": <оценка>,
        "overall": <общая оценка от 0 до 10>,
        "comments": "<комментарии по улучшению ревью>"
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
        logging.error(f"Ошибка при оценке качества ревью: {e}")
        return "Не удалось провести оценку"

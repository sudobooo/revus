import logging
from langchain.prompts import PromptTemplate
from openai import OpenAIError
from app.shared_llm import get_llm

def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logging.error(f"Ошибка при чтении файла {file_path}: {e}")
        return ""

def review_code(file_content):
    llm = get_llm()
    prompt_template = '''
    Проведи качественное ревью следующего кода:

    {code}

    Пожалуйста, учти следующее:
    1. Обрати внимание на возможные ошибки, которые могут привести к сбоям или неправильному поведению.
    2. Предложи улучшения по производительности, стилю и читабельности.
    3. Убедись, что код соответствует лучшим практикам программирования для данного языка.
    4. Если в коде присутствуют уязвимости безопасности, укажи на них.

    Представь конкретные рекомендации по исправлению или улучшению.
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
        logging.error(f"Ошибка при проведении ревью: {e}")
        return ""

def review_code_with_hints(file_content, assessment):
    llm = get_llm()
    prompt_template = '''
    Проведи ревью следующего кода:

    {code}

    Обрати особое внимание на следующие комментарии по предыдущему ревью:
    {assessment}

    Пожалуйста, учти:
    1. Исправь недостатки, указанные в предыдущем ревью, и улучшай рекомендации.
    2. Укажи на любые другие возможные ошибки, которые были упущены.
    3. Обеспечь ясность, полезность и полноту рекомендаций.
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
        logging.error(f"Ошибка при повторном ревью: {e}")
        return ""

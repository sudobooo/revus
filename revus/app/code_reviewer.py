# app/code_review.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAIError
from .llm_client import get_llm
from .logger import log_error
from .config import get_config


class CodeReviewer:
    SYSTEM_REVIEW_PROMPT = """
    You are a code reviewer tasked with reviewing changes in a pull request (PR).
    Your goal is to provide a thorough, constructive, and prioritized review of the changes.
    """

    REVIEW_PROMPT = """
    Follow these instructions carefully:

    1. First, review the full context of the file where changes were made (if provided):

    <full_file_context>
    {full_file_context}
    </full_file_context>

    2. Now, examine the specific changes made in the PR:

    <file_changes>
    {file_changes}
    </file_changes>

    3. Consider any custom rules provided for this review:

    <custom_rules>
    {custom_rules}
    </custom_rules>

    4. Conduct your review based on the following criteria:

    a) Code clarity and context alignment
    b) Readability and comprehension
    c) Code complexity and structure
    d) Potential vulnerabilities
    e) Performance considerations

    5. For each issue you identify, format your review as follows:

    <review_item>
    <code_section>
    [Insert the relevant code section here]
    </code_section>
    <comment>
    [Your review comment goes here. Be polite, constructive, and explain the importance of your suggestion.]
    </comment>
    <priority>
    [Assign a priority: High, Medium, or Low]
    </priority>
    </review_item>

    6. Additional guidelines:

    - Prioritize your comments by criticality.
    - Be polite and constructive in your feedback.
    - Suggest directions for improvement rather than prescribing specific solutions.
    - Explain how your suggestions contribute to better code quality.
    - Keep in mind that your review will be read in the command line, so format accordingly.

    7. After reviewing all changes, provide a summary of your review:

    <review_summary>
    [Summarize the key points of your review, highlighting the most critical issues and overall impressions.]
    </review_summary>

    Always answer in this language: {language}.

    Your response should always end with the </review_summary> tag. Be sure to keep this in mind before you start.

    Remember to focus on the changes made in the PR, but consider the full file context when relevant.
    If you're reviewing a new file, disregard references to the full file context.

    Begin your review now.
    """

    def __init__(self):
        self.llm = get_llm({"temperature": 0.5, "top_p": 1.0})
        self.parser = StrOutputParser()

    def review_code(self, changes):
        prompt = self.REVIEW_PROMPT
        custom_rules = get_config("custom_rules", "")
        language = get_config("language", "english")

        input_variables = {
            "full_file_context": changes["file_content"],
            "file_changes": changes["changes_in_file"],
            "custom_rules": custom_rules,
            "language": language,
        }

        messages = [("system", self.SYSTEM_REVIEW_PROMPT), ("user", prompt)]

        prompt_template = ChatPromptTemplate.from_messages(messages)

        chain = prompt_template | self.llm | self.parser

        try:
            review = chain.invoke(input_variables)
            return review
        except OpenAIError as e:
            log_error(f"Error during code review: {e}")
            return ""

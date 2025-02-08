# app/code_review.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAIError
from .llm_client import get_llm
from .logger import log_error
from .config import get_config


class CodeReviewer:
    SYSTEM_PROMPT = (
        "You are a code reviewer tasked with reviewing code changes in a pull request (PR). "
        "Provide a thorough, constructive, and prioritized review."
    )

    BASE_PROMPT = "Follow these instructions carefully:"

    # Template for diff review mode (with changes)
    DIFF_PROMPT = """
    1. Please review the differences in the file:
    <file_diff>
    Base content:
    {base_content}

    Modified content:
    {modified_content}
    </file_diff>
    """

    # Template for file review mode (review the full file)
    FILE_PROMPT = """
    1. Please review the full content of the file:
    <file_content>
    {file_content}
    </file_content>
    """

    # Common review instructions (criteria, response format, etc.)
    COMMON_INSTRUCTIONS = """
    2. Evaluate the code based on clarity, readability, complexity, potential vulnerabilities, and performance.
    3. For each issue, provide your feedback in the following format:
    <review_item>
    <code_section>[Relevant code snippet]</code_section>
    <comment>[Your constructive comment]</comment>
    <priority>[High/Medium/Low]</priority>
    </review_item>
    4. End your response with a summary enclosed in <review_summary> tags.
    """

    def __init__(self):
        self.llm = get_llm({"temperature": 0.5, "top_p": 1.0})
        self.parser = StrOutputParser()

    def review_code(self, review_data: dict, mode: str = "file") -> str:
        if mode == "diff":
            dynamic_section = self.DIFF_PROMPT.format(
                base_content=review_data.get("base_content", ""),
                modified_content=review_data.get("modified_content", ""),
            )
        elif mode == "file":
            dynamic_section = self.FILE_PROMPT.format(
                file_content=review_data.get("file_content", "")
            )
        else:
            log_error(f"Unknown review mode: {mode}")
            return "Error: unknown review mode."

        custom_rules = get_config("custom_rules", "")
        if custom_rules:
            custom_rules_section = (
                f"\n<custom_rules>\n{custom_rules}\n</custom_rules>\n"
            )
        else:
            custom_rules_section = ""

        full_prompt = "\n".join(
            [
                self.BASE_PROMPT,
                dynamic_section,
                custom_rules_section,
                self.COMMON_INSTRUCTIONS,
                f"Always answer in {get_config('language', 'english')}.",
            ]
        )

        messages = [("system", self.SYSTEM_PROMPT), ("user", full_prompt)]
        prompt_template = ChatPromptTemplate.from_messages(messages)
        chain = prompt_template | self.llm | self.parser

        try:
            review = chain.invoke({})
            return review
        except OpenAIError as e:
            log_error(f"Error during code review: {e}")
            return "Error during code review."

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
from .code_reviewer import CodeReviewer

app = FastAPI(title="Code Review API")


class FileItem(BaseModel):
    name: str

    # For file review mode (without diff)
    file_content: Optional[str] = None

    # For diff review mode
    base_content: Optional[str] = Field(None, description="Original file content")
    modified_content: Optional[str] = Field(None, description="Modified file content")


class ReviewRequest(BaseModel):
    files: List[FileItem]


class ReviewResult(BaseModel):
    name: str
    review: str


@app.post("/review", response_model=List[ReviewResult])
def review_files_api(review_request: ReviewRequest):
    reviewer = CodeReviewer()
    results = []

    for file in review_request.files:
        if file.base_content is not None and file.modified_content is not None:
            review_data = {
                "base_content": file.base_content,
                "modified_content": file.modified_content,
            }
            review = reviewer.review_code(review_data, mode="diff")
        elif file.file_content is not None:
            review_data = {"file_content": file.file_content}
            review = reviewer.review_code(review_data, mode="file")
        else:
            review = "Invalid input format. Insufficient data provided for review."
        results.append(ReviewResult(name=file.name, review=review))
    return results

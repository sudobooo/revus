# app/assess_review_quality.py

def assess_review_quality(assessment):
    if assessment.get("overall", 0) < 5:
        return 'low'
    return 'high'

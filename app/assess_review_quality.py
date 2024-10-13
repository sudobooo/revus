def assess_review_quality(assessment):
    if assessment.get("overall", 0) < 5:
        return 'low'
    return 'high'

from sklearn.metrics.pairwise import cosine_similarity

from src.vectorizer import (
    vectorizer,
    tfidf_matrix,
    all_chunks,
    chunk_sources
)

from src.answer_generator import generate_multi_passage_answer


def expand_question(question):
    question_lower = question.lower()

    synonyms = {
        "high blood pressure": "hypertension",
        "blood pressure": "hypertension",
        "covid": "covid-19 coronavirus",
        "coronavirus": "covid-19",
        "sugar disease": "diabetes",
        "low blood": "anemia",
        "low iron": "anemia",
        "heart attack": "heart disease",
        "breathing problem": "asthma shortness of breath",
        "trouble breathing": "asthma shortness of breath"
    }

    expanded_question = question_lower

    for phrase, replacement in synonyms.items():
        if phrase in question_lower:
            expanded_question += " " + replacement

    return expanded_question


def search_answer(question):
    expanded_question = expand_question(question)

    question_vector = vectorizer.transform([expanded_question])

    similarities = cosine_similarity(
        question_vector,
        tfidf_matrix
    )[0]

    ranked_indexes = similarities.argsort()[::-1]

    best_match_index = ranked_indexes[0]
    best_score = similarities[best_match_index]

    if best_score < 0.08:
        return (
            "I could not find relevant medical information in the uploaded documents.",
            best_score,
            None,
            []
        )

    top_indexes = ranked_indexes[:3]

    top_chunks = [
        all_chunks[index]
        for index in top_indexes
        if similarities[index] > 0
    ]

    answer = generate_multi_passage_answer(
        top_chunks,
        expanded_question
    )

    source_document = chunk_sources[best_match_index]

    recommendations = []

    for index in top_indexes:
        recommendations.append(
            {
                "source": chunk_sources[index],
                "score": similarities[index]
            }
        )

    return answer, best_score, source_document, recommendations
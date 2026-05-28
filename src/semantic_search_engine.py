from sentence_transformers import SentenceTransformer, util

from src.vectorizer import (
    all_chunks,
    chunk_sources
)

from src.answer_generator import generate_multi_passage_answer


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

chunk_embeddings = model.encode(
    all_chunks,
    convert_to_tensor=True
)


def semantic_search(question):

    question_embedding = model.encode(
        question,
        convert_to_tensor=True
    )

    similarities = util.cos_sim(
        question_embedding,
        chunk_embeddings
    )[0]

    ranked_indexes = similarities.argsort(descending=True)

    best_index = ranked_indexes[0].item()

    best_score = similarities[best_index].item()

    if best_score < 0.2:

        return (
            "I could not find relevant medical information in the uploaded documents.",
            best_score,
            None,
            []
        )

    top_indexes = ranked_indexes[:3]

    top_chunks = []

    recommendations = []

    for index_tensor in top_indexes:

        index = index_tensor.item()

        top_chunks.append(
            all_chunks[index]
        )

        recommendations.append(
            {
                "source": chunk_sources[index],
                "score": similarities[index].item()
            }
        )

    answer = generate_multi_passage_answer(
        top_chunks,
        question
    )

    source_document = chunk_sources[best_index]

    return (
        answer,
        best_score,
        source_document,
        recommendations
    )
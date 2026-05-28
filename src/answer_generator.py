def generate_short_answer(chunk, question):
    sentences = chunk.split(".")
    question_lower = question.lower()

    intent_keywords = get_intent_keywords(question_lower)

    best_sentence = ""
    best_score = 0

    for sentence in sentences:
        sentence_lower = sentence.lower()
        score = score_sentence(sentence_lower, question_lower, intent_keywords)

        if score > best_score:
            best_score = score
            best_sentence = sentence.strip()

    if best_sentence:
        return best_sentence + "."

    return chunk


def generate_multi_passage_answer(chunks, question):
    question_lower = question.lower()
    intent_keywords = get_intent_keywords(question_lower)

    selected_sentences = []

    for chunk in chunks:
        sentences = chunk.split(".")

        best_sentence = ""
        best_score = 0

        for sentence in sentences:
            sentence_lower = sentence.lower()
            score = score_sentence(sentence_lower, question_lower, intent_keywords)

            if score > best_score:
                best_score = score
                best_sentence = sentence.strip()

        if best_sentence and best_sentence not in selected_sentences:
            selected_sentences.append(best_sentence)

    if selected_sentences:
        return ". ".join(selected_sentences[:3]) + "."

    return chunks[0]


def get_intent_keywords(question_lower):
    if "prevent" in question_lower or "prevention" in question_lower or "avoid" in question_lower:
        return [
            "prevention",
            "prevent",
            "reduce",
            "reducing",
            "avoid",
            "avoiding",
            "maintaining",
            "exercising",
            "limiting"
        ]

    elif "symptom" in question_lower or "sign" in question_lower:
        return [
            "symptoms",
            "symptom",
            "include",
            "may cause"
        ]

    elif "cause" in question_lower or "risk" in question_lower:
        return [
            "risk",
            "risk factors",
            "cause",
            "causes",
            "include"
        ]

    elif "treat" in question_lower or "treatment" in question_lower or "management" in question_lower or "manage" in question_lower:
        return [
            "management",
            "treatment",
            "treat",
            "include",
            "medication",
            "therapy"
        ]

    else:
        return []


def score_sentence(sentence_lower, question_lower, intent_keywords):
    score = 0

    for keyword in intent_keywords:
        if keyword in sentence_lower:
            score += 5

    question_words = question_lower.split()

    for word in question_words:
        if word in sentence_lower:
            score += 1

    return score
def evaluate_response(user_question, system_answer, chunks):
    score = 0

    relevance_hits = sum([
        1 for c in chunks
        if any(word.lower() in c.lower() for word in user_question.split())
    ])

    relevance_ratio = relevance_hits / len(chunks)

    if relevance_ratio > 0.7:
        score += 4
    elif relevance_ratio > 0.4:
        score += 2

    if len(system_answer) > 50:
        score += 3

    if any(c[:40] in system_answer for c in chunks):
        score += 3

    score = min(score, 10)

    reason = (
        f"Puntuación {score}: ratio_relevancia={relevance_ratio:.2f}, "
        f"longitud_respuesta={len(system_answer)}. "
        f"Los fragmentos parecen parcialmente anclados al contexto."
    )

    return {
        "puntuacion": score,
        "motivo": reason,
    }
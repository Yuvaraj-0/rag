def reciprocal_rank_fusion(
    vector_results: list[dict],
    bm25_results: list[dict],
    k: int = 60,
    limit: int = 10
):
    """
    Combine vector-search and BM25 rankings using
    Reciprocal Rank Fusion (RRF).

    RRF formula:

        RRF score = 1 / (k + rank)

    A chunk appearing in both result lists gets
    a higher combined score.
    """

    scores = {}
    metadata = {}

    # -----------------------------------
    # 1. Process vector search results
    # -----------------------------------

    for rank, result in enumerate(vector_results, start=1):

        chunk_id = result["chunk_id"]

        if chunk_id not in scores:
            scores[chunk_id] = 0.0

        scores[chunk_id] += 1 / (k + rank)

        if chunk_id not in metadata:
            metadata[chunk_id] = dict(result)

        metadata[chunk_id]["vector_score"] = result["score"]

    # -----------------------------------
    # 2. Process BM25 results
    # -----------------------------------

    for rank, result in enumerate(bm25_results, start=1):

        chunk_id = result["chunk_id"]

        if chunk_id not in scores:
            scores[chunk_id] = 0.0

        scores[chunk_id] += 1 / (k + rank)

        if chunk_id not in metadata:
            metadata[chunk_id] = dict(result)

        metadata[chunk_id]["bm25_score"] = result["score"]

    # -----------------------------------
    # 3. Sort by RRF score
    # -----------------------------------

    ranked_results = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    # -----------------------------------
    # 4. Build final results
    # -----------------------------------

    final_results = []

    for chunk_id, rrf_score in ranked_results[:limit]:

        result = dict(metadata[chunk_id])

        result["rrf_score"] = rrf_score

        result.setdefault("vector_score", None)
        result.setdefault("bm25_score", None)

        final_results.append(result)

    return final_results
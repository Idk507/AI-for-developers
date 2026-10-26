Interview scenario
An enterprise RAG assistant previously achieved Recall@5 of 0.85.

After replacing its embedding model, Recall@5 decreases to 0.70.

However, users report that the generated answers seem more accurate.

Interview question: How could retrieval recall decrease while perceived answer quality improves?

Consider whether the new embedding model retrieves fewer irrelevant documents, whether a reranker changes the ordering of results, and whether the evaluation dataset adequately represents real user questions.

Also consider how you would distinguish retrieval improvements from generation improvements.

Prepare a two-minute explanation describing the experiments you would run before deciding whether to roll back the embedding model.
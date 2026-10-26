"""  

Imagine you're building an enterprise RAG assistant that retrieves documents from a vector database.

A user asks:
What is the company's reimbursement policy?

Your retrieval system returns five documents.

However, only two of those documents are relevant to the question.

How do you determine whether your retrieval system is performing well?

Simply checking whether the vector database returned results is insufficient. You need metrics that measure retrieval quality.

Today's engineering assignment is to implement three commonly used information-retrieval metrics: Precision@K, Recall@K, and Mean Reciprocal Rank (MRR).
Precision@K
Precision@K measures how many of the first K retrieved documents are relevant.

For example, suppose the top five retrieved documents contain three relevant documents.

Precision@5 = 3 / 5 = 0.60.
Recall@K
Recall@K measures how many of the known relevant documents were successfully retrieved within the first K results.

Suppose four documents are relevant to the query, but your top five results contain only three of them.

Recall@5 = 3 / 4 = 0.75.
Reciprocal Rank and MRR
Reciprocal Rank measures how early the first relevant document appears.

If the first relevant document appears at rank two, its reciprocal rank is 1/2 = 0.5.

If it appears at rank one, the reciprocal rank is 1.0.

MRR is the mean of reciprocal ranks across multiple queries. For a single query, your function will calculate reciprocal rank, which can later be averaged into MRR.
Your implementation requirements
Implement the following function:
def evaluate_retrieval(    relevant_doc_ids: list[str],    retrieved_doc_ids: list[str],    k: int,) -> dict[str, float]:    """    Evaluate ranked retrieval results for one query.    Return:        precision_at_k        recall_at_k        reciprocal_rank    Requirements:        k must be a positive integer.        relevant_doc_ids must be nonempty.        Document IDs must be nonempty strings.        Duplicate IDs must not inflate metric values.        Never mutate input lists.    """    pass


Evaluation rules
Treat relevant_doc_ids as the ground-truth set of relevant documents.

Treat retrieved_doc_ids as the ranked retrieval output, ordered from most relevant to least relevant according to the retrieval system.

If the retrieved list contains duplicate document IDs, retain only their first occurrence before calculating ranks and metrics.

Evaluate the first k unique retrieved documents.

For Precision@K, use k as the denominator even when fewer than k results are returned. This is the convention for today's exercise.

If no relevant document appears within the first k results, reciprocal rank must be zero.
Example
relevant_doc_ids = ["doc_A", "doc_C"]retrieved_doc_ids = [    "doc_B",    "doc_A",    "doc_D",    "doc_C",]k = 3


The first three retrieved documents are B, A, and D.

Only A is relevant.

Therefore, the expected metrics are:
Metric	Expected value
Precision@3	0.3333
Recall@3	0.5000
Reciprocal Rank@3	0.5000


The first relevant document appears at rank two.

Your function should return:
{    "precision_at_k": 1 / 3,    "recall_at_k": 1 / 2,    "reciprocal_rank": 1 / 2,}


Required tests
Write at least six tests using pytest.
Test scenario	Expected behavior
First retrieved document is relevant	Reciprocal rank is 1.0
No retrieved document is relevant	All metrics are zero
All ground-truth documents appear within top K	Recall@K is 1.0
Retrieved list is empty	All metrics are zero
Retrieved documents contain duplicates	Duplicates do not inflate metrics
k=0	Raise ValueError
Ground-truth list is empty	Raise ValueError
Input contains invalid document IDs	Raise ValueError or TypeError


Use pytest.approx() when comparing floating-point results.
Complexity targets
Let r represent the number of ground-truth document IDs and n the number of retrieved document IDs.

Aim for O(r + n) time and O(r + n) auxiliary space in the worst case, using suitable data structures.

You should not need machine learning libraries, vector databases, or LLM APIs for this exercise.
Why this matters for Applied AI Engineering
In production RAG systems, retrieval quality directly influences what evidence is available to the generation model.

Even a powerful LLM can produce an incorrect answer if the retrieval system fails to return the necessary supporting documents.

These metrics help compare embedding models, reranking strategies, chunking configurations, and retrieval parameters.

However, retrieval metrics alone cannot determine whether the final generated answer is factually correct or properly grounded in the retrieved evidence.

A complete RAG evaluation pipeline also needs answer-level assessments such as factual correctness, faithfulness, citation accuracy, and task completion.

For enterprise systems, evaluation datasets must respect document permissions. Retrieved document identifiers, queries, and relevance labels may contain sensitive business information, so access controls and data-retention policies matter.

For observability, record evaluation-run identifiers, dataset versions, retrieval configuration versions, and aggregate metrics. Avoid exposing sensitive document contents in logs.

"""
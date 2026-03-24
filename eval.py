def compute_recall(retrieved, ground_truth):
    hits = sum([1 for doc in retrieved if doc in ground_truth])
    return hits / len(ground_truth)

def hallucination_check(answer, context):
    return answer not in context  # naive baseline
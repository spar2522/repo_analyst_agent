import math


def cosine_similarity(
    a: list[float],
    b: list[float],
) -> float:
    """Compute the cosine similarity between two vectors.

    Cosine similarity is the dot product of the vectors divided by the product of their magnitudes.

    Args:
        a (list[float]): The first vector.
        b (list[float]): The second vector.

    Returns:
        float: The cosine similarity between the vectors.

    Raises:
        ValueError: If either vector is empty or if they have different lengths.
        ZeroDivisionError: If either vector has a magnitude of zero.
    """
    if not a or not b:
        raise ValueError("Vectors cannot be empty.")
    if len(a) != len(b):
        raise ValueError("Vectors must be of the same length.")

    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(x * x for x in b))

    if magnitude_a == 0 or magnitude_b == 0:
        raise ZeroDivisionError("One or both vectors have zero magnitude.")

    return dot_product / (magnitude_a * magnitude_b)
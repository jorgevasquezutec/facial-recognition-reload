import numpy as np


def convert_list_to_array(list):
    return np.array(list)

def euclidean_distance(vector1, vector2):
    return np.linalg.norm(vector1 - vector2)


def manhattan_distance(vector1, vector2):
    return np.sum(np.abs(vector1 - vector2))

def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, vector2)
    norm_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
    return dot_product / norm_product
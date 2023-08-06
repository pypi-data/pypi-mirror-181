from typing import  List
from sklearn.feature_extraction.text import TfidfVectorizer
from sparse_dot_topn import awesome_cossim_topn
import pandas as pd
import string


def tfidf_sim_pipeline(
        corpus_a: List[str],
        corpus_b: List[str],
        top_k_similarity: int = 3,
        similarity_lower_bound: float = 0.,
        return_indices = False
):
    '''
    pipe to compute tfidf similarity of given two corpora

    :param similarity_lower_bound:
    :param top_k_similarity:
    :param corpus_a: list[str], N samples
    :param corpus_b: list[str], M samples
    :param return_indices: whether to return the indicies of matched texts in corpus_b
    :return:
    '''
    assert top_k_similarity < min(len(corpus_a),len(corpus_b))

    corpora = corpus_a + corpus_b
    vectorizer = TfidfVectorizer()
    temp = vectorizer.fit_transform(corpora)

    m1 = temp[:len(corpus_a)] # N,D
    m2 = temp[len(corpus_a):] # M,D


    sim = awesome_cossim_topn(m1,m2.transpose(),top_k_similarity, similarity_lower_bound) # NxM
    nonzero_x , nonzero_y = sim.nonzero()
    data = [ [x] for x in corpus_a ]
    columns = ["Text"]
    for j in range(top_k_similarity):
        columns.append(f"Top-{j+1} Similarity")

    for i,j in zip(nonzero_x,nonzero_y):
        if return_indices:
            data[i].append((corpus_b[j],int(j)))
        else:
            data[i].append(corpus_b[j])

    ret = pd.DataFrame(data, columns=columns)
    return ret


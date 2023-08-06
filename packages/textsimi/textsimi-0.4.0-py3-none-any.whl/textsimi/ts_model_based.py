from .ts import BaseTextSimilarity
import torch
import torch.nn as nn

class TextSimilarityModelBased(BaseTextSimilarity):
    '''
    compare the similarity between two vectors/embeddings of texts
    '''

    def __to_tensor__(self, func:callable):
        def new_func(a,b):
            if not isinstance(a,torch.Tensor):
                a = torch.Tensor(a)
            if not isinstance(b, torch.Tensor):
                b = torch.Tensor(b)
            return func(a,b)
        return new_func


    def __setup__(self):
        self._current_algo = self.__to_tensor__(nn.CosineSimilarity(dim=-1, eps=1e-6))

    def change_distance_func(self, dist_func:callable):
        self._current_algo = self.__to_tensor__(dist_func)

ts_model_based = TextSimilarityModelBased()
import pandas as pd
from gensim.models import Word2Vec
import ast
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

class PrepWord2VecRecommender:
    def __init__(self):
        self.vectors = None
        self.model_data_finally = None
        self.get_vectors_and_finaldata()

    def get_vectors_and_finaldata(self):
        current_path = Path(__file__).parent
        parent_path = current_path.parent

        # word2vec_model = Word2Vec.load(f'{current_path}/word2vec_attraction.model')
        model_data_finally = pd.read_csv(f'{parent_path}/data/finally_processed.csv')
        
        # def get_average_word2vec_vector(words):
        #     word_vectors = [word2vec_model.wv[word] for word in words if word in word2vec_model.wv]
        #     if len(word_vectors) == 0:
        #         return np.zeros(word2vec_model.vector_size)
        #     return np.mean(word_vectors, axis=0)

        # self.vectors = np.array([get_average_word2vec_vector(feature) for feature in model_data_finally['features']])
        self.vectors = np.load(f'{parent_path}/data/vectors.npy')
        self.model_data_finally = model_data_finally

class Word2VecRecommender:
    def __init__(self, vectors, model_data_finally):
        self.vectors = vectors
        self.model_data_finally = model_data_finally

    def get_recommended_attractions(self, place_id):
        # 특정 관광지의 인덱스를 찾음
        place_row = self.model_data_finally[self.model_data_finally['place_id'] == place_id]
        if place_row.empty:
            raise ValueError(f"place_id '{place_id}' not found.")
        
        place_idx = place_row.index[0]
        
        # 해당 관광지와 모든 관광지의 유사도 계산
        cosine_sim = cosine_similarity([self.vectors[place_idx]], self.vectors)
        
        # 유사도 높은 관광지 찾기
        similarity_scores = list(enumerate(cosine_sim[0]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        # 유사한 관광지 정보 출력 (본인 제외)
        similar_place_ids = []
        for idx, score in similarity_scores[1:5]:  # 본인 제외 후 상위 10개
            similar_place_ids.append(self.model_data_finally['place_id'][idx])
        
        return similar_place_ids

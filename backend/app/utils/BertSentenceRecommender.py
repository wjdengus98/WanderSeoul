import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from pathlib import Path

global bert_model
bert_model = SentenceTransformer('all-MiniLM-L6-v2')  # 경량화된 Sentence-BERT 모델

class PrepBertSentenceRecommender:
    def __init__(self):
        self.model = None
        self.model_data_finally = None
        self.all_embeddings = None
        self.get_model_and_finaldata()

    def get_model_and_finaldata(self):
        current_path = Path(__file__).parent
        parent_path = current_path.parent       
        
        model_data_finally = pd.read_csv(f'{parent_path}/data/processed_places.csv')
        # model_data_finally['feature_embeddings'] = model_data_finally['features'].apply(lambda x: bert_model.encode(x))
        
        self.model = bert_model
        self.model_data_finally = model_data_finally
        self.all_embeddings = np.load(f'{parent_path}/data/all_embeddings.npy')

class BertSentenceRecommender:
    def __init__(self, model, model_data_finally, all_embeddings):
        self.model = model
        self.model_data_finally = model_data_finally
        self.all_embeddings = all_embeddings

    def recommend_places_by_sentence(self, input_sentence, top_n=20):
        """
        입력 문장을 기반으로 유사한 장소 추천.

        Args:
            input_sentence (str): 사용자가 입력한 문장.
            top_n (int): 추천할 장소의 개수.

        Returns:
            place_ids (list): 추천 결과.
        """
        # 입력 문장을 Sentence-BERT로 임베딩
        input_embedding = self.model.encode(input_sentence)
        # 저장된 모든 장소의 임베딩 로드
        all_embeddings = self.all_embeddings
        
        # 입력 문장과 모든 장소 간의 코사인 유사도 계산
        similarities = cosine_similarity([input_embedding], all_embeddings)[0]
        # 유사도를 데이터프레임에 추가
        self.model_data_finally['similarity'] = similarities
        
        # 유사도에 따라 상위 N개 장소 추천
        recommendations = self.model_data_finally.sort_values(by='similarity', ascending=False).head(top_n)
        
        # 유사한 관광지 정보 출력 (본인 제외)
        recommended_place_ids = []
        for place_id in recommendations['place_id']:
            recommended_place_ids.append(place_id)
        
        return recommended_place_ids

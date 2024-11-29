import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from pathlib import Path

class AutorecWord2VecRecommender:
    def __init__(self):
        current_path = Path(__file__).parent
        parent_path = current_path.parent
        
        # 필요한 디바이스 설정
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # 사용자 및 장소 ID 매핑을 위한 인코더 초기화
        user_encoder = LabelEncoder()
        place_encoder = LabelEncoder()

        # 사용자-장소 평점 데이터 로드
        model_data_GLocal = pd.read_csv(f'{parent_path}/data/glocal.csv')  # 실제 사용자-장소 평점 데이터

        # 사용자 및 장소 ID 인코딩
        model_data_GLocal['user_id'] = user_encoder.fit_transform(model_data_GLocal['user_name'])
        model_data_GLocal['place_id_encoded'] = place_encoder.fit_transform(model_data_GLocal['place_id'])

        # 사용자 수 및 장소 수 확인
        num_users = model_data_GLocal['user_id'].nunique()
        num_places = model_data_GLocal['place_id_encoded'].nunique()

        # Word2Vec 임베딩 데이터 로드
        model_data_word2vec = pd.read_csv(f'{parent_path}/data/word2vec.csv')

        # NaN 값 처리 (필요에 따라)
        model_data_word2vec.fillna(0, inplace=True)  # NaN 값을 0으로 대체

        # 특징 벡터를 PyTorch 텐서로 변환
        item_content = model_data_word2vec.iloc[:, 1:].values.astype(np.float32)  # 올바른 데이터 타입으로 변환
        item_content = torch.tensor(item_content, dtype=torch.float32).to(device)

        # 사용자-장소 평점 데이터에서 사용자-장소 매트릭스 생성
        train_matrix = np.zeros((num_users, num_places))  # 사용자-장소 매트릭스 초기화

        for row in model_data_GLocal.itertuples():
            train_matrix[row.user_id, row.place_id_encoded] = row.user_rating  # 평점 저장

        # 모델 정의 (HybridAutorec 모델을 정의해야 함)
        class HybridAutorec(nn.Module):
            def __init__(self, input_size, hidden_sizes, num_places, embedding_dim=1000, dropout_rate=0.5):
                super(HybridAutorec, self).__init__()
                self.encoder = nn.Sequential(
                    nn.Linear(input_size, hidden_sizes[0]),
                    nn.ReLU(),
                    nn.BatchNorm1d(hidden_sizes[0]),
                    nn.Dropout(dropout_rate),
                    nn.Linear(hidden_sizes[0], hidden_sizes[1]),
                    nn.ReLU(),
                    nn.BatchNorm1d(hidden_sizes[1]),
                    nn.Dropout(dropout_rate)
                )
                self.decoder = nn.Sequential(
                    nn.Linear(hidden_sizes[1], hidden_sizes[0]),
                    nn.ReLU(),
                    nn.BatchNorm1d(hidden_sizes[0]),
                    nn.Dropout(dropout_rate),
                    nn.Linear(hidden_sizes[0], input_size),
                    nn.Sigmoid()
                )
                self.content_embedding = nn.Linear(embedding_dim, hidden_sizes[1])

            def forward(self, user_place_input, content_input):
                encoded = self.encoder(user_place_input)
                content_encoded = self.content_embedding(content_input)
                combined = encoded + content_encoded
                decoded = self.decoder(combined)
                return decoded

        # 모델 로드
        model = HybridAutorec(num_places, hidden_sizes=[128, 64], num_places=num_places).to(device)
        model.load_state_dict(torch.load(f'{current_path}/autorec_word2vec.pth', map_location=device))  # 모델 로드
        model.eval()

        self.device = device
        self.user_encoder = user_encoder
        self.train_matrix = train_matrix
        self.model_data_word2vec = model_data_word2vec
        self.item_content = item_content
        self.model = model

    # 추천 함수 정의
    def recommend_places(self, user_name, num_recommendations=5):
        # 사용자 이름을 ID로 변환
        user_id = self.user_encoder.transform([user_name])[0]

        # 사용자-장소 매트릭스에서 해당 사용자에 대한 벡터 추출
        user_vector = torch.tensor(self.train_matrix[user_id], dtype=torch.float32).to(self.device).unsqueeze(0)  # GPU로 이동

        # 콘텐츠 임베딩을 모델에 전달
        with torch.no_grad():
            outputs = self.model(user_vector, self.item_content)  # 예측값 계산

        # 예측된 평점과 함께 장소 ID와 매핑
        predicted_ratings = outputs.cpu().numpy().flatten()
        place_ids = self.model_data_word2vec['place_id'].values  # 원래 place_id 가져오기

        # 예측된 평점이 0이 아닌 장소만 필터링
        recommendations = []
        for place_id, rating in zip(place_ids, predicted_ratings):
            if rating > 0:
                recommendations.append((place_id, rating))  # 원래 place_id 사용

        # 평점 기준으로 정렬하여 상위 추천 장소 선택
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:num_recommendations]

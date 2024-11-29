import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const WriteReview = ({ onAddReview }) => {
    const [reviewText, setReviewText] = useState('');
    const [username, setUsername] = useState('');
    const [rating, setRating] = useState(5);
    const navigate = useNavigate();

    const handleSubmit = () => {
        if (reviewText && username) {
            const newReview = { username, rating, text: reviewText };
            if (typeof onAddReview === 'function') {
                onAddReview(newReview); // 상위 컴포넌트에 리뷰 추가
                navigate('/'); // 작성 후 상세 페이지로 이동
            } else {
                console.error('onAddReview is not a function');
            }
        } else {
            alert('이름과 리뷰 내용을 입력하세요.');
        }
    };

    return (
        <div className="write-review-container">
            <h2>리뷰 작성하기</h2>
            <input
                type="text"
                placeholder="사용자 이름"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <select value={rating} onChange={(e) => setRating(Number(e.target.value))}>
                <option value={5}>5</option>
                <option value={4}>4</option>
                <option value={3}>3</option>
                <option value={2}>2</option>
                <option value={1}>1</option>
            </select>
            <textarea
                placeholder="리뷰 내용을 입력하세요"
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
            />
            <button onClick={handleSubmit}>제출</button>
        </div>
    );
}

export default WriteReview;



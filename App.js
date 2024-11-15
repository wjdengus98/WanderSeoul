import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Login from './Login'; // 로그인 컴포넌트 임포트
import './App.css';

function App() {
  const [showLoginModal, setShowLoginModal] = useState(false); // 모달을 열고 닫을 상태

  const openLoginModal = () => {
    setShowLoginModal(true); // 로그인 모달 열기
  };

  const closeLoginModal = () => {
    setShowLoginModal(false); // 로그인 모달 닫기
  };

  return (
    <Router>
      <div className="App">
        <div className="black-nav">
          <div>Recommend Seoul</div>
          {/* 로그인 버튼 클릭 시 모달 열기 */}
          <button onClick={openLoginModal}>Login/Join</button>
        </div>
        <h2>Welcome to Seoul</h2>

        {/* 모달이 열렸을 때만 Login 컴포넌트를 렌더링 */}
        {showLoginModal && (
          <div className="modal-overlay" onClick={closeLoginModal}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <Login closeModal={closeLoginModal} />
            </div>
          </div>
        )}

        {/* 라우터 설정 */}
        <Routes>
          <Route path="/" element={<h1>메인 페이지</h1>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

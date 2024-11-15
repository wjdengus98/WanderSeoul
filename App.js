import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Login from './Login';
import './App.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true); // 로그인 성공 시 상태 변경
  };

  const handleLogout = () => {
    setIsLoggedIn(false); // 로그아웃 시 상태 변경
  };

  return (
    <Router>
      <div className="App">
        {/* 네비게이션 바 */}
        <div className="black-nav">
          <div>Recommend Seoul</div>
          {!isLoggedIn ? (
            <Link to="/login">
              <button>Login/Join</button>
            </Link>
          ) : (
            <button onClick={handleLogout}>Logout</button>
          )}
        </div>

        {/* 라우트 설정 */}
        <Routes>
          <Route path="/" element={<MainPage />} />
          <Route
            path="/login"
            element={<Login onLoginSuccess={handleLogin} />}
          />
        </Routes>
      </div>
    </Router>
  );
}

// 메인 페이지 컴포넌트
function MainPage() {
  return (
    <div>
      <h1>Welcome to Seoul</h1>
      <p>This is the main page.</p>
    </div>
  );
}

export default App;

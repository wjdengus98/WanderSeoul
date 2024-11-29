import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import Login from './Login';
import Signup from './Signup';
import AttractionsByTags from './AttractionsByTags';
import AttractionsBySearch from './AttractionsBySearch';
import TouristSpotDetail from './TouristSpotDetail';
import WriteReview from './WriteReview';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import './MainPage.css';
import './App.css';
import logoImage from './images/projectlogo.png'; // 로고 이미지 경로 추가

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');  // 검색어 상태 추가
  const [sidebarOpen, setSidebarOpen] = useState(false); // 사이드바 상태 추가
  const [showMore, setShowMore] = useState(false); // 하위 항목 표시 상태 추가
  const [selectedTags, setSelectedTags] = useState([]);
  const accessToken = localStorage.getItem('accessToken');
  const userName = localStorage.getItem('userName');
  
  const handleLogin = (accessToken) => {
    if (accessToken) {
      setIsLoggedIn(true);
    }
  };
  
  const handleLogout = () => {
    const isConfirmed = window.confirm('Would you like to log out?');
    if (isConfirmed) {
      setIsLoggedIn(false);
      localStorage.removeItem('accessToken');
    }
  };

  const handleToMain = () => {
    setSearchQuery('')
  }

  // const handleToggleSidebar = () => {
  //   setSidebarOpen(!sidebarOpen);
  // };

  // const handleToggleMore = () => {
  //   setShowMore(!showMore);
  // }; // 하위 항목 토글 함수

  useEffect(() => {
    handleLogin(accessToken);
  }, [accessToken]);

  return (
    <Router>
      <div className="App">
        {/* 네비게이션 바 */}
        <Navigation
          isLoggedIn={isLoggedIn}
          userName={userName}
          handleLogout={handleLogout}
          handleToMain={handleToMain}
          setSearchQuery={setSearchQuery}
          selectedTags={selectedTags}
          setSelectedTags={setSelectedTags}
        />
        {/* 라우트 설정 */}
        <Routes>
          <Route path="/" element={<MainPage searchQuery={searchQuery} setSearchQuery={setSearchQuery} />} />
          <Route path="/login" element={<Login onLoginSuccess={handleLogin} />} />
          <Route path="/signup" element={<Signup setIsLoggedIn={setIsLoggedIn} />} />
          <Route path="/attractionsByTags" element={<AttractionsByTags selectedTags={selectedTags} />} />
          <Route path="/tourist-spot/:placeId" element={<TouristSpotDetail />} />
          <Route path="/write-review/:placeId" element={<WriteReview />} />
          <Route path="/attractionsBySearch" element={<AttractionsBySearch searchQuery={searchQuery} />} />
        </Routes>
      </div>
    </Router>
  );
}

function Navigation({ isLoggedIn, userName, handleLogout, handleToMain, setSearchQuery, selectedTags, setSelectedTags }) {
  const navigate = useNavigate();

  return (
    <div>
      <Sidebar selectedTags={selectedTags} setSelectedTags={setSelectedTags} />
      <Navbar />
      <div className="black-nav">
        {isLoggedIn ? (
          <div>
            <span>Welcome {userName}! </span>
            <button onClick={handleLogout} /*style={{ marginRight: '10px' }}*/>Logout</button>
          </div>
        ) : (
          <div>
            <Link to="/login" className="nav-text">Login</Link>
            <span style={{ marginLeft: '10px' }}>/</span>
            <Link to="/signup" className="nav-text">Sign Up</Link>
          </div>
        )}
        <span style={{ marginLeft: '10px' }}> </span>
        <Link to="/"><button onClick={handleToMain}>Main</button></Link>
      </div>
    </div>
  );
}

  // 메인 페이지 컴포넌트
function MainPage({ searchQuery, setSearchQuery }) {
  const navigate = useNavigate();

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    navigate('/attractionsBySearch');
  };

  return (
      // 로고 추가
      <div className="logo-search-container">
        <div className="logo-container">
          <img src={logoImage} alt="logo" className="logo" />
          <h1>Wander Seoul</h1>
        </div>
        <div className="main-content">
          <form onSubmit={handleSearchSubmit} style={{ marginBottom: '20px' }}>
            <input type="text" value={searchQuery} onChange={handleSearchChange} placeholder="Search for an attraction" className="search-input"/>
            <button type="submit" className="search-button">Search</button>
          </form>
        </div>
      </div>
    );
}

export default App;

import React, { useState } from 'react';
import './MainPage.css';

const MainPage = ({ items }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // 사이드바 상태
  const [selectedTags, setSelectedTags] = useState([]); // 선택된 태그 상태

  const tags = ['Culture', 'Nature', 'Theme Park', 'Family Friendly', 'History']; // 태그 목록

  // 사이드바 토글 함수
  const toggleSidebar = () => {
    setIsSidebarOpen((prevState) => !prevState);
  };

  // 태그 선택/해제 함수
  const handleTagSelection = (tag) => {
    setSelectedTags((prevTags) =>
      prevTags.includes(tag)
        ? prevTags.filter((t) => t !== tag) // 태그가 이미 선택된 경우 제거
        : [...prevTags, tag] // 선택되지 않은 경우 추가
    );
  };

  // 필터링된 아이템 계산
  const filteredItems = items.filter((item) =>
    selectedTags.length === 0 || selectedTags.some((tag) => item.features.includes(tag))
  );

  return (
    <div className="main-page">
      {/* 사이드바 버튼 */}
      <button className="sidebar-toggle-button" onClick={toggleSidebar}>
        {isSidebarOpen ? '닫기' : '필터'}
      </button>

      {/* 사이드바 */}
      {isSidebarOpen && (
        <div className="sidebar">
          <h3>필터 선택</h3>
          <ul>
            {tags.map((tag) => (
              <li key={tag}>
                <label>
                  <input
                    type="checkbox"
                    checked={selectedTags.includes(tag)}
                    onChange={() => handleTagSelection(tag)}
                  />
                  {tag}
                </label>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 메인 콘텐츠 */}
      <div className="content">
        <h1>Welcome to Seoul</h1>
        {filteredItems.length > 0 ? (
          <ul className="tourist-spot-list">
            {filteredItems.map((item) => (
              <li key={item.id}>
                <h3>{item.name}</h3>
                <p>Category: {item.category}</p>
                <p>Features: {item.features.join(', ')}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>선택된 태그에 해당하는 관광지가 없습니다.</p>
        )}
      </div>
    </div>
  );
};

export default MainPage;


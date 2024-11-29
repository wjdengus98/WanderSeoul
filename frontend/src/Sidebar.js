import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Sidebar.css';

const Sidebar = ({ selectedTags, setSelectedTags }) => {
    const [isOpen, setIsOpen] = useState(false); // 상태 관리
    const [tags, setTags] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const pageSize = 15;
    const navigate = useNavigate();

    const handleToggle = () => {
        if (!isOpen) {
            setSelectedTags([]);
        }
        setIsOpen(!isOpen); // 열림/닫힘 상태 토글
    };

    const handleClick = (item) => {
        setSelectedTags((prevSelected) => {
            if (prevSelected.includes(item)) {
                // 이미 선택된 항목이면 제거
                return prevSelected.filter(selected => selected !== item);
            } else {
                // 선택되지 않은 항목이면 추가
                return [...prevSelected, item];
            }
        });
    };
    
    const fetchTags = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`http://localhost:8000/tags?page=${currentPage}&size=${pageSize}`);

            if (!response.status === 200) {
                throw new Error('Failed to fetch tags');
            }

            setTags(response.data.items);
            setTotalPages(response.data.pages);
        } catch (error) {
            setError(error.response ? JSON.stringify(error.response.data.detail) : error.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTags();
    }, [currentPage]);

    const handlePageChange = (page) => {
        setSelectedTags([]);
        setCurrentPage(page);
    };

    const handleRecommendClick = () => {
        if (selectedTags.length === 0) {
          alert('Please select tag.');
          return;
        }

        navigate('/attractionsByTags', { selectedTags });
    };
      
    return (
        <div className={`sidebar ${isOpen ? 'open' : ''}`}> {/* 열렸을 때 open 클래스 추가 */}
            <div className="toggle-title" onClick={handleToggle}>
                <span className="toggle-symbol">{isOpen ? '−' : '≡'}</span>
            </div>
            {isOpen && (
                <div className="sidebar-content">
                    <h2>Category</h2>
                    <ul>
                        {tags.map(tag => (
                            <li
                                key={tag.tag_id}
                                onClick={() => handleClick(tag.tag_id)}
                                className={selectedTags.includes(tag.tag_id) ? 'selected' : ''}
                            >
                                {tag.tag_name} {/*selectedTags.includes(tag.tag_id) && <span className="tag"></span>*/}
                            </li>
                        ))}
                    </ul>
                    <div className="sidebar-pagination">
                        <button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>prev</button>
                        <span>{currentPage} / {totalPages}</span>
                        <button onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>next</button>
                    </div>
                    <div className="recommend">
                        <button onClick={handleRecommendClick}>Recommend</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Sidebar;



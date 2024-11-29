import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './AttractionsByTags.css';

export default function AttractionsByTags({ selectedTags }) {
    const [attractions, setAttractions] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const pageSize = 10;

    const fetchAttractionByTags = async () => {
        if (selectedTags.length === 0) {
          return;
        }
    
        setLoading(true);
        try {
          const queryString = selectedTags.map(tag => `tags=${tag}`).join('&');
          let response = await axios.get(`http://localhost:8000/attractions/by_tags/?${queryString}&page=${currentPage}&size=${pageSize}`);
          
          if (response.status !== 200) {
            throw new Error('Failed to fetch attractions');
          }

          if (response.data.pages < currentPage) {
            setCurrentPage(1);
            response = await axios.get(`http://localhost:8000/attractions/by_tags/?${queryString}&page=${currentPage}&size=${pageSize}`);
          }
          
          setAttractions(response.data.items);
          setTotalPages(response.data.pages);
        } catch (error) {
          setError(error.response ? JSON.stringify(error.response.data.detail) : error.message);
        } finally {
          setLoading(false);
        }
    };

    useEffect(() => {
        fetchAttractionByTags();
    }, [selectedTags, currentPage]);
    

    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    return (
    <div className="attraction-page">
      <div className="attraction-header">
        <h1>Attractions</h1>
      </div>
      
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
      {attractions.length > 0 && (
        <div className="attraction-container">
          {attractions.map((attraction) => (
            <Link to={`/tourist-spot/${attraction.place_id}`} key={attraction.place_id} style={{textDecoration: 'none'}}>
              <div className="attraction-item">
                <table>
                  <tr>
                    <td width="30%" align="right"><img src={attraction.cover_image_url} alt={attraction.place_name} width="200" height="150" /></td>
                    <td align="left"><b>{attraction.place_name}</b><br/>{attraction.address}</td>
                  </tr>
                </table>
              </div>
            </Link>
          ))}
        </div>
      )}
      <div className="attraction-pagination">
        <button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>Previous</button>
        <span>{currentPage} / {totalPages}</span>
        <button onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>Next</button>
      </div>
    </div>
  );
}
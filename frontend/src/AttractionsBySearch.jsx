import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './AttractionsBySearch.css';

export default function AttractionsBySearch({ searchQuery }) {
    const [attractions, setAttractions] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    const fetchAttractionBySearch = async () => {
        if (searchQuery.length === 0) {
          return;
        }
    
        setLoading(true);
        try {
          const response = await axios.get(`http://localhost:8000/attractions/by_search/?search_query=${searchQuery}`);
          
          if (response.status !== 200) {
            throw new Error('Failed to fetch attractions');
          }
          
          setAttractions(response.data);
        } catch (error) {
          setError(error.response ? JSON.stringify(error.response.data.detail) : error.message);
        } finally {
          setLoading(false);
        }
    };

    useEffect(() => {
        fetchAttractionBySearch();
    }, [searchQuery]);

    return (
    <div className="attraction-page">
      <div className="attraction-header">
        <h1>Recommended Attractions</h1>
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
    </div>
  );
}
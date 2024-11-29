import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import './TouristSpotDetail.css';

const TouristSpotDetail = () => {
  const {placeId} = useParams();
  const [reviews, setReviews] = useState([]);
  const [attraction, setAttraction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const userId = localStorage.getItem('userId');
  const userName = localStorage.getItem('userName');
  const [rating, setRating] = useState(0);
  const [reviewText, setReviewText] = useState('');
  const [recommendedAttractions, setRecommendedAttractions] = useState([]);
  const [autorecRecommendedAttractions, setAutorecRecommendedAttractions] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const pageSize = 5;
  const accessToken = localStorage.getItem('accessToken');
  const isLoggedIn = accessToken !== null;

  const fetchAttraction = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/attractions/${placeId}`);

      if (response.status !== 200) {
        throw new Error('Failed to fetch attraction');
      }

      setAttraction(response.data);
    } catch (error) {
      setError(error.response ? JSON.stringify(error.response.data.detail) : error.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchReviews = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/attractionReviews/place/${placeId}?page=${currentPage}&size=${pageSize}`);

      if (response.status !== 200) {
        throw new Error('Failed to fetch reviews');
      }

      setReviews(response.data.items);
      setTotalPages(response.data.pages);
    } catch (error) {
      setError(error.response ? JSON.stringify(error.response.data.detail) : error.message);
    } finally {
      setLoading(false);
    }
  };

  const postReview = async (reviewData) => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/attractionReviews', reviewData);

      if (response.status !== 200) {
        throw new Error('Failed to post review');
      }

      return response.data;
    } catch (error) {
      setError(error.response ? JSON.stringify(error.response.data.detail) : error.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchRecommendedAttractions = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/attractions/${placeId}/recommended`);
      
      if (response.status !== 200) {
        throw new Error('Failed to fetch recommended attractions');
      }
      
      setRecommendedAttractions(response.data);
    } catch (error) {
      setError(error.response ? JSON.stringify(error.response.data.detail) : error.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchAutorecRecommendedAttractions = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://localhost:8000/attractions/by_autorec/?user_name=${userName}`);

      if (response.status !== 200) {
        throw new Error('Failed to fetch autorec recommended attractions');
      }

      setAutorecRecommendedAttractions(response.data);
    } catch (error) {
      setError(error.response ? JSON.stringify(error.response.data.detail) : error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAttraction();
    fetchReviews();
    if (isLoggedIn) {
      fetchRecommendedAttractions();
      fetchAutorecRecommendedAttractions();
    }
  }, [placeId, currentPage, isLoggedIn]);

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const handleReviewSubmit = (e) => {
    e.preventDefault();

    if (userId && rating > 0 && reviewText) {
      const reviewData = {
        user_id: userId,
        place_id: placeId,
        user_rating: rating,
        content: reviewText
      };

      try {
        postReview(reviewData);
        window.location.reload();
      } catch (error) {
        setError(error.response ? JSON.stringify(error.response.data.detail) : error.message);
      }
    } else {
      alert('Enter rating and review content.');
    }
  };

  return (
    <div className="tourist-spot-detail">
        {loading && <p>Loading...</p>}
        {error && <p>{error}</p>}
        {attraction && (
            <div key={attraction.place_id}>
                <h2>{attraction.place_name}</h2>
                <img src={attraction.cover_image_url} alt={attraction.place_name} width="200" height="150" />
                <table>
                  <tr>
                    <td width="20%" align="right"><b>Description:</b></td>
                    <td align="left" style={{fontSize: '14px'}}>{attraction.description}</td>
                  </tr>
                  <tr>
                    <td width="20%" align="right"><b>Address:</b></td>
                    <td align="left" style={{fontSize: '14px'}}>{attraction.address}</td>
                  </tr>
                  <tr>
                    <td width="20%" align="right"><b>Score:</b></td>
                    <td align="left" style={{fontSize: '14px'}}>{attraction.comm_score} / 5</td>
                  </tr>
                </table>
            </div>
        )}

        <h2>Reviews</h2>
        <div className="review-list">
            {reviews.length > 0 ? (
                reviews.map((review, index) => (
                  <div key={index} className="review-item">
                      <b>{review.user_name} <span className="rating">({review.user_rating}/5)</span></b>
                      <p>{review.content}</p>
                  </div>
                ))
            ) : (
                <p>There are no reviews.</p>
            )}
        </div>
        <div className="pagination">
            <button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>Previous</button>
            <span>{currentPage} / {totalPages}</span>
            <button onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>Next</button>
        </div>

        {isLoggedIn && (
            <div>
              <div className="write-review-form">
                <div>
                <h2>Write a Review</h2>
                <form name="reviewForm" className="review-form" onSubmit={handleReviewSubmit}>
                    <input type="hidden" name="user_id" value={userId} />
                    <input type="hidden" name="place_id" value={placeId} />
                    <select name="user_rating" value={rating} onChange={(e) => setRating(Number(e.target.value))} required>
                        <option value="">Select</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                    </select>
                    <textarea
                        name="content"
                        placeholder="Write a review..."
                        value={reviewText}
                        onChange={(e) => setReviewText(e.target.value)}
                        required
                    />
                    <button type="submit">Submit</button>
                </form>
              </div>
            </div>
            <div className="recommended-attraction-container">
              <span></span>
                <div className="recommended-attraction-header">
                  <h2>Similar Attractions</h2>
              </div>
              <div className="recommended-attraction">
                {recommendedAttractions.length > 0 ? (
                    recommendedAttractions.map((attraction, index) => (
                        <Link to={`/tourist-spot/${attraction.place_id}`} key={attraction.place_id} style={{textDecoration: 'none'}}>
                          <div className="recommended-attraction-item">
                            <img src={attraction.cover_image_url} alt={attraction.place_name} width="150" height="100" />
                            <h4 style={{fontSize: '12px'}}>{attraction.place_name}</h4>
                          </div>
                        </Link>
                    ))
                ) : (
                    <p>There are no similar attractions.</p>
                )}
              </div>
            </div>
            <p>--------------------------------</p>
            <div className="recommended-attraction-container">
              <span></span>
              <div className="recommended-attraction-header">
                  <h2>Recommended Attractions</h2>
              </div>
              <div className="recommended-attraction">
                {autorecRecommendedAttractions.length > 0 ? (
                    autorecRecommendedAttractions.map((attraction, index) => (
                        <Link to={`/tourist-spot/${attraction.place_id}`} key={attraction.place_id} style={{textDecoration: 'none'}}>
                          <div className="recommended-attraction-item">
                            <img src={attraction.cover_image_url} alt={attraction.place_name} width="150" height="100" />
                            <h4 style={{fontSize: '12px'}}>{attraction.place_name}</h4>
                          </div>
                        </Link>
                    ))
                ) : (
                    <p>There are no similar attractions.</p>
                )}
              </div>
            </div>
          </div>
        )}
    </div>
  );
};

export default TouristSpotDetail;
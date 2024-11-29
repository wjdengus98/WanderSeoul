import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Signup.css'; // CSS 파일을 임포트합니다.
import logoImage from './images/projectlogo.png';

export default function Signup({ setIsLoggedIn }) {
  const [email, setEmail] = useState('');
  const [pw, setPw] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [agree, setAgree] = useState(false);
  const [emailValid, setEmailValid] = useState(false);
  const [pwValid, setPwValid] = useState(false);
  const [notAllow, setNotAllow] = useState(true);
  const navigate = useNavigate();

  const handleEmail = (e) => {
    setEmail(e.target.value);
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    setEmailValid(regex.test(e.target.value));
  };

  const handlePassword = (e) => {
    setPw(e.target.value);
    const regex = /^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+]).{8,20}$/;
    setPwValid(regex.test(e.target.value));
  };

  const handleFirstName = (e) => setFirstName(e.target.value);
  const handleLastName = (e) => setLastName(e.target.value);
  const handleAgree = (e) => setAgree(e.target.checked);

  useEffect(() => {
    setNotAllow(!(emailValid && pwValid && firstName && lastName && agree));
  }, [emailValid, pwValid, firstName, lastName, agree]);

  const handleSubmit = async () => {
    const userData = {
      user_name: email,
      password: pw,
      first_name: firstName,
      last_name: lastName,
      email: email
    };

    try {
      const response = await axios.post('http://localhost:8000/users', userData);
      if (response.status === 200) {
        alert('Your membership registration has been completed.');
        // setIsLoggedIn(true);
        navigate('/login'); // 로그인 페이지로 리다이렉트
      }
    } catch (error) {
      console.error('Error signing up:', error);
      alert('Signing up failed. Please try again.');
    }
  };

  return (
    <div className="signup-page">
      <img src={logoImage} alt='로고' className='logo' />
      <h1>Create an account</h1>
      <div className="inputWrap">
        <input
          type="text"
          placeholder="Email address*"
          value={email}
          onChange={handleEmail}
        />
        <div>
          {!emailValid && email.length > 0 && <div className='error-message'>Enter a valid email address.</div>}
        </div>
        <input
          type="password"
          placeholder="Password*"
          value={pw}
          onChange={handlePassword}
        />
        <div>
          {!pwValid && pw.length > 0 && <div className='error-message'>Enter a valid password.</div>}
        </div>
        <input
          type="text"
          placeholder="Name*"
          value={firstName}
          onChange={handleFirstName}
        />
        <input
          type="text"
          placeholder="Last name*"
          value={lastName}
          onChange={handleLastName}
        />
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            checked={agree}
            onChange={handleAgree}
          />
          I agree to receive emails
        </label>
      </div>
      <button
        onClick={handleSubmit}
        disabled={notAllow}
        className="signup-button"
      >
        Sign Up
      </button>
    </div>
  );
}
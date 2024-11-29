import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import logoImage from './images/projectlogo.png';
import './Login.css';

export default function Login({ onLoginSuccess }) {
  const [email, setEmail] = useState('');
  const [pw, setPw] = useState('');
  const [emailValid, setEmailValid] = useState(false);
  const [pwValid, setPwValid] = useState(false);
  const [notAllow, setNotAllow] = useState(true);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const handleEmail = (e) => {
    setEmail(e.target.value);
    const regex =
      /^(([^<>()\[\].,;:\s@"]+(\.[^<>()\[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/i;
    setEmailValid(regex.test(e.target.value));
  };
  
  const handlePassword = (e) => {
    setPw(e.target.value);
    const regex =
      /^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[$`~!@$!%*#^?&\\(\\)\-_=+])(?!.*[^a-zA-z0-9$`~!@$!%*#^?&\\(\\)\-_=+]).{8,20}$/;
    setPwValid(regex.test(e.target.value));
  };

  const onClickConfirmButton = async () => {
    const loginInfo = {
      user_name: email,
      password: pw
    };

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/auth/login', loginInfo);
      const accessToken = response.data.access_token;
      const userId = response.data.user_id;
      const userName = response.data.user_name;

      if (response.status === 200 && accessToken) {
        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('userId', userId);
        localStorage.setItem('userName', userName);
        onLoginSuccess(accessToken); // 로그인 성공 시 상태 변경
        // alert('로그인에 성공했습니다');
        navigate('/'); // 로그인 성공 후 메인 페이지로 리다이렉트
      } else {
        alert('You are not a registered member.');
        // navigate('/signup'); // 회원가입 페이지로 리다이렉트
      }
    } catch (error) {
      console.error('Error during login:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!notAllow) {
      onClickConfirmButton();
    }
  };

  useEffect(() => {
    setNotAllow(!(emailValid && pwValid));
  }, [emailValid, pwValid]);

  return (
    <div className="login-page">
      <img src={logoImage} alt='로고' className='logo' />
      <div className="titleWrap">Enter your email and password</div>
      <form onSubmit={handleSubmit}>
        <div className="contentWrap">
          <div className="inputTitle">Email</div>
          <div className="inputWrap">
            <input
              type="text"
              className="input"
              placeholder="UserID@gmail.com"
              value={email}
              onChange={handleEmail}
              style={{ fontSize: '14px' }}
            />
          </div>
          <div className="errorMessageWrap">
            {!emailValid && email.length > 0 && <div>Please enter a valid email address.</div>}
          </div>
          <div style={{ marginTop: '26px' }} className="inputTitle">
            PassWord
          </div>
          <div className="inputWrap">
            <input
              type="password"
              className="input"
              placeholder="8 more(English, numbers, and special characters)"
              value={pw}
              onChange={handlePassword}
            />
          </div>
          <div className="errorMessageWrap">
            {!pwValid && pw.length > 0 && <div>Please enter the correct password</div>}
          </div>
        </div>
        <div>
          <button onClick={onClickConfirmButton} disabled={notAllow} className="bottomButton">
            Confirm
          </button>
        </div>
      </form>
      <div className="link-section" style={{ marginTop: '20px' }}>
        <Link to="/signup">Signup</Link> {/* 회원가입 페이지로 이동하는 링크 */}
      </div>
    </div>
  );
}
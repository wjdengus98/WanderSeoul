import React from 'react';
import { useNavigate } from 'react-router-dom'; // useHistory 훅 추가
import './Navbar.css';
import headerImage from './images/seoul-twilight.jpg'; // 이미지 경로

const Navbar = () => {
    const history = useNavigate(); // history 객체 생성
    const handleLoginClick = () => {
        history.push('/login'); // 로그인 페이지로 이동
    };
    const handleSignupClick = () => {
        history.push('/signup'); // 회원가입 페이지로 이동
    };
    return (
        <div className="navbar">
            <img src={headerImage} alt="Header" className="header-image" />
            {/* <div className="nav-buttons">
            </div> */}
        </div>
    );
};

export default Navbar;

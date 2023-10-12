import React from "react";
import { removeToken } from "../../utilities/tokenService";
import { useNavigate } from "react-router-dom";

const Logout = () => {
    const navigate = useNavigate();
    const handleLogoutClick = () => {
        removeToken();
        navigate("/");
    };
    return (
        <button className="ml-4 mb-6 hover:text-amber-400 text-white" onClick={handleLogoutClick}>
            <h1 className="text-l font-bold">Log out</h1>
        </button>
    );
};

export default Logout;
// 
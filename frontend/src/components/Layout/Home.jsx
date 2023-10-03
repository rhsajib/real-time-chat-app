import React from "react";
import "./Home.css";
import Sidebar from "../Sidebar/Sidebar";
import Chat from "../Chats/Chats";
import { Outlet } from "react-router-dom";

const Home = () => {
    return (
        <div className="lg:flex">
            <div className="">
                <Sidebar />
            </div>
            <Outlet />
        </div>
    );
};

export default Home;

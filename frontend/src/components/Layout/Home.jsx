import React from "react";
import "./Home.css";
import Sidebar from "../Sidebar/Sidebar";
import { Outlet, useLoaderData } from "react-router-dom";

const Home = () => {
    // console.log(user)
    // const {username} = user
    return (
        <div className="lg:flex lg:flex-row h-screen bg-gray-200">
            <div className="lg:w-1/6">
                <Sidebar />
            </div>
            <div className="w-full border-r">
                <Outlet />
            </div>
        </div>
    );
};

export default Home;

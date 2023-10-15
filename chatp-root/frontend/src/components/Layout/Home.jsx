import React from "react";
import "./Home.css";
import Sidebar from "../Sidebar/Sidebar";
import { Outlet, useLoaderData } from "react-router-dom";

const Home = () => {
    const profile = useLoaderData();
    // console.log(profile);
    const { username, id } = profile;
    return (
        <div className="lg:flex lg:flex-row h-screen bg-gray-200">
            <div className="lg:w-1/6">
                <Sidebar username={username}/>
            </div>
            <div className="w-full">
                <Outlet />
            </div>
        </div>
    );
};

export default Home;

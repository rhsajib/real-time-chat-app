import React from "react";
import { Outlet, useLoaderData } from "react-router-dom";
import Users from "../Users/Users";

const Chats = () => {
    const users = useLoaderData();
    // console.log(users)
    return (
        <div className="lg:flex">
            <div className="w-[300px] border h-screen overflow-y-auto px-2 pt-4">
                <input
                    className="placeholder:italic placeholder:text-slate-400 block bg-white w-full border border-slate-300 rounded-md py-2 px-4 shadow-sm focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1 sm:text-sm"
                    placeholder="Chat with..."
                    type="text"
                    name="search"
                />
                <Users key={1} users={users} />
            </div>
            <div className="">
                <Outlet />
            </div>
        </div>
    );
};

export default Chats;

import React from "react";
import { Outlet, useLoaderData } from "react-router-dom";
import Users from "../Users/Users";
import ChatSearch from "../ChatSearch/ChatSearch";

const Chats = () => {
    const users = useLoaderData();
    // console.log(users)
    return (
        <div className="flex flex-row h-screen">
            <div className="flex flex-col w-1/3 border">
                <div className="sticky top-0 mx-3">
                    <ChatSearch />
                </div>
                <div className="flex flex-col overflow-y-auto">
                    <Users key={1} users={users} />
                </div>
            </div>
            <div className="w-full">
                <div>
                    <Outlet />
                </div>
            </div>
        </div>
    );
};

export default Chats;

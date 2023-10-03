import React from "react";
import { Link } from "react-router-dom";

const User = ({ user }) => {
    // console.log(user);
    const { username, email, id } = user;
    return (
        <Link to={`/chats/private/${id}`}>
            <div
                className="flex flex-col h-20 w-full justify-center px-4 mt-3 bg-stone-200 rounded-md"
            >
                <h4 className="text-2xl">{username}</h4>
                <span className="text-xs">{email}</span>
            </div>
        </Link>
    );
};

export default User;

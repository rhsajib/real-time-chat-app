import React from "react";
import ActiveLink from "../ActiveLink/ActiveLink";

const User = ({ user }) => {
    // console.log(user);
    const { username, email, id } = user;
    return (
        <div className="flex flex-col justify-center my-1 h-20 w-full">
            {/* <div className="flex flex-col my-2 h-20 w-full justify-center bg-slate-100 border border-blue-500 rounded-md"> */}
            <ActiveLink to={`/cp/users/profile/${id}`}>
                <div className="flex flex-row items-center h-[60px]">
                    <h4 className="text-2xl">{username}</h4>
                    {/* <span className="text-xs">{email}</span> */}
                </div>
            </ActiveLink>
            {/* <ActiveLink to={`/chats/private/${id}`}>
                <div>
                    <h4 className="text-2xl">{username}</h4>
                    <span className="text-xs">{email}</span>
                </div>
            </ActiveLink> */}
        </div>
    );
};

export default User;

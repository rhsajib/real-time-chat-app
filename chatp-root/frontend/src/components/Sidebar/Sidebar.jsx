import React from "react";
import { Link } from "react-router-dom";
import Logout from "../Logout/Logout";

const Sidebar = ({ username }) => {
    return (
        // <div className="flex flex-row lg:flex-col w-full lg:w-[150px] justify-between bg-gray-800 lg:h-screen lg:top-0 lg:left-0">
        <div className="flex flex-row lg:flex-col text-white justify-between bg-cyan-900 lg:overflow-y-auto lg:h-screen lg:top-0 lg:left-0 p-2">
            <div className="p-4 items-center">
                <h1 className="text-2xl font-bold">ChatP</h1>
            </div>

            <div className="p-4">
                <h1 className="text-xl font-bold">{username}</h1>
                <h1 className="text-sm font-bold">Profile Photo</h1>
            </div>

            {/* Menu Items */}
            <div className="lg:ml-4 flex items-center lg:items-start ">
                <ul className="flex lg:flex-col lg:items-start ">
                    <li className="mr-2 lg:my-2">
                        <Link to="/cp/chat" className="hover:text-amber-400">
                            Chats
                        </Link>
                    </li>
                    <li className="mr-2 lg:my-2">
                        <Link to="/cp/me" className="hover:text-amber-400">
                            Profile
                        </Link>
                    </li>
                    <li className="mr-2 lg:my-2">
                        <Link to="/cp/groups" className="hover:text-amber-400">
                            Groups
                        </Link>
                    </li>
                    <li className="mr-2 lg:my-2">
                        <Link to="/cp/users" className="hover:text-amber-400">
                            Users
                        </Link>
                    </li>
                    <li className="mr-2 lg:my-2">
                        <Link
                            to="/cp/settings"
                            className="hover:text-amber-400"
                        >
                            Settings
                        </Link>
                    </li>
                </ul>
            </div>

            <div>
                <Logout />
            </div>
        </div>
    );
};

export default Sidebar;

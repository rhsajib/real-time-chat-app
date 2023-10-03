import React from "react";
import { Link } from "react-router-dom";

const Sidebar = () => {
    return (
        <div className="flex flex-row lg:flex-col w-full lg:w-[150px] justify-between bg-gray-800 lg:h-screen lg:top-0 lg:left-0">
            <div className="p-4 text-white flex items-center text-center">
                <h1 className="text-2xl font-bold">Chat</h1>
            </div>

            {/* Menu Items */}
            <div className="lg:ml-4 flex items-center lg:items-start ">
                <ul className="flex lg:flex-col lg:items-start ">
                    <li className="mr-2 lg:my-2">
                        <Link to="/chats" className="text-white hover:text-blue-500">
                            Chats
                        </Link>
                    </li>
                    <li className="mr-2 lg:my-2">
                        <Link to="/profile" className="text-white hover:text-blue-500">
                            Profile
                        </Link>
                    </li>
                    <li className="mr-2 lg:my-2">
                        <Link to="/groups" className="text-white hover:text-blue-500">
                            Groups
                        </Link>
                    </li>
                    <li className="mr-2 lg:my-2">
                        <Link to="/contacts" className="text-white hover:text-blue-500">
                            Contacts
                        </Link>
                    </li>
                    <li className="mr-2 lg:my-2">
                        <Link to="/settings" className="text-white hover:text-blue-500">
                            Settings
                        </Link>
                    </li>
                </ul>
            </div>

            <div className="p-4 text-white flex items-center text-center">
                <h1 className="text-l font-bold">Profile Photo</h1>
            </div>
        </div>
    );
};

export default Sidebar;

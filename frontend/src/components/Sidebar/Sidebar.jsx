import React from "react";
import { Link } from "react-router-dom";

const Sidebar = () => {
    return (
        // <div className="flex flex-row lg:flex-col w-full lg:w-[150px] justify-between bg-gray-800 lg:h-screen lg:top-0 lg:left-0">
        <div className="flex flex-row lg:flex-col justify-between bg-gray-800 lg:h-screen lg:top-0 lg:left-0 p-2">
            <div className="p-4 text-white items-center">
                <h1 className="text-2xl font-bold">ChatP</h1>
            </div>

            {/* Menu Items */}
            <div className="lg:ml-4 flex items-center lg:items-start ">
                <ul className="flex lg:flex-col lg:items-start ">
                    <li className="mr-2 lg:my-2">
                        <Link to="/ChatP/chats" className="text-white hover:text-blue-500">
                            Chats
                        </Link>
                    </li>
                    <li className="mr-2 lg:my-2">
                        <Link to="/ChatP/myprofile" className="text-white hover:text-blue-500">
                            Profile
                        </Link>
                    </li>
                    <li className="mr-2 lg:my-2">
                        <Link to="/ChatP/groups" className="text-white hover:text-blue-500">
                            Groups
                        </Link>
                    </li>
                    <li className="mr-2 lg:my-2">
                        <Link to="/ChatP/users" className="text-white hover:text-blue-500">
                            Users
                        </Link>
                    </li>
                    <li className="mr-2 lg:my-2">
                        <Link to="/ChatP/settings" className="text-white hover:text-blue-500">
                            Settings
                        </Link>
                    </li>
                </ul>
            </div>


            <div className="p-4 text-white">
                <h1 className="text-l font-bold">Profile Photo</h1>
            </div>
        </div>
    );
};

export default Sidebar;

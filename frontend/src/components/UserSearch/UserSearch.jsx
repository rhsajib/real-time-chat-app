import React from "react";

const UserSearch = () => {
    return (
        <div>
            <input
                className="placeholder:italic placeholder:text-slate-400 block bg-white w-full border border-slate-300 rounded-md my-3 py-2 px-4 shadow-sm focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1 sm:text-sm"
                placeholder="Chat with or start..."
                type="text"
                name="search"
            />
        </div>
    );
};

export default UserSearch;
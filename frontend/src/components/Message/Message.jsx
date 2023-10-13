import React from "react";

const Message = ({ message }) => {
    return (
        <div className="py-1 px-2 my-1 mx-4 whitespace-pre-line bg-gray-200 rounded-md">
            {/* whitespace-pre-line is for daisplay lines with spaces and new line breaks */}
            <p className="">{message.message}</p>
            <div className="mt-3 flex flex-col">
                <p className="flex justify-end">
                    <small>{message.user_id}</small>
                </p>
                <p className="flex justify-end">
                    <small>{message.created_at}</small>
                </p>
            </div>
        </div>
    );
};

export default Message;

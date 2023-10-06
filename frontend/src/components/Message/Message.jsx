import React from "react";

const Message = ({ message }) => {
    return (
        <div className="p-2 my-2 mx-3 whitespace-pre-line bg-slate-300 rounded-md">
            {/* whitespace-pre-line is for daisplay lines with spaces and new line breaks */}
            <p className="mx-4">{message.message}</p>
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

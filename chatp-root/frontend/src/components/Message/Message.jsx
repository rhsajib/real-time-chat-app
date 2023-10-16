import React, { useEffect, useState } from "react";

const Message = ({ message, currentUserId }) => {
    let container, text;

    if (currentUserId === message.created_by) {
        // console.log("currentUserId", currentUserId, "created_by", message.created_by);
        container = "justify-end ";
        text = "text-left bg-emerald-300 ml-40 rounded-l-2xl rounded-tr-2xl";
    } else {
        container = "justify-start";
        text = "text-left bg-neutral-200 mr-40 rounded-r-2xl rounded-tl-2xl";
    }

    return (
        <div className={`flex ${container} mx-4 mb-2`}>
            {/* whitespace-pre-line is for daisplay lines with spaces and new line breaks */}
            <div
                className={`py-2 px-4 ${text} whitespace-pre-line`}
            >
                <p className="">{message.message}</p>
                {/* <div className="mt-3 flex flex-col ">
                    <p><small>{message.created_at}</small></p>
                </div> */}
            </div>
        </div>
    );
};

export default Message;

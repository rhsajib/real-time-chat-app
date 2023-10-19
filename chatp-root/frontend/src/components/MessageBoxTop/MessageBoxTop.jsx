import React, { useEffect, useState } from "react";

const MessageBoxTop = ({ recipientData, handleRecipientProfileClick }) => {
    return (
        <div className="bg-teal-900 h-15 px-4 py-4 border border-b-slate-200 text-white text-right sticky top-0">
            <button
                type="text"
                
                onClick={handleRecipientProfileClick}
            >
                <div className="w-[32px] h-[32px] rounded-full bg-blue-500 text-white text-center flex items-center justify-center font-bold text-xl">
                    {recipientData.username[0]}
                </div>
                {/* <h>{recipientData.username}</h> */}
            </button>
        </div>
    );
};

export default MessageBoxTop;

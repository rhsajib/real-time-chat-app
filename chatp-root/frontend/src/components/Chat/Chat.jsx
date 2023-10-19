import React, { useEffect, useState } from "react";
import ActiveLink from "../ActiveLink/ActiveLink";
import { userProfileLoader } from "../../utilities/apiLoaders";

const Chat = ({ chat }) => {
    const { recipient_id, chat_id } = chat;
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        const loadUserProfile = async () => {
            try {
                const response = await userProfileLoader(recipient_id);
                const data = await response.json();
                console.log("Parsed JSON data:", data);
                setUserData(data);
            } catch (error) {
                console.error("Error profile loading:", error);
            }
        };

        loadUserProfile();
    }, [recipient_id]);

    return (
        <div className="flex flex-col justify-center mb-1 w-full">
            {/* <div className="flex flex-col my-2 h-20 w-full justify-center bg-slate-100 border border-blue-500 rounded-md"> */}

            {userData ? (
                <ActiveLink to={`/cp/chat/private/${chat_id}`}>
                    <div className="flex flex-row items-center h-[60px]">
                        <div className="w-[40px] h-[40px] rounded-full bg-blue-500 text-white text-center flex items-center justify-center font-bold text-xl">
                            {userData.username[0]}
                        </div>
                        <p className="text-xl ml-4">{userData.username}</p>
                    </div>
                </ActiveLink>
            ) : (
                <p className="text-xl">Loading...</p>
                // <p></p>
            )}
        </div>
    );
};

export default Chat;

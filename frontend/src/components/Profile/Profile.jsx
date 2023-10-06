import React, { useEffect, useState } from "react";
import { Link, useLoaderData, useNavigate } from "react-router-dom";
import { chatIdLoader, newChatIdLoader } from "../../loaders/apiLoaders";

const Profile = () => {
    const profile = useLoaderData();
    // console.log(profile);
    const { first_name, last_name, email, username, phone, active, id } =
        profile;

    // handle Continue Chat
    // we should use useEffect as chatId is related to asynchronous operation.
    // otherwise it will raise promise error.
    const [chatId, setChatId] = useState(null); // State to store the chat ID
    useEffect(() => {
        const fetchChatId = async () => {
            const chatIdValue = await chatIdLoader(id);
            setChatId(chatIdValue);
        };
        fetchChatId();
    }, [id]);

    // handle Start New Chat
    const navigate = useNavigate(); // Get the navigate function for programmatic navigation
    const handleStartNewChatClick = async () => {
        const newChatIdValue = await newChatIdLoader(id);

        // After setting the state, navigate to the new chat
        navigate(`/chats/private/${newChatIdValue}`);
    };

    return (
        <div className="flex justify-center items-center h-screen">
            <div className="grow ml-12">
                <ul>
                    <li>User Name: {username}</li>
                    <li>First Name: {first_name}</li>
                    <li>Last Name: {last_name}</li>
                    <li>Email: {email}</li>
                    <li>Phone: {phone}</li>
                    <li>Status: {active ? "Active" : "Not Active"}</li>
                </ul>
            </div>
            <div className="w-40 mr-12 text-center">
                {chatId ? (
                    <Link to={`/chats/private/${chatId}`}>
                        <div className="border bg-sky-700 text-white py-3 rounded-xl">
                            Continue Chat
                        </div>
                    </Link>
                ) : (
                    <Link>
                        <div
                            className="border bg-yellow-800 text-white py-3 rounded-xl"
                            onClick={handleStartNewChatClick}
                        >
                            Start New Chat
                        </div>
                    </Link>
                )}
            </div>
        </div>
    );
};

export default Profile;

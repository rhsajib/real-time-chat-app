import React, { useState } from "react";
import Message from "../Message/Message";
import { useLoaderData } from "react-router-dom";

const Messages = () => {
    const chat = useLoaderData();
    // console.log(chat);
    const { chat_id, messages } = chat;

    const [previousMessages, setPreviousMessages] = useState(messages)

    const handleSendMesaage = (newMessage) => {
        const newMessages = [...previousMessages, newMessage]
        setPreviousMessages(newMessages)
    }

    return (
        <div className="flex flex-col mx-6 w-[800px] border h-screen">
            <div className="flex flex-col-reverse  h-screen overflow-y-auto">
                {messages.length !== 0 ? (
                    messages.map((message) => (
                        <Message key={message.id} message={message} />
                    ))
                ) : (
                    <div>
                        <h1>No messages</h1>
                    </div>
                )}
            </div>
            <div className="my-3 flex flex-row">
                <input
                    className="placeholder:italic placeholder:text-slate-400 block bg-white w-full border border-slate-300 rounded-md py-2 px-4 shadow-sm focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1"
                    placeholder="Write text..."
                    type="text"
                    name="newMessage"
                />
                <button className="bg-slate-400 rounded-lg ml-3 px-4" onClick={() => handleSendMesaage(newMessage)}>Send</button>
            </div>
        </div>
    );
};

export default Messages;

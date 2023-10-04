import React, { useEffect, useState } from "react";
import Message from "../Message/Message";
import { useLoaderData } from "react-router-dom";
import NoMessage from "../NoMessage/NoMessage";
import SendMessage from "../SendMessage/SendMessage";

const Messages = () => {
    // loades data from api
    const chatMessages = useLoaderData();

    // data destructure
    const { chat_id, messages } = chatMessages;

    // previous messages
    const [previousMessages, setPreviousMessages] = useState([]);
    useEffect(() => {
        setPreviousMessages(messages);
    }, [messages]);

    // handler to send message
    const handleSendMesaage = (message) => {
        // step 1: handle messages in client side
        const modelMessage = {
            user_id: "2123bb0ec29d4471bd295be4cca68aed",
            message: message,
            created_at: Date.now(),
        };
        // console.log(modelMessage);

        // React er state gula immutable. tai amra push pop use korte pari na
        // tai new array create kori
        const currentMessages = [...previousMessages, modelMessage];
        setPreviousMessages(currentMessages);

        // step : handle messages in server side
    };

    // console.log(previousMessages);

    return (
        // <div className="flex flex-col w-[800px] border h-screen">
        <div className="flex flex-col h-screen">
            <div className="flex-grow flex flex-col justify-end overflow-y-auto">
                <div className="">
                    {previousMessages.length !== 0 ? (
                        previousMessages.map((message, index) => (
                            <Message key={index} message={message} />
                        ))
                    ) : (
                        <NoMessage />
                    )}
                </div>
            </div>

            <div className="bg-white border-t-2 sticky bottom-0">
                <SendMessage
                    // messageInput={messageInput}
                    handleSendMesaage={handleSendMesaage}
                />
            </div>
        </div>
    );
};

export default Messages;

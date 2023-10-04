import React, { useEffect, useState } from "react";
import Message from "../Message/Message";
import { useLoaderData } from "react-router-dom";
import NoMessage from "../NoMessage/NoMessage";
import SendMessage from "../SendMessage/SendMessage";
import axios from "axios";

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
    const handleSendMesaage = async (message) => {
        // step 1: handle messages in server side
        // Send a POST request to your API endpoint
        const apiUrl = `http://127.0.0.1:8000/api/v1/chat/private/message/create/${chat_id}`;
        const data = {
            message: message,
        };

        const response = await axios
            .post(apiUrl, data, {
                headers: {
                    "Content-Type": "application/json", // Set the content type to JSON
                },
            })
            .then((response) => {
                // Handle the response as needed
                console.log("Message sent successfully:", response.data);

                // step 2: handle messages in client side
                // React er state gula immutable. tai amra push pop use korte pari na
                // tai new array create kori
                const createdMessage = response.data;
                const currentMessages = [...previousMessages, createdMessage];
                setPreviousMessages(currentMessages);
                // Update the state with the new message
                // setPreviousMessages((previousMessages) => [
                //     ...previousMessages,
                //     response.data,
                // ]);
            })
            .catch((error) => {
                // Handle any errors that occur during the POST request
                console.error("Error sending message:", error);
                setResponseMessage("Error sending message");
            });
    };

    // console.log(previousMessages);

    return (
        // <div className="flex flex-col w-[800px] border h-screen">
        <div className="grid grid-cols-1 content-end h-screen">
            <div className="overflow-y-auto">
                <div className="flex flex-col justify-end ">
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

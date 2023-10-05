import React, { useEffect, useState, useRef } from "react";
import Message from "../Message/Message";
import { useLoaderData } from "react-router-dom";
import NoMessage from "../NoMessage/NoMessage";
import SendMessage from "../SendMessage/SendMessage";
import axios from "axios";

const Messages = () => {
    // Load data from API
    const chatMessages = useLoaderData();

    // Data destructuring
    const { chat_id, messages } = chatMessages;

    // Reference for the chat container
    const chatContainerRef = useRef(null);

    // Previous messages
    const [previousMessages, setPreviousMessages] = useState([]);
    useEffect(() => {
        setPreviousMessages(messages);
    }, [messages]);

    // Handler to send a message
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

                // or
                // setPreviousMessages((previousMessages) => [
                //     ...previousMessages,
                //     createdMessage,
                // ]);

                // Scroll to the bottom after adding a new message
                // scrollToBottom();
            })
            .catch((error) => {
                // Handle any errors that occur during the POST request
                console.error("Error sending message:", error);
                setResponseMessage("Error sending message");
            });
    };

    // Function to scroll to the bottom
    const scrollToBottom = () => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop =
                chatContainerRef.current.scrollHeight;
        }
    };

    // Use useEffect to scroll to the bottom when the component mounts
    useEffect(() => {
        scrollToBottom();
    }, [previousMessages]);

    // console.log(previousMessages);

    return (
        // <div className="flex flex-col w-[800px] border h-screen">
        <div className="grid grid-cols-1 content-end h-screen">
            <div
                ref={chatContainerRef}
                className="flex flex-col h-full overflow-y-auto"
            >
                {" "}
                {/* max-h-80vh for 80% of view height*/}
                {previousMessages.length !== 0 ? (
                    previousMessages.map((message, index) => (
                        <Message key={index} message={message} />
                    ))
                ) : (
                    <NoMessage />
                )}
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

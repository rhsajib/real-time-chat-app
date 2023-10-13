import React, { useEffect, useState, useRef } from "react";
import Message from "../Message/Message";
import { useLoaderData } from "react-router-dom";
import NoMessage from "../NoMessage/NoMessage";
import SendMessage from "../SendMessage/SendMessage";
import { getToken } from "../../utilities/tokenService";

const Messages = () => {
    // Load data from API
    const chatMessages = useLoaderData();

    // Data destructuring
    const { chat_id, type, messages } = chatMessages;
    const token = getToken()

    // Reference for the chat container
    const messageContainerRef = useRef(null);

    // Previous messages from Api
    const [previousMessages, setPreviousMessages] = useState([]);
    useEffect(() => {
        setPreviousMessages(messages);
    }, [messages]);

    //--------------------------------------start handle SOCKET--------------------------------------------------
    // State to store the WebSocket instance
    const [socket, setSocket] = useState(null);
    useEffect(() => {
        // const url = `ws://127.0.0.1:8000/ws/chat/${chat_id}`;
        const url = `ws://127.0.0.1:8000/ws/chat/${type}/${chat_id}?token=${token}`

        // https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications
        // Create a WebSocket instance
        const newSocket = new WebSocket(url);

        newSocket.onopen = () => {
            console.log(`WebSocket connection established for ${chat_id}`);
        };

        newSocket.onmessage = (event) => {
            console.log(event);

            const parsedMessage = JSON.parse(event.data);
            console.log("Received Message:", parsedMessage);

            setPreviousMessages([...previousMessages, parsedMessage]);
        };

        newSocket.onclose = () => {
            console.log("WebSocket connection closed.");
        };

        setSocket(newSocket);

        return () => {
            // Clean up WebSocket when component unmounts
            console.log("WebSocket cleaned up.");
            newSocket.close();
        };
    }, [previousMessages]);

    // Handler to send a message
    const handleSendMesaage = (messageText) => {
        if (socket) {
            // https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications
            socket.send(messageText);
        }
    };

    //--------------------------------------end handle SOCKET--------------------------------------------------
    // Function to scroll to the bottom
    const scrollToBottom = () => {
        if (messageContainerRef.current) {
            messageContainerRef.current.scrollTop =
                messageContainerRef.current.scrollHeight;
        }
    };

    // Use useEffect to scroll to the bottom when the component mounts
    useEffect(() => {
        scrollToBottom();
    }, [previousMessages]);

    // console.log(previousMessages)
    // console.log(previousMessages);

    return (
        // <div className="flex flex-col w-[800px] border h-screen">
        <div className="grid grid-cols-1 content-end h-screen">
            <div
                ref={messageContainerRef}
                className="flex flex-col h-full overflow-y-auto"
            >
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

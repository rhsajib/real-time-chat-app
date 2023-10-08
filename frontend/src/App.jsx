import { useEffect, useState } from "react";
import "./App.css";

function App() {
    const [messages, setMessages] = useState([]);
    const [messageText, setMessageText] = useState("");
    const [socket, setSocket] = useState(null); // State to store the WebSocket instance

    const client_id = "a4sfdkj490";
    const url = `ws://127.0.0.1:8000/ws/chat/${client_id}`;

    useEffect(() => {
        // Create a WebSocket instance
        const newSocket = new WebSocket(url);

        newSocket.onopen = () => {
            console.log("WebSocket connection established.");
        };

        newSocket.onmessage = (event) => {
            // console.log("Message received:", event);
            setMessages([...messages, event.data]);
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
    }, [messages]);

    const handleFormSubmit = (e) => {
        e.preventDefault(); // Prevent the default form submission behavior

        if (socket) {
            socket.send(messageText);        // https://websockets.readthedocs.io/en/stable/intro/tutorial1.html
            setMessageText("");
        }
    };

    return (
        <div>
            <div className="text-3xl">Chat app</div>
            <form onSubmit={handleFormSubmit}>
                <input
                    className="border border-red-500"
                    placeholder="Write here..."
                    id="message"
                    type="text"
                    value={messageText}
                    onChange={(e) => setMessageText(e.target.value)}
                />
                <button type="text" className="m-3 border py-1 rounded-md px-4">
                    <span>Send</span>
                </button>
                <div>
                    <h1>Messages</h1>
                    {messages.map((message, idx) => (
                        <p key={idx}>{message}</p>
                    ))}
                </div>
            </form>
        </div>
    );
}

export default App;

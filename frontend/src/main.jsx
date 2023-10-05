import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import Home from "./components/Layout/Home";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Chats from "./components/Chats/Chats";
import Contacts from "./components/Contacts/Contacts";
import Profile from "./components/Profile/Profile";
import Groups from "./components/Groups/Groups";
import Messages from "./components/Messages/Messages";
import App from './App.jsx'

const router = createBrowserRouter([
    {
        path: "/",
        element: <Home />,
        children: [
            {
                path: "/chats",
                element: <Chats />,
                loader: () => fetch("http://127.0.0.1:8000/api/v1/user/all"),
                children: [
                    {
                        path: "/chats/private/:userId",
                        element: <Messages />,
                        loader: ({params}) => fetch(`http://127.0.0.1:8000/api/v1/chat/private/${params.userId}`)
                    },
                ],
            },
            {
                path: "/profile",
                element: <Profile />,
                // loader={}
            },
            {
                path: "/groups",
                element: <Groups />,
                // loader={}
            },
            {
                path: "/contacts",
                element: <Contacts />,
                // loader={}
            },
            {
                path: "/settings",
                element: <Contacts />,
                // loader={}
            },
        ],
    },
]);
ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        <RouterProvider router={router} />
        {/* <App /> */}
    </React.StrictMode>
);

import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import Home from "./components/Layout/Home";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Chats from "./components/Chats/Chats";
import Profile from "./components/Profile/Profile";
import Groups from "./components/Groups/Groups";
import Messages from "./components/Messages/Messages";
import App from "./App.jsx";
import {
    privateChatsLoader,
    usersLoader,
    userProfileLoader,
    messageLoader,
    myProfileLoader,
} from "./loaders/apiLoaders";
import Users from "./components/Users/Users";
import MyProfile from "./components/MyProfile/MyProfile";
import Settings from "./components/Settings/Settings";

const router = createBrowserRouter([
    {
        path: "/",
        element: <Home />,
        children: [
            {
                path: "/chats",
                element: <Chats />,
                loader: privateChatsLoader,
                children: [
                    {
                        path: "/chats/private/:chatId",
                        element: <Messages />,
                        loader: ({ params }) => messageLoader(params.chatId),
                    },
                ],
            },
            {
                path: "/myprofile",
                element: <MyProfile />,
                loader: myProfileLoader
            },
            {
                path: "/groups",
                element: <Groups />,
                // loader={}
            },
            {
                path: "/users",
                element: <Users />,
                loader: usersLoader,
                children: [
                    {
                        path: "/users/profile/:userId",
                        element: <Profile />,
                        loader: ({params}) => userProfileLoader(params.userId)
                    },
                    {
                        path: "/users/profile",
                        element: <Profile />,
                    },
                ],
            },
            {
                path: "/settings",
                element: <Settings />,
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

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
} from "./utilities/apiLoaders";
import Users from "./components/Users/Users";
import MyProfile from "./components/MyProfile/MyProfile";
import Settings from "./components/Settings/Settings";
import SignupLogin from "./components/SignupLogin/SignupLogin";

const router = createBrowserRouter([
    {
        path: "/",
        element: <SignupLogin />
    },
    {
        path: "/home",
        element: <Home />,
        children: [
            {
                path: "/home/chats",
                element: <Chats />,
                loader: privateChatsLoader,
                children: [
                    {
                        path: "/home/chats/private/:chatId",
                        element: <Messages />,
                        loader: ({ params }) => messageLoader(params.chatId),
                    },
                ],
            },
            {
                path: "/home/myprofile",
                element: <MyProfile />,
                loader: myProfileLoader
            },
            {
                path: "/home/groups",
                element: <Groups />,
                // loader={}
            },
            {
                path: "/home/users",
                element: <Users />,
                loader: usersLoader,
                children: [
                    {
                        path: "/home/users/profile/:userId",
                        element: <Profile />,
                        loader: ({params}) => userProfileLoader(params.userId)
                    },
                    {
                        path: "/home/users/profile",
                        element: <Profile />,
                    },
                ],
            },
            {
                path: "/home/settings",
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

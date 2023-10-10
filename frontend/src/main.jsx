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
        path: "/ChatP",
        element: <Home />,
        children: [
            {
                path: "/ChatP/chats",
                element: <Chats />,
                loader: privateChatsLoader,
                children: [
                    {
                        path: "/ChatP/chats/private/:chatId",
                        element: <Messages />,
                        loader: ({ params }) => messageLoader(params.chatId),
                    },
                ],
            },
            {
                path: "/ChatP/myprofile",
                element: <MyProfile />,
                loader: myProfileLoader
            },
            {
                path: "/ChatP/groups",
                element: <Groups />,
                // loader={}
            },
            {
                path: "/ChatP/users",
                element: <Users />,
                loader: usersLoader,
                children: [
                    {
                        path: "/ChatP/users/profile/:userId",
                        element: <Profile />,
                        loader: ({params}) => userProfileLoader(params.userId)
                    },
                    {
                        path: "/ChatP/users/profile",
                        element: <Profile />,
                    },
                ],
            },
            {
                path: "/ChatP/settings",
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

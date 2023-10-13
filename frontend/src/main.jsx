import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import Home from "./components/Layout/Home";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
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
import Auth from "./components/Auth/Auth";

const router = createBrowserRouter([
    {
        path: "/",
        element: <SignupLogin />,
    },
    {
        path: "/cp",
        element:(
            <Auth>
              <Home />
            </Auth>
          ),
        loader: myProfileLoader,
        children: [
            {
                path: "/cp/chat",
                element: <Chats />,
                loader: privateChatsLoader,
                children: [
                    {
                        path: "/cp/chat/private/:chatId",
                        element: <Messages />,
                        loader: ({ params }) => messageLoader(params.chatId),
                    },
                ],
            },
            {
                path: "/cp/me",
                element: <MyProfile />,
                loader: myProfileLoader,
            },
            {
                path: "/cp/groups",
                element: <Groups />,
                // loader={}
            },
            {
                path: "/cp/users",
                element: <Users />,
                loader: usersLoader,
                children: [
                    {
                        path: "/cp/users/profile/:userId",
                        element: <Profile />,
                        loader: ({ params }) =>
                            userProfileLoader(params.userId),
                    },
                    {
                        path: "/cp/users/profile",
                        element: <Profile />,
                    },
                ],
            },
            {
                path: "/cp/settings",
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

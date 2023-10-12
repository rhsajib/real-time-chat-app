// user -------------------------------------------------------------

import { addTokenToHeaders } from "./tokenService";

// Reusable function for making asynchronous API requests
// const fetchWithAuthHeaders = (url, headers) => {
const fetchWithAuthHeaders = (url, headers = {}) => {
    const updatedHeaders = addTokenToHeaders(headers);
    return fetch(url, { headers: updatedHeaders });
};

const usersLoader = () =>
    fetchWithAuthHeaders("http://127.0.0.1:8000/api/v1/user/all");

const userProfileLoader = (userId) =>
    fetchWithAuthHeaders(`http://127.0.0.1:8000/api/v1/user/info/${userId}`);

const myProfileLoader = (userId) =>
    fetchWithAuthHeaders("http://127.0.0.1:8000/api/v1/user/info/me");

const privateChatsLoader = () =>
    fetchWithAuthHeaders(
        "http://127.0.0.1:8000/api/v1/chat/private/msg-recipients/"
    );

// chat -------------------------------------------------------------

const chatsLoader = () =>
    fetchWithAuthHeaders("http://127.0.0.1:8000/api/v1/chat/private/all");

const messageLoader = (chatId) =>
    fetchWithAuthHeaders(
        `http://127.0.0.1:8000/api/v1/chat/private/info/${chatId}`
    );

const authUserLoader = async () => {
    try {
        const response = await fetchWithAuthHeaders(
            "http://127.0.0.1:8000/api/v1/chat/home"
        );
        // console.log(response)
        const user = await response.json();
        console.log("user", user);
        return user;
    } catch (error) {
        console.error("Error fetching auth user:", error);
        throw error; // You can handle the error as needed
    }
};

const chatIdLoader = async (userId) => {
    try {
        const response = await fetchWithAuthHeaders(
            `http://127.0.0.1:8000/api/v1/chat/private/recipient/get-chat/${userId}`
        );
        const data = await response.json();
        //   console.log(data.chat_id)
        return data.chat_id;
    } catch (error) {
        console.error("Error fetching chat ID:", error);
        throw error; // You can handle the error as needed
    }
};

const newChatIdLoader = async (userId) => {
    try {
        const response = await fetchWithAuthHeaders(
            `http://127.0.0.1:8000/api/v1/chat/private/recipient/create-chat/${userId}`
        );
        const data = await response.json();
        //   console.log(data.chat_id)
        return data.chat_id;
    } catch (error) {
        console.error("Error fetching chat ID:", error);
        throw error; // You can handle the error as needed
    }
};

export {
    authUserLoader,
    chatsLoader,
    messageLoader,
    privateChatsLoader,
    usersLoader,
    userProfileLoader,
    myProfileLoader,
    chatIdLoader,
    newChatIdLoader,
};

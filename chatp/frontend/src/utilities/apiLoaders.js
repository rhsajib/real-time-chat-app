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

// the following loaders are not directly being used in loader in react router
// thst's why these are async function

const authUserLoader = async () => {
    try {
        const response = await fetchWithAuthHeaders(
            "http://127.0.0.1:8000/api/v1/chat/home"
        );
        // console.log(response)
        const user = await response.json();
        console.log("auth user", user);
        return user;
    } catch (error) {
        console.error("Error fetching auth user:", error);
        throw error; // You can handle the error as needed
    }
};

const chatIdLoader = async (userId) => {
    /*
    // Make an HTTP POST request to create a new user
    fetch("http://127.0.0.1:8000/api/v1/user/create", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(userData), // Send user data to the server
    })
        .then((response) => {
            if (response.status === 422) {
                // Validation error, email already in use
                return response.json().then((errorResponse) => {
                    console.log("Validation Failed:", errorResponse);
                    // Handle the error response on the client side
                });
            }
            if (response.status === 200) {
                // User created successfully
                return response.json().then((userResponse) => {
                    console.log("User Created:", userResponse);
                    // Handle the successful user creation response
                });
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            // Handle other errors (e.g., network issues)
        });
    */

    try {
        const response = await fetchWithAuthHeaders(
            `http://127.0.0.1:8000/api/v1/chat/private/recipient/chat-id/${userId}`
        );

        console.log(response);

        if (response.status === 404) {
            return null;
        } else if (response.status === 200) {
            const data = await response.json();
            // console.log('data.chat_id', data.chat_id);
            return data.chat_id;
        }
    } catch (error) {
        console.error("Error fetching chat ID:", error);
        throw error; // You can handle the error as needed
    }
};
// const chatIdLoader = async (userId) => {
//     try {
//         const response = await fetchWithAuthHeaders(
//             `http://127.0.0.1:8000/api/v1/chat/private/recipient/chat-id/${userId}`
//         );
//         const data = await response.json();
//           console.log(data.chat_id)
//         return data.chat_id;
//     } catch (error) {
//         console.error("Error fetching chat ID:", error);
//         throw error; // You can handle the error as needed
//     }
// };

const newChatIdLoader = async (userId) => {
    console.log('newChatIdLoader', userId)
    try {
        const response = await fetchWithAuthHeaders(
            `http://127.0.0.1:8000/api/v1/chat/private/recipient/create-chat/${userId}`
        );
        const data = await response.json();
          console.log(data)
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

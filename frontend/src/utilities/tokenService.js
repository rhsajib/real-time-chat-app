import Cookies from "js-cookie";

const TOKEN_KEY = "chatp-access-token";

export const getToken = () => {
    return Cookies.get(TOKEN_KEY);
};

export const setToken = (token) => {
    Cookies.set(TOKEN_KEY, token, { expires: 7 }); // Adjust the expiration as needed
};

export const removeToken = () => {
    Cookies.remove(TOKEN_KEY);
};

// Define a function to add the access token to the headers
export const addTokenToHeaders = (headers) => {
    const token = getToken(); // Retrieve the access token
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }
    return headers;
}
import axios from "axios";
import { apiBaseUrl, apiVersion } from './configCore';

const apiBase = apiBaseUrl + apiVersion

const handleSignupData = async (data) => {
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

    // Make an HTTP POST request to create a new user
    // axios
    //     .post("http://127.0.0.1:8000/api/v1/user/create", data, {
    //         headers: {
    //             "Content-Type": "application/json",
    //         },
    //     })
    //     .then((response) => {
    //         console.log('response', response.data)
    //         if (response.status === 422) {
    //             // Validation error, email already in use
    //             console.log("Validation Failed:", response.data);
    //             // Handle the error response on the client side
    //         } else if (response.status === 201) {
    //             // User created successfully
    //             console.log("User Created:", response.data);
    //             // Handle the successful user creation response
    //         }
    //     })
    //     .catch((error) => {
    //         console.log('inside error')
    //         console.error("Error:", error);
    //         // Handle other errors (e.g., network issues)
    //     });

    try {
        // here, data = {username: 'sajib', email: 'rhsajib15@gmail.com', password1: '11', password2: '11'}
        // console.log(data);
        const apiUrl = `${apiBase}/user/create`;

        const response = await axios.post(apiUrl, data, {
            headers: {
                "Content-Type": "application/json", // Set the content type to JSON
            },
        });

        // Handle the response as needed
        console.log("Sign up completed successfully:", response);
        // console.log("Sign up completed successfully:", response.data["username"]);

        return response; // Return the response
    } catch (error) {
        // Handle any errors that occur during the POST request
        console.error("Error signing up:", error.response);
        throw error;
    }
};

const handleLoginData = async (data) => {
    try {
        // here, data = {email: 'rhsajib15@gmail.com', password: '11'}
        console.log(data);
        const apiUrl = `${apiBase}/auth/login/access-token`;

        const response = await axios.post(apiUrl, data, {
            headers: {
                "Content-Type": "application/json", // Set the content type to JSON
            },
        });

        // Handle the response as needed
        console.log("Login completed successfully:");
        console.log(response.data);
        return response; // Return the response
    } catch (error) {
        // Handle any errors that occur during the POST request
        console.error("Login Error:", error);
        throw error; // Rethrow the error
    }
};

export { handleSignupData, handleLoginData };

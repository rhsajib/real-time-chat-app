// import axios from "axios";

// const handleSignupData = async (data) => {
//     // here, data = {username: 'sajib', email: 'rhsajib15@gmail.com', password1: '11', password2: '11'}
//     console.log(data);
//     const apiUrl = "http://127.0.0.1:8000/api/v1/user/create";
//     // const userData = {
//     //     user: data
//     // }

//     const response = await axios
//         .post(apiUrl, data, {
//             headers: {
//                 "Content-Type": "application/json", // Set the content type to JSON
//             },
//         })
//         .then((response) => {
//             // Handle the response as needed
//             console.log(
//                 "Sign up completed successfully:",
//                 response.data["username"]
//             );
//             return response.data;
//         })
//         .catch((error) => {
//             // Handle any errors that occur during the POST request
//             console.error("Error sending message:", error);
//             setResponseMessage("Error sending message");
//         });
// };

// export { handleSignupData };

import axios from "axios";

const handleSignupData = async (data) => {
    try {
        // here, data = {username: 'sajib', email: 'rhsajib15@gmail.com', password1: '11', password2: '11'}
        // console.log(data);
        const apiUrl = "http://127.0.0.1:8000/api/v1/user/create";

        const response = await axios.post(apiUrl, data, {
            headers: {
                "Content-Type": "application/json", // Set the content type to JSON
            },
        });

        // Handle the response as needed
        console.log("Sign up completed successfully:", response.data);
        // console.log("Sign up completed successfully:", response.data["username"]);

        return response; // Return the response
    } catch (error) {
        // Handle any errors that occur during the POST request
        console.error("Error signing up:", error);
        throw error; // Rethrow the error
    }
};

const handleLoginData = async (data) => {
    try {
        // here, data = {email: 'rhsajib15@gmail.com', password: '11'}
        console.log(data);
        const apiUrl = "http://127.0.0.1:8000/api/v1/auth/login/access-token";

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
        console.error("Error Login:", error);
        throw error; // Rethrow the error
    }
};

export { handleSignupData, handleLoginData };

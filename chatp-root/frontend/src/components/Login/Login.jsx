import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import LoginInputFields from "../LoginInputFields/LoginInputFields";
import { handleLoginData } from "../../utilities/handlers";
import { getToken, setToken } from "../../utilities/tokenService";
import { useNavigate } from "react-router-dom";
import PasswordChange from "../PasswordChange/PasswordChange";

const Login = () => {
    const containerVariants = {
        initial: { opacity: 0, y: -20 },
        animate: { opacity: 1, y: 0, transition: { duration: 0.9 } },
    };

    const initiaFormData = {
        email: "",
        password: "",
    };

    const navigate = useNavigate(); // Initialize the navigate function
    const [errorMessage, setErrorMessage] = useState(null);
    const [formData, setFormData] = useState(initiaFormData);
    const [forgotPassword, setForgotPassword] = useState(false);

    useEffect(() => {
        // Check if the access token exists
        const accessToken = getToken(); // Implement your own function to retrieve the access token
        if (accessToken) {
            // If access token exists, navigate to the desired path
            navigate("/cp"); // Replace with the path you want to navigate to
        }
    }, []);

    const handleLoginSubmit = (e) => {
        e.preventDefault(); // Prevent the default form submission behavior

        handleLoginData(formData)
            // When we call handleLoginSubmit(formData) , it returns a promise (since handleLoginSubmit is an asynchronous function),
            // so we need to handle the promise using then to get the result.
            .then((response) => {
                // console.log(response.data);

                const { access_token } = response.data;

                // Store the access token in cookie (or state or local storage)
                setToken(access_token);
                setFormData(initiaFormData);
                // Navigate to the desired path after successful login
                navigate("/cp"); // Replace with the path you want to navigate to
            })
            .catch((error) => {
                console.error("Login failed", error);
                const response = error.response;
                const message = response.data.detail;
                // console.log(message);
                setErrorMessage(message);
            });
    };

    // Handle form input changes
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        // console.log(`${name}: ${value}`)
        setFormData({ ...formData, [name]: value });
        // console.log(formData);
    };

    const haldleForgotPassword = () => {
        setForgotPassword(true);
    };

    return (
        <motion.div
            className="min-h-screen flex items-center justify-center"
            initial="initial"
            animate="animate"
            variants={containerVariants}
        >
            {!forgotPassword ? (
                <LoginInputFields
                    handleLoginSubmit={handleLoginSubmit}
                    formData={formData} // Pass the formData to the child component
                    fieldError={errorMessage}
                    handleInputChange={handleInputChange} // Pass the handleInputChange function to the child component
                    haldleForgotPassword={haldleForgotPassword}
                />
            ) : (
                // <PasswordChange />
                <h1>Forgot password</h1>

            )}
        </motion.div>
    );
};

export default Login;

// import React from "react";

// const Login = () => {
//     return (
//         <div className="flex flex-row h-screen">
//             <div className="flex justify-center items-center h-full w-1/2 border-r mr-1">
//                 <h1>part1</h1>
//             </div>
//             <div className="flex justify-center items-center h-full w-1/2 border-l ml-1">
//                 <h1>part1</h1>
//             </div>
//         </div>
//     );
// };

// export default Login;

/* 

To achieve the functionality where the login form first checks if a username exists in the database and then displays the password field and login button accordingly, you'll need to integrate a backend server to handle this logic. Here's a high-level overview of the steps involved:

1. **Backend API**: Create a backend API using a server-side technology of your choice (e.g., Node.js with Express, Django, Ruby on Rails, etc.). This API should have endpoints for checking if a username exists in the database and for handling user authentication.

2. **Frontend Integration**: In your React frontend, make an asynchronous request to the backend API when the user enters their username/email and hits a "Check Availability" or similar button.

3. **Backend Logic**: In the backend, check if the username/email exists in the database. If it does, return a response indicating that the username exists. If not, return a response indicating that the username doesn't exist.

4. **Frontend Response Handling**: In your React frontend, based on the response from the backend, conditionally render the password field and login button.

Here's an example of how your code could look:

```jsx
import React, { useState } from 'react';
import { motion } from 'framer-motion';

const Login = () => {
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [isUsernameAvailable, setIsUsernameAvailable] = useState(false);

  const inputVariants = {
    rest: { scale: 1 },
    hover: { scale: 1.05 },
  };

  const checkUsernameAvailability = async () => {
    try {
      // Make an API request to check if the username exists in the database
      // You would replace this with your actual API endpoint and logic
      const response = await fetch('/api/check-username', {
        method: 'POST',
        body: JSON.stringify({ usernameOrEmail }),
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        setIsUsernameAvailable(true);
      } else {
        setIsUsernameAvailable(false);
      }
    } catch (error) {
      console.error('Error checking username availability:', error);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="max-w-md w-full p-6">
        <form>
          <div className="mb-4">
            <input
              className="w-full px-4 py-2 text-cyan-700 border rounded-xl focus:outline-none focus:border-cyan-700"
              type="text"
              id="usernameOrEmail"
              name="usernameOrEmail"
              placeholder="Enter your username or email"
              onChange={(e) => setUsernameOrEmail(e.target.value)}
            />
            <motion.button
              variants={inputVariants}
              whileHover="hover"
              whileTap="rest"
              onClick={checkUsernameAvailability}
              className="mt-2 bg-cyan-700 hover:bg-cyan-800 text-white font-bold py-2 rounded-md transition duration-300"
              type="button"
            >
              Check Availability
            </motion.button>
          </div>
          {isUsernameAvailable && (
            <>
              <div className="mb-6">
                <input
                  className="w-full px-4 py-2 text-cyan-700 border rounded-xl focus:outline-none focus:border-cyan-700"
                  type="password"
                  id="password"
                  name="password"
                  placeholder="Enter your password"
                />
              </div>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="w-full bg-cyan-700 hover:bg-cyan-800 text-white font-bold py-2 rounded-md transition duration-300"
                type="submit"
              >
                Login
              </motion.button>
            </>
          )}
        </form>
      </div>
    </div>
  );
};

export default Login;
```

In this code:

- We added a state variable `isUsernameAvailable` to keep track of whether the username exists in the database.
- When the user clicks the "Check Availability" button, we make an API request to your backend to check if the username exists. The response determines whether the password field and login button should be displayed.
- If `isUsernameAvailable` is `true`, the password field and login button will be rendered.

Please note that the actual backend API logic and routes (`/api/check-username`) should be implemented on your server.

*/

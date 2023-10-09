import React from 'react';
import { motion } from 'framer-motion';

const Login = () => {
  const inputVariants = {
    rest: { scale: 1 },
    hover: { scale: 1.05 },
  };

  const containerVariants = {
    initial: { opacity: 0, y: -20 },
    animate: { opacity: 1, y: 0, transition: { duration: 0.9 } },
  };

  return (
    <motion.div
      className="min-h-screen flex items-center justify-center"
      initial="initial"
      animate="animate"
      variants={containerVariants}
    >
      <div className="max-w-md w-full p-6">
        <form>
          <div className="mb-4">
            <motion.input
              variants={inputVariants}
              whileHover="hover"
              whileTap="rest"
              className="w-full px-4 py-2 text-cyan-700 border rounded-xl focus:outline-none focus:border-cyan-700"
              type="text"
              id="usernameOrEmail"
              name="usernameOrEmail"
              placeholder="Enter your username or email"
            />
          </div>
          <div className="mb-6">
            <motion.input
              variants={inputVariants}
              whileHover="hover"
              whileTap="rest"
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
            className="w-full bg-cyan-500 hover:bg-cyan-700 text-white font-bold py-2 rounded-xl transition duration-300"
            type="submit"
          >
            Login
          </motion.button>
        </form>
      </div>
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
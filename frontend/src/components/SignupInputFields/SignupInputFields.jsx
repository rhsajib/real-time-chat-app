import React, { useState } from "react";
import { motion } from "framer-motion";

const SignupInputFields = ({ handleSignup }) => {
    const inputVariants = {
        rest: { scale: 1 },
        hover: { scale: 1.05 },
    };

    const initiaFormData = {
        username: "",
        email: "",
        password1: "",
        password2: "",
    };

    // State to store form data
    const [formData, setFormData] = useState({});
    const [passwordsMatch, setPasswordsMatch] = useState(true);

    // Handle form input changes
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSignupSubmit = (e) => {
        e.preventDefault(); // Prevent the default form submission behavior
        //By default, when we submit a form,
        // it performs a full-page refresh and appends the form data
        // to the URL as query parameters.
        // Check if passwords match
        if (formData.password1 !== formData.password2) {
            setPasswordsMatch(false);
            return; // Prevent form submission if passwords do not match
        }

        // Reset the passwordsMatch state to true when they match
        setPasswordsMatch(true);

        // Perform the signup
        const completed = handleSignup(formData);

        if (completed) {
            // Reset form data
            setFormData(initiaFormData);
        }
    };
    return (
        <div className="max-w-md w-full p-6">
            <form onSubmit={handleSignupSubmit}>
                <div className="mb-4">
                    <motion.input
                        variants={inputVariants}
                        whileHover="hover"
                        whileTap="rest"
                        className="w-full px-4 py-2 text-cyan-700 border rounded-xl focus:outline-none focus:border-cyan-700"
                        type="text"
                        id="username"
                        name="username"
                        placeholder="Enter your username"
                        value={formData.username}
                        onChange={handleInputChange}
                    />
                </div>
                <div className="mb-4">
                    <motion.input
                        variants={inputVariants}
                        whileHover="hover"
                        whileTap="rest"
                        className="w-full px-4 py-2 text-cyan-700 border rounded-xl focus:outline-none focus:border-cyan-700"
                        type="email"
                        id="email"
                        name="email"
                        placeholder="Enter your email"
                        value={formData.email}
                        onChange={handleInputChange}
                    />
                </div>
                <div className="mb-6">
                    <motion.input
                        variants={inputVariants}
                        whileHover="hover"
                        whileTap="rest"
                        className="w-full px-4 py-2 text-cyan-700 border rounded-xl focus:outline-none focus:border-cyan-700"
                        type="password"
                        id="password1"
                        name="password1"
                        placeholder="Choose a password"
                        value={formData.password1}
                        onChange={handleInputChange}
                    />
                </div>
                <div className="mb-6">
                    <motion.input
                        variants={inputVariants}
                        whileHover="hover"
                        whileTap="rest"
                        className="w-full px-4 py-2 text-cyan-700 border rounded-xl focus:outline-none focus:border-cyan-700"
                        type="password"
                        id="password2"
                        name="password2"
                        placeholder="Enter password again"
                        autoComplete="off"
                        value={formData.password2}
                        onChange={handleInputChange}
                    />
                </div>
                {!passwordsMatch && (
                    <p className=" text-center mb-2 text-red-500">
                        Passwords do not match.
                    </p>
                )}
                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="w-full bg-cyan-500 hover:bg-cyan-700 text-white font-bold py-2 rounded-md transition duration-300"
                    type="submit"
                >
                    Sign Up
                </motion.button>
            </form>
        </div>
    );
};

export default SignupInputFields;

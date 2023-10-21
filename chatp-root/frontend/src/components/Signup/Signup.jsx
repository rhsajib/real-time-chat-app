import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import SignupInputFields from "../SignupInputFields/SignupInputFields";
import { handleSignupData } from "../../utilities/handlers";
import SignupComplete from "../SignupComplete/SignupComplete";

const Signup = () => {
    const containerVariants = {
        initial: { opacity: 0, y: -20 },
        animate: { opacity: 1, y: 0, transition: { duration: 0.9 } },
    };
    const initiaFormData = {
        username: "",
        email: "",
        password1: "",
        password2: "",
    };

    // State to store form data
    const [formData, setFormData] = useState(initiaFormData);
    const [passwordsMatch, setPasswordsMatch] = useState(true);
    const [passwordLengthError, setPasswordLengthError] = useState(false);
    const [errorMessage, setErrorMessage] = useState(null);
    const [userName, setUserName] = useState("");

    // Handle form input changes
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const resetForm = () => {
        setFormData(initialFormData);
    };

    const clearErrors = () => {
        console.log("Clearing errors...");
        setErrorMessage(null);
        setPasswordLengthError(false);
        setPasswordsMatch(true); // Reset the passwordsMatch state to true when they match
    };

    const handleSignupSubmit = async (e) => {
        e.preventDefault(); // Prevent the default form submission behavior
        //By default, when we submit a form,
        // it performs a full-page refresh and appends the form data
        // to the URL as query parameters.
        // Check if passwords match

        clearErrors();
        console.log("handleSignupSubmit");

        if (formData.password1.length < 6) {
            console.log("Password length is less than 6");
            setPasswordLengthError(true);
            return;
        }

        if (formData.password1 !== formData.password2) {
            setPasswordsMatch(false);
            return;
        }

        // handleSignupData(formData)
        // When we call handleSignupData(formData) , it returns a promise (since handleSignupData is an asynchronous function),
        // so we need to handle the promise using then to get the result.

        // process 1  (remove async from handleSignupSubmit)
        // .then((response) => {
        //     const newUserName = response.data["username"];
        //     setUserName(newUserName);
        //     // Reset the form data after successful signup
        //     resetForm();
        // })
        // .catch((error) => {
        //     console.error("Error signing up:", error);
        //     const response = error.response;
        //     const message = response.data.detail.errors[0].message;
        //     setErrorMessage(message);
        // });

        // process 2
        try {
            const response = await handleSignupData(formData);
            const newUserName = response.data.username;
            setUserName(newUserName);
            resetForm();
        } catch (error) {
            console.error("Error signing up:", error);
            const message =
                error.response?.data.detail.errors[0].message ||
                "An error occurred.";
            setErrorMessage(message);
        }
    };

    return (
        <motion.div
            className="min-h-screen flex items-center justify-center"
            initial="initial"
            animate="animate"
            variants={containerVariants}
        >
            {userName && userName.length !== 0 ? (
                <SignupComplete userName={userName} />
            ) : (
                <SignupInputFields
                    handleSignupSubmit={handleSignupSubmit}
                    formData={formData} // Pass the formData to the child component
                    handleInputChange={handleInputChange} // Pass the handleInputChange function to the child component
                    passwordsMatch={passwordsMatch}
                    passwordLengthError={passwordLengthError}
                    fieldError={errorMessage}
                />
            )}
        </motion.div>
    );
};

export default Signup;

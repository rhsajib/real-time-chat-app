import React, { useState } from "react";
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
    const [userName, setUserName] = useState("");

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

        handleSignupData(formData)
            // When we call handleSignupData(formData) , it returns a promise (since handleSignupData is an asynchronous function),
            // so we need to handle the promise using then to get the result.
            .then((response) => {
                const newUserName = response.data["username"];

                console.log(newUserName);
                setUserName(newUserName);

                // Reset the form data after successful signup
                setFormData(initiaFormData);
            })
            .catch((error) => {
                console.error("Error signing up:", error);
            });
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
                />
            )}
        </motion.div>
    );
};

export default Signup;

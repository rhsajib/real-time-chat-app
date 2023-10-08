import React, { useState } from "react";
import { motion } from "framer-motion";
import SignupInputFields from "../SignupInputFields/SignupInputFields";
import { handleSignupData } from "../../utilities/handlers";
import SignupComplete from "../SignupComplete/SignupComplete";

const Signup = () => {
    const [userName, serUserName] = useState("");

    const containerVariants = {
        initial: { opacity: 0, y: -20 },
        animate: { opacity: 1, y: 0, transition: { duration: 0.9 } },
    };

    // const handleSignup = (formData) => {
    //     const response = handleSignupData(formData)

    //     const newUserName = response.data['username']
    //     console.log(newUserName)
    //     serUserName(newUserName);
    // };
    const handleSignup = (formData) => {
        // When we call handleSignupData(formData) , it returns a promise (since handleSignupData is an asynchronous function),
        // so you need to handle the promise using then to get the result.
        handleSignupData(formData)
            .then((response) => {
                const newUserName = response.data["username"];
                console.log(newUserName);
                serUserName(newUserName);
            })
            .catch((error) => {
                console.error("Error signing up:", error);
            });
        return true
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
                <SignupInputFields handleSignup={handleSignup} />
            )}
        </motion.div>
    );
};

export default Signup;

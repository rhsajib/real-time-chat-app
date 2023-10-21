import React from "react";
import { motion } from "framer-motion";

const AccountActivatedPage = () => {
    const containerVariants = {
        initial: { opacity: 0, y: -20 },
        animate: { opacity: 1, y: 0 },
    };

    const textVariants = {
        initial: { opacity: 0, y: 20 },
        animate: { opacity: 1, y: 0, transition: { delay: 0.5, duration: 1 } },
    };

    return (
        <motion.div
            className="min-h-screen flex items-center justify-center"
            initial="initial"
            animate="animate"
            variants={containerVariants}
        >
            <motion.div
                className="text-xl text-cyan-800 font-semibold"
                variants={textVariants}
            >
                <p>Your account has been activated.</p>
                <p> Please Login.</p>
            </motion.div>
        </motion.div>
    );
};

export default AccountActivatedPage;

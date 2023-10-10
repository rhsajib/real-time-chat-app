import React from "react";
import { motion } from "framer-motion";

const LoginInputFields = ({handleLoginSubmit, formData, handleInputChange}) => {
    const inputVariants = {
        rest: { scale: 1 },
        hover: { scale: 1.05 },
    };

    return (
        <div className="max-w-md w-full p-6">
            <form onSubmit={handleLoginSubmit}>
                <div className="mb-4">
                    <motion.input
                        variants={inputVariants}
                        whileHover="hover"
                        whileTap="rest"
                        className="w-full px-4 py-2 text-cyan-700 border rounded-xl focus:outline-none focus:border-cyan-700"
                        type="text"
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
                        id="password"
                        name="password"
                        placeholder="Enter your password"
                        value={formData.password}
                        onChange={handleInputChange}
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
    );
};

export default LoginInputFields;

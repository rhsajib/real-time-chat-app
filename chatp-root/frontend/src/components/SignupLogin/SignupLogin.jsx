import React, { useEffect, useState } from "react";
import Login from "../Login/Login";
import Signup from "../Signup/Signup";
import LandingPage from "../LandingPge/LandingPage";
import { motion } from "framer-motion";
import { useLocation } from "react-router-dom";
import AccountActivatedPage from "../AccountActivatedPage/AccountActivatedPage";

const SignupLogin = () => {
    // use useLocatio to access params / data
    const location = useLocation();
    const params = new URLSearchParams(location.search);

    // Access query parameters after activating account by email verification
    const accountActivated = params.get("activated");
    console.log(accountActivated);

    const defaultBtnBg = "bg-white text-cyan-700";
    const containerVariants = {
        initial: { opacity: 0, y: -10 },
        animate: { opacity: 1, y: 0, transition: { duration: 0.9 } },
    };

    const [currentPage, setCurrentPage] = useState("landing");
    useEffect(() => {
        if (accountActivated == "true") {
            setCurrentPage("activated");
        }
    }, []);

    const [signupBtnBackground, setSignupBtnBackground] =
        useState(defaultBtnBg);
    const [haveAccBtnBackground, setHaveAccBtnBackground] =
        useState(defaultBtnBg);

    const handleSignup = () => {
        setSignupBtnBackground("bg-cyan-700 text-white");
        setHaveAccBtnBackground(defaultBtnBg);
        setCurrentPage("signup");
    };

    const handleAlreadyHaveAccount = () => {
        setCurrentPage("login");
        setHaveAccBtnBackground("bg-cyan-700 text-white");
        setSignupBtnBackground(defaultBtnBg);
    };

    return (
        <motion.div
            className="h-screen flex flex-row bg-gray-200"
            initial="initial"
            animate="animate"
            variants={containerVariants}
        >
            <div className="flex justify-center items-center w-1/3 border border-r-amber-400">
                <div className="w-full p-6">
                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className={`w-full ${signupBtnBackground} hover:bg-cyan-700 hover:text-white font-bold py-2 rounded-xl mb-4 transition duration-300`}
                        onClick={handleSignup}
                    >
                        Sign Up
                    </motion.button>

                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className={`w-full ${haveAccBtnBackground} hover:bg-cyan-700 hover:text-white font-bold py-2 rounded-xl mb-4 transition duration-300`}
                        onClick={handleAlreadyHaveAccount}
                    >
                        Have an Account
                    </motion.button>
                </div>
            </div>
            <div className="flex justify-center items-center overflow-y-auto w-2/3">
                <div className="w-full px-6">
                    {currentPage === "landing" && <LandingPage />}
                    {currentPage === "activated" && <AccountActivatedPage />}
                    {currentPage === "login" && <Login />}
                    {currentPage === "signup" && <Signup />}
                </div>
            </div>
        </motion.div>
    );
};

export default SignupLogin;

// process 2

// import React, { useState } from "react";
// import Login from "../Login/Login";
// import Signup from "../SignUp/SignUp";
// import LandingPage from "../LandingPge/LandingPage";
// import { motion } from "framer-motion";

// const SignupLogin = () => {
//     const [currentPage, setCurrentPage] = useState("landing");
//     const [buttonBackground, setButtonBackground] = useState("bg-cyan-500 text-white");

//     const handleButtonClick = (page) => {
//         setCurrentPage(page);
//         setButtonBackground(page === "signup" ? "bg-cyan-700 text-white" : "bg-cyan-500 text-white");
//     };

//     return (
//         <div className="h-screen flex flex-row bg-gray-100">
//             <div className="flex justify-center items-center w-1/3 border border-r-amber-400">
//                 <div className="w-full p-6">
//                     <motion.button
//                         whileHover={{ scale: 1.05 }}
//                         whileTap={{ scale: 0.95 }}
//                         className={`w-full ${buttonBackground} hover:bg-cyan-700 font-bold py-2 rounded-xl mb-4 transition duration-200`}
//                         onClick={() => handleButtonClick("signup")}
//                     >
//                         Sign Up
//                     </motion.button>
//                     <motion.button
//                         whileHover={{ scale: 1.05 }}
//                         whileTap={{ scale: 0.95 }}
//                         className={`w-full ${buttonBackground} hover:bg-cyan-700 font-bold py-2 rounded-xl mb-4 transition duration-200`}
//                         onClick={() => handleButtonClick("login")}
//                     >
//                         Have an Account
//                     </motion.button>
//                 </div>
//             </div>
//             <div className="flex justify-center items-center w-2/3">
//                 <div className="w-full p-6">
//                     {currentPage === "landing" && <LandingPage />}
//                     {currentPage === "login" && <Login />}
//                     {currentPage === "signup" && <Signup />}
//                 </div>
//             </div>
//         </div>
//     );
// };

// export default SignupLogin;

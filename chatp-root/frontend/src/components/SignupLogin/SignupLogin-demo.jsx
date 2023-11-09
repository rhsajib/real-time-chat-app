
import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Login from "../Login/Login";
import Signup from "../Signup/Signup";

const SignupLogin = () => {
  const [currentPage, setCurrentPage] = useState("landing");

  const handleAlreadyHaveAccount = () => {
    setCurrentPage("login");
  };

  const handleSignup = () => {
    setCurrentPage("signup");
  };

  const handleBackToLanding = () => {
    setCurrentPage("landing");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="max-w-md w-full p-6">
        <AnimatePresence wait>
          {currentPage === "landing" && (
            <motion.div
              key="landing"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <button
                className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 rounded-xl mb-4 transition duration-300"
                onClick={handleSignup}
              >
                Sign up
              </button>
              <button
                className="w-full bg-cyan-700 hover:bg-cyan-800 text-white font-bold py-2 rounded-xl transition duration-300"
                onClick={handleAlreadyHaveAccount}
              >
                Already have an account
              </button>
            </motion.div>
          )}
          {currentPage === "login" && (
            <motion.div
              key="login"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <button
                className="w-full bg-cyan-700 hover:bg-cyan-800 text-white font-bold py-2 rounded-xl transition duration-300"
                onClick={handleBackToLanding}
              >
                Back to Landing
              </button>
              <Login />
            </motion.div>
          )}
          {currentPage === "signup" && (
            <motion.div
              key="signup"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <button
                className="w-full bg-cyan-700 hover:bg-cyan-800 text-white font-bold py-2 rounded-xl transition duration-300"
                onClick={handleBackToLanding}
              >
                Back to Landing
              </button>
              <Signup />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default SignupLogin;





// the following one is great. just try it...!


// import React, { useState } from "react";
// import Login from "../Login/Login";
// import Signup from "../SignUp/SignUp";

// const SignupLogin = () => {
//     const [currentPage, setCurrentPage] = useState("landing");

//     const handleAlreadyHaveAccount = () => {
//         setCurrentPage("login");
//     };

//     const handleSignup = () => {
//         setCurrentPage("signup");
//     };

//     const handleBackToLanding = () => {
//         setCurrentPage("landing");
//     };

//     return (
//         <div className="min-h-screen flex items-center justify-center bg-gray-100">
//             <div className="max-w-md w-full p-6">
//                 {currentPage === "landing" && (
//                     <div>
//                         <button
//                             className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 rounded-xl mb-4 transition duration-300"
//                             onClick={handleSignup}
//                         >
//                             Sign up
//                         </button>
//                         <button
//                             className="w-full bg-cyan-700 hover:bg-cyan-800 text-white font-bold py-2 rounded-xl transition duration-300"
//                             onClick={handleAlreadyHaveAccount}
//                         >
//                             Already have an account
//                         </button>
//                     </div>
//                 )}
//                 {currentPage === "login" && (
//                     <div>
//                         <button
//                             className="w-full bg-cyan-700 hover:bg-cyan-800 text-white font-bold py-2 rounded-xl transition duration-300"
//                             onClick={handleBackToLanding}
//                         >
//                             Back to Landing
//                         </button>
//                         <Login />
//                     </div>
//                 )}
//                 {currentPage === "signup" && (
//                     <div>
//                         <button
//                             className="w-full bg-cyan-700 hover:bg-cyan-800 text-white font-bold py-2 rounded-xl transition duration-300"
//                             onClick={handleBackToLanding}
//                         >
//                             Back to Landing
//                         </button>
//                         <Signup />
//                     </div>
//                 )}
//             </div>
//         </div>
//     );
// };

// export default SignupLogin;




// import React, { useState } from "react";
// import Login from "../Login/Login";
// import Signup from "../SignUp/SignUp";
// // import Signup from "../Signup/Signup"; // Import your Signup component here

// const SignupLogin = () => {
//     const [showLogin, setShowLogin] = useState(false);
//     const [showSignup, setShowSignup] = useState(false);

//     const handleAlreadyHaveAccount = () => {
//         setShowLogin(true);
//         setShowSignup(false); // Ensure Signup is hidden when switching to Login
//     };

//     const handleSignup = () => {
//         setShowLogin(false); // Ensure Login is hidden when switching to Signup
//         setShowSignup(true);
//     };

//     return (
//         <div className="min-h-screen flex items-center justify-center bg-gray-100">
//             <div className="max-w-md w-full p-6">
//                 {showLogin ? (
//                     <Login />
//                 ) : showSignup ? (
//                     <Signup />
//                 ) : (
//                     <div>
//                         <button
//                             className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 rounded-xl mb-4 transition duration-300"
//                             onClick={handleSignup}
//                         >
//                             Sign up
//                         </button>
//                         <button
//                             className="w-full bg-cyan-700 hover:bg-cyan-800 text-white font-bold py-2 rounded-xl transition duration-300"
//                             onClick={handleAlreadyHaveAccount}
//                         >
//                             Already have an account
//                         </button>
//                     </div>
//                 )}
//             </div>
//         </div>
//     );
// };

// export default SignupLogin;



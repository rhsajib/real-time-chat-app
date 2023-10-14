import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getToken, removeToken } from "../../utilities/tokenService";
import { authUserLoader } from "../../utilities/apiLoaders";

const Auth = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const token = getToken();
        if (token) {
            authUserLoader()
                .then((user) => {
                    // console.log(user)
                    if (user.id) {
                        setIsAuthenticated(true);
                    } else {
                        setIsAuthenticated(false);
                        removeToken(); // Remove the token from storage if it's invalid
                        // otherwise every time if i click in login it will go to SignupLogin page
                        // and will not render Login page.
                        navigate("/"); // Navigate to "/" route when not authenticated
                    }
                })
                .catch((error) => {
                    console.error("Error fetching auth user:", error);
                    // Handle the error as needed
                });
        } else {
            setIsAuthenticated(false);
            navigate("/"); // Navigate to "/" route when not authenticated
        }
    }, [navigate]);

    return isAuthenticated ? children : null;
};

export default Auth;

// import React, { useEffect, useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { getToken } from "../../utilities/tokenService";
// import { authUserLoader } from "../../utilities/apiLoaders";

// const Auth = ({ children }) => {
//     const [isAuthenticated, setIsAuthenticated] = useState(false);
//     const navigate = useNavigate();

//     useEffect(() => {
//         const token = getToken();
//         authUserLoader()
//             .then((user) => {
//                 if (user) {
//                     setIsAuthenticated(true);
//                 }
//             })
//             .catch((error) => {
//                 console.error("Error fetching auth user:", error);
//                 // Handle the error as needed
//             });
//     }, []);

//     return isAuthenticated ? children : navigate("/");
// };

// export default Auth;

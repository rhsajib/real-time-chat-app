// import React, { useEffect, useState } from "react";
// import { Route, useNavigate } from "react-router-dom";

// import { authUserLoader } from "../../utilities/apiLoaders";
// import { getToken } from "../../utilities/tokenService";

// const Auth = ({ component: Component, ...rest }) => {
//     const [isAuthenticated, setIsAuthenticated] = useState(false);
//     const navigate = useNavigate(); 

//     useEffect(() => {
//         const token = getToken();
//         authUserLoader()
//             .then((user) => {
//                 if (user) {
//                     setIsAuthenticated(true); // Implement your own function to check if the user is authenticated
//                 }
//             })
//             .catch((error) => {
//                 console.error("Error fetching auth user:", error);
//                 // Handle the error as needed
//             });

//     }, []);

//     return (
//         <Route
//             {...rest}
//             render={(props) =>
//                 isAuthenticated ? <Component {...props} /> : navigate("/")
//             }
//         />
//     );
// };

// export default Auth;

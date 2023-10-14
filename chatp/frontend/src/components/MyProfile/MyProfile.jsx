import React, { useEffect, useState } from "react";
import { Link, useLoaderData, useNavigate } from "react-router-dom";
import { chatIdLoader, newChatIdLoader } from "../../utilities/apiLoaders";

const MyProfile = () => {
    const profile = useLoaderData();
    // console.log(profile);
    const { first_name, last_name, email, username, phone, active, id } =
        profile;


    return (
        <div className="flex justify-center items-center h-screen">
            
                <ul>
                    <li>User Name: {username}</li>
                    <li>First Name: {first_name}</li>
                    <li>Last Name: {last_name}</li>
                    <li>Email: {email}</li>
                    <li>Phone: {phone}</li>
                    <li>Status: {active ? "Active" : "Not Active"}</li>
                </ul>
          
           
        </div>
    );
};

export default MyProfile;

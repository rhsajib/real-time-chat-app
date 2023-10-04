import React, { useState } from "react";
import User from "../User/User";

const Users = ({ users }) => {
    // const [messages, setMessages] = useState([])

    // const handleUserMessages = (user) => {
    //     const userId = user.id
    //     const messages = messagesLoader(userId)
    //     useState[messages]
    // }

    return (
        <div className="mx-3 mb-3">
            {users.map((user) => (
                <User key={user.id} user={user} />
            ))}
        </div>
    );
};

export default Users;


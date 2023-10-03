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
        <div>
            <div >
                
                <div className="flex flex-col">
                    {users.map((user) => (
                        <User key={user.id} user={user} />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Users;

// return (
//     <div>
//         <ul role="list" class="p-6 divide-y divide-slate-200">
//         {#each people as person}
//             <!-- Remove top/bottom padding when first/last child -->
//             <li class="flex py-4 first:pt-0 last:pb-0">
//                 <img class="h-10 w-10 rounded-full" src="{person.imageUrl}" alt="" />
//                 <div class="ml-3 overflow-hidden">
//                     <p class="text-sm font-medium text-slate-900">{person.name}</p>
//                     <p class="text-sm text-slate-500 truncate">{person.email}</p>
//                 </div>
//             </li>
//         {/each}
//         </ul>
//     </div>
// );

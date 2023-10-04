import React from 'react';

const Message = ({message}) => {
    return (
        <div className='p-2 my-2 mx-3 bg-slate-300 rounded-md'>
            <h1>{message.user_id}</h1>
            <p>{message.message}</p>
            <p><small>{message.created_at}</small></p>           
        </div>
    );
};

export default Message;
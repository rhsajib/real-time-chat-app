import React, { useEffect, useState } from "react";

const SendMessage = ({ handleSendMesaage }) => {
    const [messageText, setMessageText] = useState("");

    const handleSendClick = () => {
        // Call the parent's handleSendMessage function to send the message
        handleSendMesaage(messageText);

        // Clear the input field by resetting messageText to an empty string
        setMessageText("");
    };

    const handleFormSubmit = (e) => {
        e.preventDefault(); // Prevent the default form submission behavior
        handleSendClick(); // Trigger the send click when the form is submitted
    };

    // ref: https://codingbeautydev.com/blog/react-get-input-value-on-button-click/
    // ref: https://bobbyhadz.com/blog/react-get-input-value
    // this function will dynamically track every change of message in input box
    const handleMessageTextChange = (e) => {
        // console.log(e);
        setMessageText(e.target.value);
    };

    return (
        <form onSubmit={handleFormSubmit}>
            <div className="my-3 flex flex-row mx-4">
                <input
                    className="placeholder:italic placeholder:text-slate-400 bg-white w-full border border-slate-300 rounded-md py-2 px-4 shadow-sm focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1"
                    type="text"
                    id="message"
                    name="message"
                    value={messageText}
                    onChange={handleMessageTextChange}
                    placeholder="Write text..."
                    autoComplete="off"
                />
                <button
                    type="submit"
                    className="bg-slate-400 rounded-lg ml-3 px-4"
                    // onClick={handleSendClick}
                >
                    <span>Send</span>
                </button>
            </div>
        </form>
    );
};

export default SendMessage;

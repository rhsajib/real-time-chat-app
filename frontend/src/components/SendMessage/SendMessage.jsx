import React, { useState } from "react";

const SendMessage = ({ handleSendMesaage }) => {
    const [messageText, setMessageText] = useState("");
    const [textareaClasses, setTextareaClasses] = useState("max-h-10");

    const handleSendMessageClick = () => {
        // Call the parent's handleSendMessage function to send the message
        handleSendMesaage(messageText.trim()); // Trim leading and trailing whitespace

        // Clear the input field by resetting messageText to an empty string
        setMessageText("");
        setTextareaClasses("max-h-10");
    };

    const handleFormSubmit = (e) => {
        e.preventDefault(); // Prevent the default form submission behavior

        if (messageText.trim() !== "") {
            handleSendMessageClick(); // Trigger the send click when the form is submitted
        }
    };

    // ref: https://codingbeautydev.com/blog/react-get-input-value-on-button-click/
    // ref: https://bobbyhadz.com/blog/react-get-input-value
    // this function will dynamically track every change of message in text box
    const handleMessageTextChange = (e) => {
        // console.log(e);

        const { value } = e.target;
        setMessageText(value);
        // or
        // setMessageText(e.target.value);

        if (value.length !== 0) {
            setTextareaClasses("max-h-24");
        } else {
            setTextareaClasses("max-h-10");
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault(); // Prevent the default Enter key behavior
            handleSendMessageClick(); // Send the message
        }
    };

    return (
        <form onSubmit={handleFormSubmit}>
            <div className="my-3 flex flex-row justify-center items-center mx-4">
                <div className="grow">
                    <textarea
                        // ref={textAreaRef}  // scroll below to see the implementation of ref
                        className={`${textareaClasses} w-full border rounded-md py-2 px-4 shadow-sm placeholder:italic placeholder:text-slate-400 bg-white border-slate-300 focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1`}
                        id="message"
                        name="message"
                        value={messageText}
                        onChange={handleMessageTextChange}
                        onKeyDown={handleKeyPress}
                        placeholder="Write text..."
                        autoComplete="off"
                    />
                </div>
                <div className="">
                    <button
                        type="submit"
                        className="bg-slate-400 rounded-lg ml-3 px-4 py-1"

                        // onClick={handleSendClick}
                    >
                        Send
                    </button>
                </div>
            </div>
        </form>
    );
};

export default SendMessage;

/* 

* the default height of the textarea and change it.

import React, { Component, createRef } from 'react';

class MyComponent extends Component {
  constructor(props) {
    super(props);
    this.textAreaRef = createRef(); // Create a ref for the textarea element
    this.state = {
      defaultHeight: 0, // Store the default height here
      currentHeight: 0, // Store the current height here
    };
  }

  componentDidMount() {
    // Access the default height of the textarea element after it has been rendered
    const defaultHeight = this.textAreaRef.current.clientHeight;
    this.setState({ defaultHeight }); // Update the state with the default height
  }

  handleTextAreaResize = () => {
    // Access the current height of the textarea element
    const currentHeight = this.textAreaRef.current.clientHeight;
    this.setState({ currentHeight }); // Update the state with the current height
  };

  render() {
    return (
      <div>
        <textarea
          ref={this.textAreaRef}
          onInput={this.handleTextAreaResize}
          style={{ height: `${this.state.currentHeight}px` }} // Dynamically adjust the height
        ></textarea>
        <p>Default Height: {this.state.defaultHeight}px</p>
      </div>
    );
  }
}

export default MyComponent;

*/

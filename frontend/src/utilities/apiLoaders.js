// user -------------------------------------------------------------
const usersLoader = () => fetch("http://127.0.0.1:8000/api/v1/user/all");

const userProfileLoader = (userId) =>
    fetch(`http://127.0.0.1:8000/api/v1/user/info/${userId}`);

const myProfileLoader = (userId) =>
    fetch("http://127.0.0.1:8000/api/v1/user/info/me");

const privateChatsLoader = () =>
    fetch("http://127.0.0.1:8000/api/v1/chat/private/msg-rcpnts/");

// chat -------------------------------------------------------------
const chatsLoader = () =>
    fetch("http://127.0.0.1:8000/api/v1/chat/private/all");

const messageLoader = (chatId) =>
    fetch(`http://127.0.0.1:8000/api/v1/chat/private/chat-info/${chatId}`);


const chatIdLoader =async (userId) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/v1/chat/private/recipient/get-chat/${userId}`);
      const data = await response.json();
    //   console.log(data.chat_id)
      return data.chat_id;
    } catch (error) {
      console.error("Error fetching chat ID:", error);
      throw error; // You can handle the error as needed
    }
  };

const newChatIdLoader = async (userId) => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/v1/chat/private/recipient/create-chat/${userId}`);
        const data = await response.json();
      //   console.log(data.chat_id)
        return data.chat_id;
      } catch (error) {
        console.error("Error fetching chat ID:", error);
        throw error; // You can handle the error as needed
      }
}
  

export {
    chatsLoader,
    messageLoader,
    privateChatsLoader,
    usersLoader,
    userProfileLoader,
    myProfileLoader,
    chatIdLoader,
    newChatIdLoader
};

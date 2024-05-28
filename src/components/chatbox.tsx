import React, { useState } from "react";

type ChatMessage = {
  id: number;
  text: string;
};

const Chatbox: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState("");

  const handleMessageSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputText.trim() !== "") {
      setMessages([
        ...messages,
        { id: messages.length, text: inputText.trim() },
      ]);
      setInputText("");
    }
  };

  return (
    <div className="chatbox">
      <div className="messages">
        {messages.map((message) => (
          <div key={message.id} className="message">
            {message.text}
          </div>
        ))}
      </div>
      <form onSubmit={handleMessageSubmit} className="input-form">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default Chatbox;

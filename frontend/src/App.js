import React, { useState, useRef, useEffect } from 'react';

function App() {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState([]);
  const chatEndRef = useRef(null);

  // Scroll to latest message automatically
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chat]);

  const handleSend = async () => {
    if (!message.trim()) return;

    // Add user's message to chat
    const newUserMessage = { text: message, sender: 'user' };
    setChat(prev => [...prev, newUserMessage]);
    setMessage('');

    // Call API
    try {
      const response = await fetch('http://127.0.0.1:5000/predict_intent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });
      const data = await response.json();

      const botMessage = { text: `Predicted Intent: ${data.intent}`, sender: 'bot' };
      setChat(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = { text: 'Error: Could not fetch intent', sender: 'bot' };
      setChat(prev => [...prev, errorMessage]);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      background: 'linear-gradient(135deg, #a8e6cf, #dcedc1, #ffd3b6)',
      fontFamily: 'Arial, sans-serif',
      padding: 20
    }}>
      <div style={{
        width: '100%',
        maxWidth: 500,
        display: 'flex',
        flexDirection: 'column',
        borderRadius: 25,
        boxShadow: '0 15px 35px rgba(0,0,0,0.2)',
        background: 'linear-gradient(145deg, #ffffff, #e0f7e9)',
        overflow: 'hidden',
      }}>
        <h2 style={{
          textAlign: 'center',
          color: '#2e7d32',
          margin: '25px 0',
          fontSize: 26,
          fontWeight: 'bold'
        }}>
          Intent Recognition Chat
        </h2>

        {/* Chat Area */}
        <div style={{
          flex: 1,
          minHeight: 300,
          maxHeight: 400,
          overflowY: 'auto',
          padding: 20,
          display: 'flex',
          flexDirection: 'column',
          gap: 12,
          background: 'linear-gradient(to bottom, #f5f5f5, #e8f5e9)'
        }}>
          {chat.map((msg, idx) => (
            <div key={idx} style={{
              display: 'flex',
              justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start'
            }}>
              <div style={{
                background: msg.sender === 'user'
                  ? 'linear-gradient(135deg, #4caf50, #81c784)'
                  : 'linear-gradient(135deg, #80deea, #4dd0e1)',
                color: 'white',
                padding: '10px 15px',
                borderRadius: msg.sender === 'user' ? '20px 20px 0 20px' : '20px 20px 20px 0',
                maxWidth: '70%',
                wordWrap: 'break-word',
                boxShadow: '0 3px 6px rgba(0,0,0,0.15)',
                transition: '0.3s'
              }}>
                {msg.text}
              </div>
            </div>
          ))}
          <div ref={chatEndRef}></div>
        </div>

        {/* Input */}
        <div style={{
          display: 'flex',
          gap: 10,
          padding: 20,
          background: 'linear-gradient(135deg, #f1f8e9, #ffffff)',
          borderTop: '1px solid #c8e6c9'
        }}>
          <input
            type="text"
            value={message}
            onChange={e => setMessage(e.target.value)}
            placeholder="Type your message..."
            style={{
              flex: 1,
              padding: 14,
              borderRadius: 25,
              border: '1px solid #ccc',
              outline: 'none',
              fontSize: 16,
              boxShadow: 'inset 0 2px 5px rgba(0,0,0,0.1)',
            }}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
          />
          <button
            onClick={handleSend}
            style={{
              padding: '0 25px',
              borderRadius: 25,
              border: 'none',
              background: 'linear-gradient(135deg, #43a047, #66bb6a)',
              color: 'white',
              fontSize: 16,
              cursor: 'pointer',
              transition: '0.3s'
            }}
            onMouseOver={e => e.target.style.background = 'linear-gradient(135deg, #2e7d32, #4caf50)'}
            onMouseOut={e => e.target.style.background = 'linear-gradient(135deg, #43a047, #66bb6a)'}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;

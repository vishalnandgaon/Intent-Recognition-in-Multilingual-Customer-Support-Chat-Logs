import React, { useState } from 'react';

function App() {
  const [message, setMessage] = useState('');
  const [intent, setIntent] = useState('');

  const handleSend = async () => {
    const response = await fetch('http://127.0.0.1:5000/predict_intent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    const data = await response.json();
    setIntent(data.intent);
  };

  return (
    <div style={{ maxWidth: 400, margin: 'auto', padding: 20 }}>
      <h2>Intent Recognition Chat</h2>
      <input
        type="text"
        value={message}
        onChange={e => setMessage(e.target.value)}
        placeholder="Type your message"
        style={{ width: '100%', marginBottom: 10 }}
      />
      <button onClick={handleSend} style={{ width: '100%' }}>Send</button>
      {intent && (
        <div style={{ marginTop: 20 }}>
          <strong>Predicted Intent:</strong> {intent}
        </div>
      )}
    </div>
  );
}

export default App;
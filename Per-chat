from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IPSearchRequest(BaseModel):
    ip: str

@app.post("/search/ip")
async def search_ip(request: IPSearchRequest):
    # Dummy response; replace with real API calls
    return {
        "ip": request.ip,
        "splunk": "Yes",
        "firewall": "No",
        "inventory": "Yes"
    }

=====================================
Frontend (React)
frontend/package.json
{
  "name": "ip-search-chatbot",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start"
  }
}


--------------------------
frontend/src/App.js

import React, { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSearch = async () => {
    if (!input) return;
    const res = await fetch("http://localhost:8000/search/ip", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ip: input }),
    });
    const data = await res.json();
    setMessages([
      ...messages,
      {
        user: input,
        bot: `Splunk: ${data.splunk}, Firewall: ${data.firewall}, Inventory: ${data.inventory}`,
      },
    ]);
    setInput("");
  };

  return (
    <div style={{ maxWidth: 500, margin: "auto", padding: 20 }}>
      <h2>IP Search Chatbot</h2>
      <div style={{ minHeight: 200, border: "1px solid #ccc", padding: 10 }}>
        {messages.map((m, i) => (
          <div key={i}>
            <b>User:</b> {m.user}
            <br />
            <b>Bot:</b> {m.bot}
            <br />
            <br />
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Enter IP address"
        style={{ width: "70%" }}
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
}

export default App;


======================
http://localhost:8000/search/ip).
frontend/src/index.js

import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);

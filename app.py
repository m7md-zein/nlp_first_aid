"""
Member 5 - UI: Flask Web Interface
Run: python app.py  then open http://localhost:5000
"""

from flask import Flask, render_template_string, request, jsonify
from chatbot import FirstAidChatbot

app = Flask(__name__)
bot = FirstAidChatbot()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>First Aid Chatbot</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Serif+Display&display=swap" rel="stylesheet">
<style>
  :root {
    --bg:        #f4f7f6;
    --surface:   #ffffff;
    --primary:   #1a6b4a;
    --primary2:  #22885e;
    --accent:    #e63946;
    --text:      #1c2b27;
    --muted:     #6b8a7f;
    --border:    #d6e4de;
    --user-bg:   #1a6b4a;
    --bot-bg:    #ffffff;
    --emergency: #fff0f0;
    --emr-border:#e63946;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'DM Sans', sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  header {
    width: 100%;
    background: var(--primary);
    padding: 20px 32px;
    display: flex;
    align-items: center;
    gap: 14px;
  }
  .logo {
    width: 44px; height: 44px;
    background: white;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
  }
  header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    color: white;
  }
  header p {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.7);
    margin-top: 2px;
  }

  .wrapper {
    width: 100%;
    max-width: 720px;
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 20px 16px;
    gap: 14px;
  }

  .messages {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 12px;
    overflow-y: auto;
    max-height: 58vh;
    padding: 4px 2px;
  }

  .msg-row { display: flex; align-items: flex-end; gap: 8px; }
  .msg-row.user { flex-direction: row-reverse; }

  .avatar {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; flex-shrink: 0;
  }
  .avatar.bot  { background: var(--primary); }
  .avatar.user { background: var(--primary2); }

  .bubble {
    padding: 12px 16px;
    border-radius: 18px;
    max-width: 78%;
    font-size: 0.92rem;
    line-height: 1.6;
    white-space: pre-wrap;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
  }
  .bubble.bot {
    background: var(--bot-bg);
    border-bottom-left-radius: 4px;
    border: 1px solid var(--border);
    color: var(--text);
  }
  .bubble.user {
    background: var(--user-bg);
    border-bottom-right-radius: 4px;
    color: white;
  }
  .bubble.emergency {
    background: var(--emergency);
    border: 1.5px solid var(--emr-border);
  }

  .intent-tag {
    display: inline-block;
    margin-top: 7px;
    font-size: 0.7rem;
    background: #eaf2ee;
    color: var(--primary);
    padding: 2px 8px;
    border-radius: 20px;
    font-weight: 500;
  }

  .quick-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
  }
  .quick-wrap button {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 0.8rem;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
    cursor: pointer;
    transition: all 0.15s;
  }
  .quick-wrap button:hover {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
  }

  .input-row {
    display: flex;
    gap: 10px;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 28px;
    padding: 6px 6px 6px 18px;
    transition: border-color 0.2s;
  }
  .input-row:focus-within { border-color: var(--primary); }
  .input-row input {
    flex: 1;
    border: none; outline: none;
    font-size: 0.93rem;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
    background: transparent;
  }
  .input-row button {
    background: var(--primary);
    color: white;
    border: none;
    border-radius: 22px;
    padding: 10px 22px;
    font-size: 0.88rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s;
  }
  .input-row button:hover { background: var(--primary2); }

  .disclaimer {
    font-size: 0.72rem;
    color: var(--muted);
    text-align: center;
    padding: 4px;
  }

  .typing { display: flex; gap: 4px; padding: 14px 16px; }
  .typing span {
    width: 7px; height: 7px;
    background: var(--muted);
    border-radius: 50%;
    animation: bounce 1s infinite;
  }
  .typing span:nth-child(2) { animation-delay: 0.15s; }
  .typing span:nth-child(3) { animation-delay: 0.3s; }
  @keyframes bounce {
    0%,60%,100% { transform: translateY(0); }
    30%          { transform: translateY(-6px); }
  }
</style>
</head>
<body>

<header>
  <div class="logo">🩺</div>
  <div>
    <h1>First Aid Chatbot</h1>
    <p>NHS-based guidance · Delta University AI Project</p>
  </div>
</header>

<div class="wrapper">
  <div class="messages" id="messages">
    <div class="msg-row">
      <div class="avatar bot">🩺</div>
      <div class="bubble bot">
        Hello! 👋 I'm your First Aid assistant based on <strong>NHS guidelines</strong>.<br>
        Ask me about burns, bleeding, choking, CPR, heart attack, stroke and more.<br><br>
        <strong>⚠️ In a real emergency, always call 999 first!</strong>
      </div>
    </div>
  </div>

  <div class="quick-wrap">
    <button onclick="ask('What to do for a burn?')">🔥 Burns</button>
    <button onclick="ask('Someone is bleeding heavily')">🩸 Bleeding</button>
    <button onclick="ask('Person is choking')">😮 Choking</button>
    <button onclick="ask('How to do CPR?')">❤️ CPR</button>
    <button onclick="ask('Signs of a heart attack')">💔 Heart Attack</button>
    <button onclick="ask('Stroke symptoms')">🧠 Stroke</button>
    <button onclick="ask('Someone fainted')">😵 Fainting</button>
    <button onclick="ask('Severe allergic reaction')">🐝 Anaphylaxis</button>
  </div>

  <div class="input-row">
    <input type="text" id="userInput" placeholder="Type your first aid question..."
           onkeydown="if(event.key==='Enter') sendMsg()">
    <button onclick="sendMsg()">Send ➤</button>
  </div>

  <p class="disclaimer">
    ⚠️ General first aid guidance only · Not a substitute for professional medical advice · Always call 999 in an emergency
  </p>
</div>

<script>
function ask(q) {
  document.getElementById('userInput').value = q;
  sendMsg();
}

async function sendMsg() {
  const input = document.getElementById('userInput');
  const q = input.value.trim();
  if (!q) return;
  input.value = '';

  addBubble(q, 'user', null, null);
  const typingId = addTyping();

  const res = await fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: q})
  });
  const data = await res.json();

  removeTyping(typingId);
  addBubble(data.response, data.is_emergency ? 'bot emergency' : 'bot', data.intent, data.confidence);
}

function addBubble(text, cls, intent, conf) {
  const msgs = document.getElementById('messages');
  const isUser = cls.includes('user');

  const row = document.createElement('div');
  row.className = 'msg-row' + (isUser ? ' user' : '');

  const avatar = document.createElement('div');
  avatar.className = 'avatar ' + (isUser ? 'user' : 'bot');
  avatar.textContent = isUser ? '🧑' : '🩺';

  const bubble = document.createElement('div');
  bubble.className = 'bubble ' + cls;
  bubble.textContent = text;

  if (intent) {
    const tag = document.createElement('div');
    tag.className = 'intent-tag';
    tag.textContent = intent + ' · ' + (conf * 100).toFixed(0) + '% confident';
    bubble.appendChild(tag);
  }

  row.appendChild(avatar);
  row.appendChild(bubble);
  msgs.appendChild(row);
  msgs.scrollTop = msgs.scrollHeight;
}

function addTyping() {
  const msgs = document.getElementById('messages');
  const row = document.createElement('div');
  row.className = 'msg-row';
  const id = 'typing-' + Date.now();
  row.id = id;
  row.innerHTML = '<div class="avatar bot">🩺</div><div class="bubble bot typing"><span></span><span></span><span></span></div>';
  msgs.appendChild(row);
  msgs.scrollTop = msgs.scrollHeight;
  return id;
}

function removeTyping(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}
</script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_msg = data.get('message', '')
    response, intent, confidence = bot.get_response(user_msg)
    is_emergency = response.startswith('\n⚠️')
    return jsonify({
        'response': response,
        'intent': intent,
        'confidence': round(confidence, 3),
        'is_emergency': is_emergency
    })


if __name__ == '__main__':
    print("Starting First Aid Chatbot at http://localhost:5000")
    app.run(debug=True)

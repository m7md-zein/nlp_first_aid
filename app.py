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
<title>First Aid Chatbot 🩺</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', sans-serif; background: #f0f4f8; min-height: 100vh; display: flex; flex-direction: column; align-items: center; }
  header { background: #c0392b; color: white; width: 100%; padding: 16px 24px; text-align: center; }
  header h1 { font-size: 1.5rem; }
  header p  { font-size: 0.85rem; opacity: 0.9; margin-top: 4px; }
  .chat-container { width: 100%; max-width: 700px; flex: 1; display: flex; flex-direction: column; padding: 16px; gap: 12px; }
  .messages { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; max-height: 60vh; padding-right: 4px; }
  .msg { padding: 12px 16px; border-radius: 12px; max-width: 85%; line-height: 1.5; font-size: 0.93rem; white-space: pre-wrap; }
  .msg.user { background: #2980b9; color: white; align-self: flex-end; border-bottom-right-radius: 2px; }
  .msg.bot  { background: white; color: #2c3e50; align-self: flex-start; border-bottom-left-radius: 2px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
  .msg.emergency { border-left: 4px solid #e74c3c; background: #fff5f5; }
  .intent-badge { font-size: 0.73rem; color: #7f8c8d; margin-top: 6px; }
  .input-row { display: flex; gap: 8px; }
  .input-row input { flex: 1; padding: 12px 16px; border: 1px solid #ddd; border-radius: 24px; font-size: 0.95rem; outline: none; }
  .input-row input:focus { border-color: #c0392b; }
  .input-row button { background: #c0392b; color: white; border: none; border-radius: 24px; padding: 12px 24px; cursor: pointer; font-size: 0.95rem; }
  .input-row button:hover { background: #a93226; }
  .quick-btns { display: flex; flex-wrap: wrap; gap: 6px; }
  .quick-btns button { background: #ecf0f1; border: 1px solid #bdc3c7; border-radius: 16px; padding: 6px 14px; cursor: pointer; font-size: 0.82rem; color: #2c3e50; }
  .quick-btns button:hover { background: #dfe6e9; }
  .disclaimer { font-size: 0.75rem; color: #7f8c8d; text-align: center; padding: 8px; }
</style>
</head>
<body>
<header>
  <h1>🩺 First Aid Chatbot</h1>
  <p>NHS-based first aid guidance • Delta University AI Project</p>
</header>
<div class="chat-container">
  <div class="messages" id="messages">
    <div class="msg bot">
      Hello! 👋 I'm your First Aid assistant based on NHS guidelines.<br>
      Ask me about burns, bleeding, choking, CPR, heart attack, stroke and more.<br><br>
      <strong>⚠️ In a real emergency, always call 999 first!</strong>
    </div>
  </div>
  <div class="quick-btns">
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
    <input type="text" id="userInput" placeholder="Type your first aid question..." onkeydown="if(event.key==='Enter') sendMsg()">
    <button onclick="sendMsg()">Send</button>
  </div>
  <p class="disclaimer">⚠️ This chatbot provides general first aid guidance only. Always call 999 in a real emergency. Not a substitute for professional medical advice.</p>
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

  addMsg(q, 'user', null, null);

  const res = await fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: q})
  });
  const data = await res.json();
  addMsg(data.response, data.is_emergency ? 'bot emergency' : 'bot', data.intent, data.confidence);
  scrollBottom();
}

function addMsg(text, cls, intent, conf) {
  const div = document.createElement('div');
  div.className = 'msg ' + cls;
  div.textContent = text;
  if (intent) {
    const badge = document.createElement('div');
    badge.className = 'intent-badge';
    badge.textContent = `Intent: ${intent} | Confidence: ${(conf * 100).toFixed(0)}%`;
    div.appendChild(badge);
  }
  document.getElementById('messages').appendChild(div);
  scrollBottom();
}

function scrollBottom() {
  const m = document.getElementById('messages');
  m.scrollTop = m.scrollHeight;
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

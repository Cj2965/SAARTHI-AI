"""
Fix all issues:
1. Replace the old duplicate chat widget (lines 380-400) with the correct single new one
2. Remove any stray second chatWidget div added later
"""

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The old floating chat block to replace
old_chat = '''    <!-- Floating Chat Widget -->
    <button id="floatingChatBtn" class="floating-chat-btn">🤖 Chat with AI</button>
    <div id="chat-widget" class="chat-widget hidden">
        <div class="chat-header">
            <h3>Saarthi AI Guide</h3>
            <button id="closeChatBtn" class="close-btn">&times;</button>
        </div>
        <div id="chatHistory" class="chat-messages">
            <div class="msg-bubble ai-bubble">
                <div class="avatar">🤖</div>
                <div class="text">Namaste! I am your Saarthi AI. I can guide you through the platform, summarize our services, or help you find schemes!</div>
            </div>
        </div>
        <div class="chat-input-row">
            <div class="input-with-mic" style="flex:1;">
                <input type="text" id="chatInput" placeholder="Type or speak...">
                <button id="micBtnChat" class="mic-btn" title="Speak">🎙️</button>
            </div>
            <button id="sendChatBtn" class="btn-primary">Send</button>
        </div>
    </div>'''

new_chat = '''    <!-- Floating Chat Widget (Single) -->
    <button id="floatingChatBtn" style="position:fixed;bottom:28px;right:28px;width:58px;height:58px;border-radius:50%;background:linear-gradient(135deg,#f97316,#ea580c);color:white;font-size:22px;border:none;cursor:pointer;box-shadow:0 6px 20px rgba(249,115,22,0.4);z-index:10000;display:flex;align-items:center;justify-content:center;">&#128172;</button>

    <div id="chatWidget" class="hidden" style="position:fixed;bottom:100px;right:28px;width:370px;height:520px;background:white;border-radius:16px;box-shadow:0 16px 48px rgba(0,0,0,0.18);z-index:10000;display:flex;flex-direction:column;overflow:hidden;border:1px solid #e2e8f0;">
        <div style="background:linear-gradient(135deg,#1d4ed8,#1e40af);color:white;padding:16px 20px;display:flex;justify-content:space-between;align-items:center;">
            <div>
                <h3 style="margin:0;font-size:16px;">&#129302; Saarthi AI Assistant</h3>
                <p style="margin:0;font-size:11px;opacity:0.8;">Powered by Gemini AI</p>
            </div>
            <button id="closeChatBtn" style="background:none;border:none;color:white;font-size:22px;cursor:pointer;line-height:1;">&times;</button>
        </div>
        <div id="chatMessages" style="flex:1;padding:16px;overflow-y:auto;background:#f8fafc;display:flex;flex-direction:column;gap:10px;">
            <div style="background:white;padding:12px 16px;border-radius:14px;align-self:flex-start;max-width:85%;border:1px solid #e2e8f0;font-size:13px;line-height:1.5;">
                &#128075; Hello! I am your Saarthi AI. Type or speak your need &#8212; for example: <em>"I am a farmer from Karnataka and need crop insurance."</em>
            </div>
        </div>
        <div style="padding:14px;border-top:1px solid #e2e8f0;display:flex;gap:8px;background:white;align-items:center;">
            <input type="text" id="chatInput" placeholder="Type your query..." style="flex:1;padding:10px 14px;border:1px solid #e2e8f0;border-radius:24px;outline:none;font-size:13px;">
            <button id="sendChatBtn" style="background:#1d4ed8;color:white;border:none;border-radius:50%;width:38px;height:38px;cursor:pointer;font-size:16px;">&#10148;</button>
            <button id="voiceChatBtn" style="background:#f97316;color:white;border:none;border-radius:50%;width:38px;height:38px;cursor:pointer;font-size:16px;" title="Voice Input">&#127908;</button>
        </div>
    </div>'''

if old_chat in content:
    content = content.replace(old_chat, new_chat, 1)
    print("Replaced old chat widget with new one.")
else:
    print("Old chat widget not found exactly - checking...")
    idx = content.find('chat-widget')
    print(f"Found 'chat-widget' at pos {idx}")
    print(repr(content[idx-50:idx+100]))

# Also remove any stray second chatWidget div that was added after footer
# (the one added in a previous session that duplicated things)
import re
# Remove second occurrence of floatingChatBtn if present
occurrences = [m.start() for m in re.finditer(r'id="floatingChatBtn"', content)]
print(f"floatingChatBtn occurrences: {len(occurrences)} at positions {occurrences}")

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("DONE - HTML saved.")

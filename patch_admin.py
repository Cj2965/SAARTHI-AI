import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove How Saarthi Works section
# It starts with <section id="workflow" and ends before <section id="discovery-methods"
wf_start = html.find('<section id="workflow"')
if wf_start != -1:
    wf_end = html.find('</section>', wf_start) + len('</section>')
    html = html[:wf_start] + html[wf_end:]

# 2. Fix DigiLocker Button
old_dl_btn = '''<button class="btn-ghost" style="border: 1px solid #ddd;" onclick="alert('Proceeding to DigiLocker for document verification...');">&#128272; Verify via DigiLocker</button>'''
new_dl_btn = '''<button class="btn-ghost" style="border: 1px solid #ddd;" onclick="openDigiLocker()">&#128272; Verify via DigiLocker</button>'''
if old_dl_btn in html:
    html = html.replace(old_dl_btn, new_dl_btn)
else:
    # try regex
    html = re.sub(r'<button[^>]*>.*?Verify via DigiLocker</button>', new_dl_btn, html)

# 3. Add DigiLocker Modal and Eligibility Quiz Modal
modals = """
    <!-- DigiLocker Modal -->
    <div id="digilockerModal" class="modal hidden" style="align-items: center; z-index: 10005;">
        <div class="modal-card" style="width: 450px; text-align: center; background: white; border-radius: 20px; padding: 40px;">
            <div id="dl-step1">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/DigiLocker_logo.svg/512px-DigiLocker_logo.svg.png" alt="DigiLocker" style="width: 150px; margin-bottom: 20px; display: inline-block;">
                <h3 style="color: #1e3a8a; margin-bottom: 10px;">Link DigiLocker</h3>
                <p style="color: #64748b; font-size: 14px; margin-bottom: 25px;">Securely fetch your documents to instantly verify eligibility.</p>
                <input type="text" placeholder="Enter Aadhaar Number" style="width: 100%; padding: 12px; margin-bottom: 15px; border-radius: 8px; border: 1px solid #cbd5e1; text-align: center; font-size: 16px; letter-spacing: 2px;">
                <button onclick="startDigiLockerAuth()" class="btn-primary" style="width: 100%; background: #1e40af;">Send OTP</button>
                <button onclick="document.getElementById('digilockerModal').classList.add('hidden')" class="btn-ghost" style="margin-top: 15px;">Cancel</button>
            </div>
            <div id="dl-step2" class="hidden">
                <div class="spinner" style="border-top-color: #1e40af; margin: 0 auto;"></div>
                <h4 style="color: #1e3a8a; margin-top: 20px;">Verifying & Fetching...</h4>
                <p style="color: #64748b; font-size: 13px;">Please wait while we securely access your documents.</p>
            </div>
            <div id="dl-step3" class="hidden">
                <div style="width: 60px; height: 60px; background: #22c55e; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; margin: 0 auto 20px;">&#10003;</div>
                <h3 style="color: #16a34a; margin-bottom: 15px;">Documents Verified!</h3>
                <ul style="list-style: none; padding: 0; text-align: left; background: #f8fafc; padding: 15px; border-radius: 10px; font-size: 14px; color: #334155;">
                    <li style="margin-bottom: 8px;">&#9989; Aadhaar Card fetched</li>
                    <li style="margin-bottom: 8px;">&#9989; Income Certificate fetched</li>
                    <li style="margin-bottom: 8px;">&#9989; Caste Certificate fetched</li>
                </ul>
                <button onclick="document.getElementById('digilockerModal').classList.add('hidden')" class="btn-primary" style="width: 100%; margin-top: 20px;">Continue Application</button>
            </div>
        </div>
    </div>

    <!-- Eligibility Quiz Modal -->
    <div id="eligibilityQuizModal" class="modal hidden" style="align-items: flex-start; padding-top: 50px; z-index: 10006;">
        <div class="modal-card" style="width: 600px; max-width: 95%; background: white; border-radius: 20px; padding: 35px;">
            <h2 style="color: #1d4ed8; margin-bottom: 10px; font-size: 24px;">&#128221; Pre-Application Verification</h2>
            <p style="color: #475569; font-size: 14px; margin-bottom: 25px;">Please answer these background verification questions truthfully to confirm your eligibility for <strong id="eq-scheme-name">this scheme</strong>.</p>
            
            <div id="quizQuestions">
                <div style="margin-bottom: 20px; padding: 15px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0;">
                    <p style="font-weight: 700; color: #1e293b; margin-bottom: 10px;">1. Is your annual family income strictly below ₹2.5 Lakhs?</p>
                    <div style="display: flex; gap: 15px;">
                        <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;"><input type="radio" name="q1" value="yes"> Yes, it is below ₹2.5L</label>
                        <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;"><input type="radio" name="q1" value="no"> No, it is higher</label>
                    </div>
                </div>
                
                <div style="margin-bottom: 20px; padding: 15px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0;">
                    <p style="font-weight: 700; color: #1e293b; margin-bottom: 10px;">2. Do you currently hold a valid BPL (Below Poverty Line) Ration Card?</p>
                    <div style="display: flex; gap: 15px;">
                        <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;"><input type="radio" name="q2" value="yes"> Yes</label>
                        <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;"><input type="radio" name="q2" value="no"> No</label>
                    </div>
                </div>
                
                <div style="margin-bottom: 20px; padding: 15px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0;">
                    <p style="font-weight: 700; color: #1e293b; margin-bottom: 10px;">3. Have you availed any similar government benefits in the last 3 years?</p>
                    <div style="display: flex; gap: 15px;">
                        <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;"><input type="radio" name="q3" value="yes"> Yes</label>
                        <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;"><input type="radio" name="q3" value="no"> No</label>
                    </div>
                </div>
            </div>
            
            <div id="quizResult" class="hidden" style="padding: 15px; border-radius: 10px; margin-bottom: 20px; text-align: center; font-weight: 700;"></div>

            <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px;">
                <button onclick="document.getElementById('eligibilityQuizModal').classList.add('hidden')" class="btn-ghost" style="padding: 10px 20px;">Cancel</button>
                <button id="submitQuizBtn" class="btn-primary" style="padding: 10px 24px; background: #16a34a;">Verify & Proceed</button>
            </div>
        </div>
    </div>
"""

# Check if digilockerModal already exists
if 'id="digilockerModal"' not in html:
    # Insert before Floating Chat Widget
    html = html.replace('<!-- Floating Chat Widget (Single) -->', modals + '\n    <!-- Floating Chat Widget (Single) -->')
else:
    # It exists but maybe eligibility doesn't.
    if 'id="eligibilityQuizModal"' not in html:
        html = html.replace('<!-- Floating Chat Widget (Single) -->', modals + '\n    <!-- Floating Chat Widget (Single) -->')

# Hide Dashboard nav button by default
nav_btn = '<li><a href="#" id="dashboardNavBtn">Dashboard</a></li>'
hidden_nav_btn = '<li><a href="#" id="dashboardNavBtn" style="display: none;">Admin Dashboard</a></li>'
html = html.replace(nav_btn, hidden_nav_btn)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html updated")

# Now app.js
with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Admin Login Logic
old_login = '''    if (submitAuthBtn)  submitAuthBtn.addEventListener ('click', () => {
        const email = document.getElementById('a_email');
        const pass  = document.getElementById('a_password');
        if (!email?.value || !pass?.value) return alert('Please fill in all details.');
        alert(`Successfully ${authMode === 'login' ? 'logged in' : 'registered'} as ${email.value}!`);
        closeModal('authModal');
    });'''

new_login = '''    if (submitAuthBtn)  submitAuthBtn.addEventListener ('click', () => {
        const email = document.getElementById('a_email');
        const pass  = document.getElementById('a_password');
        if (!email?.value || !pass?.value) return alert('Please fill in all details.');
        
        if (email.value === 'admin@saarthi.ai' && pass.value === 'admin123') {
            alert('Welcome Admin! You now have access to the Dashboard.');
            document.getElementById('dashboardNavBtn').style.display = 'inline-block';
        } else {
            alert(`Successfully ${authMode === 'login' ? 'logged in' : 'registered'} as ${email.value}!`);
            document.getElementById('dashboardNavBtn').style.display = 'none'; // normal users don't see dashboard
        }
        closeModal('authModal');
    });'''

js = js.replace(old_login, new_login)

# Eligibility check logic
old_elig = """            // Check Eligibility
            card.querySelector('.elig-btn').addEventListener('click', () => {
                alert(`Eligibility Check\\n\\nStatus: ${(el.status || 'Partially Eligible').toUpperCase()}\\nReason: ${el.reason || 'You meet the basic criteria. Upload documents to confirm.'}`);
            });"""

new_elig = """            // Check Eligibility Quiz
            card.querySelector('.elig-btn').addEventListener('click', () => {
                document.getElementById('eq-scheme-name').innerText = opp.name || 'Scheme';
                document.getElementById('eligibilityQuizModal').classList.remove('hidden');
                document.getElementById('quizResult').classList.add('hidden');
                document.getElementById('quizQuestions').style.display = 'block';
                
                // Clear previous answers
                document.querySelectorAll('input[type="radio"]').forEach(r => r.checked = false);
                
                // Keep track of the current card's apply button to enable it
                window.currentApplyBtn = card.querySelector('.assist-btn');
                window.currentEligBtn = card.querySelector('.elig-btn');
            });"""

js = js.replace(old_elig, new_elig)

quiz_handler = """
    // ── Eligibility Quiz Logic ───────────────────────────────
    const submitQuizBtn = document.getElementById('submitQuizBtn');
    if (submitQuizBtn) {
        submitQuizBtn.addEventListener('click', () => {
            const q1 = document.querySelector('input[name="q1"]:checked')?.value;
            const q2 = document.querySelector('input[name="q2"]:checked')?.value;
            const q3 = document.querySelector('input[name="q3"]:checked')?.value;
            
            if (!q1 || !q2 || !q3) return alert('Please answer all verification questions.');
            
            const resEl = document.getElementById('quizResult');
            document.getElementById('quizQuestions').style.display = 'none';
            resEl.classList.remove('hidden');
            
            // To pass, they must answer yes, yes, no
            if (q1 === 'yes' && q2 === 'yes' && q3 === 'no') {
                resEl.style.background = '#dcfce7';
                resEl.style.color = '#16a34a';
                resEl.innerText = '✅ Verification Passed! You are eligible to apply. Proceeding to Application...';
                
                if (window.currentEligBtn) {
                    window.currentEligBtn.innerText = 'Verified Eligible ✓';
                    window.currentEligBtn.style.color = '#16a34a';
                    window.currentEligBtn.style.borderColor = '#16a34a';
                }
                
                setTimeout(() => {
                    document.getElementById('eligibilityQuizModal').classList.add('hidden');
                    // Automatically trigger the apply with assistant flow
                    if (window.currentApplyBtn) window.currentApplyBtn.click();
                }, 2000);
            } else {
                resEl.style.background = '#fee2e2';
                resEl.style.color = '#dc2626';
                resEl.innerText = '❌ Verification Failed. Based on your answers, you do not meet the strict criteria for this scheme.';
                setTimeout(() => {
                    document.getElementById('eligibilityQuizModal').classList.add('hidden');
                }, 3500);
            }
        });
    }
"""
if 'submitQuizBtn.addEventListener' not in js:
    js += quiz_handler

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("app.js updated")

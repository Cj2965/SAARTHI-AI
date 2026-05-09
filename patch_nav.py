import re

# 1. Update index.html
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Nav adjustments
old_nav = """        <ul class="nav-links">
            <li><a href="#hero">Home</a></li>
            <li><a href="#problem">The Problem</a></li>
            <li><a href="#solution">Solution</a></li>
            <li><a href="#usp">Micro-Employment</a></li>
            <li><a href="#discover" class="nav-highlight">Find Schemes</a></li>
            <li><a href="#" id="dashboardNavBtn" style="display: none;">Admin Dashboard</a></li>
        </ul>"""

new_nav = """        <ul class="nav-links">
            <li><a href="#hero">Home</a></li>
            <li><a href="#problem">The Problem</a></li>
            <li><a href="#solution">Solution</a></li>
            <li><a href="#" onclick="openModal('microEmploymentModal')">Micro-Employment</a></li>
            <li><a href="#discover" class="nav-highlight">Find Schemes</a></li>
            <li><a href="#" onclick="openModal('dashboardModal')" class="text-blue" style="font-weight: bold;">Track Applications</a></li>
            <li><a href="#" id="dashboardNavBtn" style="display: none;">Admin Dashboard</a></li>
        </ul>"""

html = html.replace(old_nav, new_nav)

# Extract and wrap USP section into a modal
usp_start = html.find('<!-- Micro-Employment USP -->')
usp_end = html.find('</section>', usp_start) + len('</section>')

if usp_start != -1 and usp_end > usp_start:
    usp_content = html[usp_start:usp_end]
    
    micro_modal = f"""
    <!-- Micro-Employment Modal -->
    <div id="microEmploymentModal" class="modal hidden" style="align-items: center; z-index: 10010;">
        <div class="modal-card" style="width: 900px; max-width: 95%; max-height: 90vh; overflow-y: auto; background: white; border-radius: 20px; padding: 0;">
            <div style="background: linear-gradient(135deg, #f97316, #ea580c); padding: 20px 30px; color: white; display: flex; justify-content: space-between; border-radius: 20px 20px 0 0;">
                <h2 style="margin: 0; font-size: 22px;">Earn While Helping</h2>
                <button onclick="closeSmallModal('microEmploymentModal')" style="background: none; border: none; color: white; font-size: 28px; cursor: pointer;">&times;</button>
            </div>
            <div style="padding: 20px;">
                {usp_content.replace('class="info-section text-center"', 'class="text-center" style="padding: 20px;"').replace('id="usp"', 'id="usp-inner"')}
            </div>
        </div>
    </div>
    """
    # Remove from original place
    html = html[:usp_start] + html[usp_end:]
    # Inject before Floating Chat Widget
    html = html.replace('<!-- Floating Chat Widget (Single) -->', micro_modal + '\n    <!-- Floating Chat Widget (Single) -->')

# Make dynamic assistant block in pipelineModal HTML
old_assist_block = """                    <div id="assistantMatchBlock" class="hidden" style="margin-bottom: 20px; padding: 15px; background: #f0fdf4; border-radius: 10px; border: 1px solid #bbf7d0;">
                        <strong style="color: #16a34a; font-size: 15px;">✅ Assistant Automatically Matched!</strong><br>
                        <div style="display: flex; align-items: center; gap: 10px; margin-top: 10px;">
                            <div style="font-size: 30px;">👨🏽‍💼</div>
                            <div>
                                <strong>Rajesh K.</strong> (Speaks: Kannada, English)<br>
                                <span style="font-size: 12px; color: #64748b;">Rating: ⭐⭐⭐⭐⭐ (4.9) | Expertise: Govt Loans</span>
                            </div>
                        </div>
                        <p style="font-size: 12px; color: #16a34a; margin-top: 10px;">Rajesh is now assisting you. He will verify your blurry PAN card and fill the form.</p>
                    </div>"""

new_assist_block = """                    <div id="assistantMatchBlock" class="hidden" style="margin-bottom: 20px; padding: 15px; background: #f0fdf4; border-radius: 10px; border: 1px solid #bbf7d0;">
                        <strong style="color: #16a34a; font-size: 15px;">✅ Assistant Automatically Matched!</strong><br>
                        <div style="display: flex; align-items: center; gap: 10px; margin-top: 10px;">
                            <div style="font-size: 30px;">👨🏽‍💼</div>
                            <div>
                                <strong id="pipeAssistName">Loading...</strong> (Speaks: <span id="pipeAssistLang">Loading...</span>)<br>
                                <span style="font-size: 12px; color: #64748b;">Rating: ⭐⭐⭐⭐⭐ (<span id="pipeAssistRating">4.9</span>) | Expertise: <span id="pipeAssistSector">General</span></span>
                            </div>
                        </div>
                        <p style="font-size: 12px; color: #16a34a; margin-top: 10px;"><span id="pipeAssistName2">Your Assistant</span> is now assisting you. They will verify missing documents and fill the form securely.</p>
                    </div>"""
html = html.replace(old_assist_block, new_assist_block)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html")

# 2. Update app.js (Dynamic questions & Assistant Match)
with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Eligibility Check Dynamic Questions
old_elig = """            // Check Eligibility Quiz
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

new_elig = """            // Check Eligibility Quiz
            card.querySelector('.elig-btn').addEventListener('click', () => {
                document.getElementById('eq-scheme-name').innerText = opp.name || 'Scheme';
                document.getElementById('eligibilityQuizModal').classList.remove('hidden');
                document.getElementById('quizResult').classList.add('hidden');
                
                // Generate Dynamic Questions based on Scheme Name/Sector
                const sector = (opp.sector || '').toLowerCase();
                let q1 = `Is your annual family income strictly below ₹${opp.income_limit || '2.5 Lakhs'}?`;
                let q2 = `Are you a permanent resident of ${opp.state || 'this state'}?`;
                let q3 = `Do you meet the specific age or category criteria for ${opp.name}?`;
                
                if (sector.includes('education')) {
                    q3 = `Have you scored above 60% in your previous academic year?`;
                } else if (sector.includes('agriculture')) {
                    q3 = `Do you possess agricultural land registered under your name?`;
                } else if (sector.includes('business')) {
                    q3 = `Do you have an active MSME registration or startup plan?`;
                }
                
                const qHtml = `
                    <div style="margin-bottom: 20px; padding: 15px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0;">
                        <p style="font-weight: 700; color: #1e293b; margin-bottom: 10px;">1. ${q1}</p>
                        <div style="display: flex; gap: 15px;">
                            <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;"><input type="radio" name="q1" value="yes"> Yes</label>
                            <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;"><input type="radio" name="q1" value="no"> No</label>
                        </div>
                    </div>
                    <div style="margin-bottom: 20px; padding: 15px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0;">
                        <p style="font-weight: 700; color: #1e293b; margin-bottom: 10px;">2. ${q2}</p>
                        <div style="display: flex; gap: 15px;">
                            <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;"><input type="radio" name="q2" value="yes"> Yes</label>
                            <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;"><input type="radio" name="q2" value="no"> No</label>
                        </div>
                    </div>
                    <div style="margin-bottom: 20px; padding: 15px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0;">
                        <p style="font-weight: 700; color: #1e293b; margin-bottom: 10px;">3. ${q3}</p>
                        <div style="display: flex; gap: 15px;">
                            <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;"><input type="radio" name="q3" value="yes"> Yes</label>
                            <label style="display: flex; align-items: center; gap: 5px; cursor: pointer;"><input type="radio" name="q3" value="no"> No</label>
                        </div>
                    </div>
                `;
                
                const qContainer = document.getElementById('quizQuestions');
                qContainer.innerHTML = qHtml;
                qContainer.style.display = 'block';
                
                // Keep track of the current card's apply button to enable it
                window.currentApplyBtn = card.querySelector('.assist-btn');
                window.currentEligBtn = card.querySelector('.elig-btn');
            });"""

js = js.replace(old_elig, new_elig)

# Dynamic Assistant in Pipeline Step 4
old_pipe = """            if (mode === 'assistant') {
                document.getElementById('formModeTitle').innerText = 'Step 4: Assistant Workflow';
                document.getElementById('assistantMatchBlock').classList.remove('hidden');
            } else {"""

new_pipe = """            if (mode === 'assistant') {
                document.getElementById('formModeTitle').innerText = 'Step 4: Assistant Workflow';
                
                // Pick a dynamic assistant based on user language or random fallback
                const assistants = [
                    { name: 'Rajesh K.', lang: 'Kannada, English', rating: '4.9' },
                    { name: 'Priya S.', lang: 'Hindi, English', rating: '4.8' },
                    { name: 'Amit P.', lang: 'Marathi, Hindi', rating: '4.7' },
                    { name: 'Meenakshi V.', lang: 'Tamil, English', rating: '4.9' }
                ];
                let chosen = assistants[Math.floor(Math.random() * assistants.length)];
                
                document.getElementById('pipeAssistName').innerText = chosen.name;
                document.getElementById('pipeAssistName2').innerText = chosen.name;
                document.getElementById('pipeAssistLang').innerText = chosen.lang;
                document.getElementById('pipeAssistRating').innerText = chosen.rating;
                document.getElementById('pipeAssistSector').innerText = (window.currentOpp || {}).sector || 'General';
                
                document.getElementById('assistantMatchBlock').classList.remove('hidden');
            } else {"""

js = js.replace(old_pipe, new_pipe)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated app.js")


with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Rename 'Why Do You Need?' to 'Profile-Based Filter Search' in the 3 discovery cards
content = content.replace(
    '<h3 class="text-saffron" style="margin:0 0 8px 0;">Why Do You Need?</h3>',
    '<h3 class="text-saffron" style="margin:0 0 8px 0;">Profile-Based Filter Search</h3>'
)

# 2. Add Occupation to Modal B and rename its title
modal_b_old = '<h2 style="margin:0; font-size:26px; color:#1d4ed8;">&#128100; Why Do You Need?</h2>'
modal_b_new = '<h2 style="margin:0; font-size:26px; color:#1d4ed8;">&#128100; Profile-Based Filter Search</h2>'
content = content.replace(modal_b_old, modal_b_new)

# Add occupation field in Modal B
old_eco_field = """                <div>
                    <label style="font-size:12px; font-weight:700; color:#374151; display:block; margin-bottom:6px;">Economic Status ▽</label>
                    <select id="mb_eco" style="width:100%; padding:10px; border-radius:10px; border:1px solid #e2e8f0;">
                        <option value="">Select Status</option>
                        <option>Below Poverty Line (BPL)</option><option>Low Income (₹0–₹1L/yr)</option>
                        <option>Middle Income (₹1L–₹5L/yr)</option><option>Upper Middle (₹5L–₹10L/yr)</option>
                        <option>High Income (₹10L+/yr)</option>
                    </select>
                </div>"""

new_eco_field = old_eco_field + """
                <div style="grid-column: span 2;">
                    <label style="font-size:12px; font-weight:700; color:#374151; display:block; margin-bottom:6px;">Occupation</label>
                    <input type="text" id="mb_occupation" placeholder="e.g. Farmer, Student, Tailor" style="width:100%; padding:10px; border-radius:10px; border:1px solid #e2e8f0;">
                </div>"""

content = content.replace(old_eco_field, new_eco_field)

# 3. Hide 'Try the Platform Now' and the old form, keep the results section visible
old_try = """    <!-- Application Features Integration -->
    <div class="features-wrapper">
        <div class="container text-center mb-40">
            <h2 class="section-title text-blue">Try the Platform Now</h2>
            <p>Experience the MVP live below.</p>
        </div>
        
        <!-- Discover Section -->
        <section id="discover" class="feature-section">
            <div class="glass-container dual-layout">"""

new_try = """    <!-- Application Features Integration -->
    <div class="features-wrapper">
        
        <!-- Discover Section -->
        <section id="discover" class="feature-section">
            <div class="glass-container dual-layout hidden" style="display:none;">"""

content = content.replace(old_try, new_try)

# 4. Integrate DigiLocker Modal
old_digi = '<button class="btn-ghost" style="border: 1px solid #ddd;" onclick="alert(\'Proceeding to DigiLocker for document verification...\');">&#128272; Verify via DigiLocker</button>'
new_digi = '<button class="btn-ghost" style="border: 1px solid #ddd;" onclick="openDigiLocker()">&#128272; Verify via DigiLocker</button>'
content = content.replace(old_digi, new_digi)

digi_modal = """
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
                <div style="width: 60px; height: 60px; background: #22c55e; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; margin: 0 auto 20px;">✓</div>
                <h3 style="color: #16a34a; margin-bottom: 15px;">Documents Verified!</h3>
                <ul style="list-style: none; padding: 0; text-align: left; background: #f8fafc; padding: 15px; border-radius: 10px; font-size: 14px; color: #334155;">
                    <li style="margin-bottom: 8px;">✅ Aadhaar Card fetched</li>
                    <li style="margin-bottom: 8px;">✅ Income Certificate fetched</li>
                    <li style="margin-bottom: 8px;">✅ Caste Certificate fetched</li>
                </ul>
                <button onclick="document.getElementById('digilockerModal').classList.add('hidden')" class="btn-primary" style="width: 100%; margin-top: 20px;">Continue Application</button>
            </div>
        </div>
    </div>
"""

content = content.replace('<!-- Floating Chat Widget (Single) -->', digi_modal + '\n    <!-- Floating Chat Widget (Single) -->')

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML successfully updated")

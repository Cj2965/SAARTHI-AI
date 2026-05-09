import sys

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# 1. Update submitProfileSearch to include occupation
old_profile_func = """    // ── Profile Search from Modal B ───────────────────────────
    window.submitProfileSearch = function() {
        const state  = document.getElementById('mb_state')?.value  || '';
        const gender = document.getElementById('mb_gender')?.value || '';
        const age    = document.getElementById('mb_age')?.value    || '';
        const caste  = document.getElementById('mb_caste')?.value  || '';
        const edu    = document.getElementById('mb_edu')?.value    || '';
        const eco    = document.getElementById('mb_eco')?.value    || '';
        const need   = document.getElementById('mb_need')?.value   || '';

        const query = need || `I am a ${gender || 'citizen'} aged ${age || '25'} from ${state || 'India'}, ${caste ? 'category: '+caste+',' : ''} ${edu ? 'education: '+edu+',' : ''} ${eco ? 'income: '+eco+',' : ''} looking for government schemes.`;"""

new_profile_func = """    // ── Profile Search from Modal B ───────────────────────────
    window.submitProfileSearch = function() {
        const state  = document.getElementById('mb_state')?.value  || '';
        const gender = document.getElementById('mb_gender')?.value || '';
        const age    = document.getElementById('mb_age')?.value    || '';
        const caste  = document.getElementById('mb_caste')?.value  || '';
        const edu    = document.getElementById('mb_edu')?.value    || '';
        const eco    = document.getElementById('mb_eco')?.value    || '';
        const occ    = document.getElementById('mb_occupation')?.value || '';
        const need   = document.getElementById('mb_need')?.value   || '';

        const query = need || `I am a ${gender || 'citizen'} aged ${age || '25'} from ${state || 'India'}, ${caste ? 'category: '+caste+',' : ''} ${edu ? 'education: '+edu+',' : ''} ${eco ? 'income: '+eco+',' : ''} ${occ ? 'occupation: '+occ+',' : ''} looking for government schemes.`;"""

app_js = app_js.replace(old_profile_func, new_profile_func)

# 2. Fix dashboard task rendering (wrap text in .task-info so CSS applies)
old_task = """            <div class="task-item">
                <div style="display:flex;justify-content:space-between;margin-bottom:15px;">
                    <div>
                        <h4>${t.scheme_name}</h4>
                        <p><strong>Tracking ID:</strong> #SRT-${(t.task_id||'').substring(0,8).toUpperCase()}</p>
                        <p><strong>Assistant:</strong> ${t.assistant_name} (${t.language}) &nbsp;|&nbsp; <strong>Fee:</strong> ₹${t.fee}</p>
                    </div>"""

new_task = """            <div class="task-item">
                <div style="display:flex;justify-content:space-between;margin-bottom:15px;">
                    <div class="task-info">
                        <h4>${t.scheme_name}</h4>
                        <p><strong>Tracking ID:</strong> #SRT-${(t.task_id||'').substring(0,8).toUpperCase()}</p>
                        <p><strong>Assistant:</strong> ${t.assistant_name} (${t.language}) &nbsp;|&nbsp; <strong>Fee:</strong> ₹${t.fee}</p>
                    </div>"""

app_js = app_js.replace(old_task, new_task)

# 3. Add DigiLocker functions
digi_funcs = """
    // ── DigiLocker Verification ───────────────────────────────
    window.openDigiLocker = function() {
        document.getElementById('digilockerModal')?.classList.remove('hidden');
        document.getElementById('dl-step1')?.classList.remove('hidden');
        document.getElementById('dl-step2')?.classList.add('hidden');
        document.getElementById('dl-step3')?.classList.add('hidden');
    };

    window.startDigiLockerAuth = function() {
        document.getElementById('dl-step1')?.classList.add('hidden');
        document.getElementById('dl-step2')?.classList.remove('hidden');
        
        // Simulate API call and verification
        setTimeout(() => {
            document.getElementById('dl-step2')?.classList.add('hidden');
            document.getElementById('dl-step3')?.classList.remove('hidden');
            
            // Mark eligibility check complete
            const sEl = document.querySelector('.elig-btn');
            if (sEl) {
                sEl.innerText = 'Verified via DigiLocker ✓';
                sEl.style.background = '#dcfce7';
                sEl.style.color = '#16a34a';
                sEl.style.border = '1px solid #16a34a';
            }
        }, 2500);
    };
"""

app_js += digi_funcs

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("app.js updated successfully")

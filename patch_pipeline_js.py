import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update Card HTML to change Apply button text
old_btns = '''                    <div style="display:flex;gap:10px;margin-top:15px;">
                        <button class="btn-ghost elig-btn" style="flex:1;">Check Eligibility</button>
                        <button class="btn-primary assist-btn" style="flex:1;">Apply with Assistant</button>
                    </div>'''

new_btns = '''                    <div style="display:flex;gap:10px;margin-top:15px;">
                        <button class="btn-ghost elig-btn" style="flex:1;">Check Eligibility</button>
                        <button class="btn-primary assist-btn" style="flex:1; background: #1d4ed8;">Start Application</button>
                    </div>'''
js = js.replace(old_btns, new_btns)

# 2. Update .assist-btn event listener
old_assist_block = """            // Apply with Assistant
            card.querySelector('.assist-btn').addEventListener('click', async () => {
                const btn = card.querySelector('.assist-btn');
                btn.innerText = 'Assigning...';
                btn.disabled  = true;
                try {
                    const r = await fetch('/api/request_assistant', {
                        method:  'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body:    JSON.stringify({ user_profile: userProfile, opportunity: opp })
                    });
                    const d = await r.json();
                    if (d.error) throw new Error(d.error);
                    alert(`✅ Assistant ${d.assistant_name} assigned!\\nTask ID: ${d.task_id}\\n\\nOpen Dashboard to track live progress.`);
                    btn.innerText = 'Assigned ✓';
                    btn.style.background = '#16a34a';
                    loadTasks();
                } catch(e) {
                    btn.innerText = 'Error';
                    console.error(e);
                }
            });"""

new_assist_block = """            // Start Application Pipeline
            card.querySelector('.assist-btn').addEventListener('click', () => {
                window.currentOpp = opp;
                window.currentUserProfile = userProfile;
                document.getElementById('pipeSchemeName').innerText = opp.name || 'Scheme';
                
                // Reset states
                window.uploadedDocsCount = 0;
                document.querySelectorAll('.upload-status').forEach(el => {
                    el.innerText = 'Click to upload';
                    el.style.color = '#64748b';
                    el.parentElement.style.borderColor = '#cbd5e1';
                    el.parentElement.style.background = 'transparent';
                });
                document.getElementById('ocrLoading').classList.add('hidden');
                document.getElementById('ocrResults').classList.add('hidden');
                
                // Show Step 1
                document.getElementById('pipeStep1').classList.remove('hidden');
                document.getElementById('pipeStep2').classList.add('hidden');
                document.getElementById('pipeStep3').classList.add('hidden');
                document.getElementById('pipeStep4').classList.add('hidden');
                
                // Close other modals if any
                closeModal('schemeDetailsModal');
                closeModal('resultsModal');
                
                openModal('pipelineModal');
            });"""

js = js.replace(old_assist_block, new_assist_block)

# 3. Add Pipeline Logic
pipeline_logic = """
    // ── Workflow Pipeline Logic ───────────────────────────────
    window.simulateFileUpload = function(type, el) {
        if (el.innerText.includes('Uploaded')) return; // already uploaded
        el.style.borderColor = '#1d4ed8';
        el.style.background = '#eff6ff';
        const statusEl = el.querySelector('.upload-status');
        statusEl.innerText = 'Uploading...';
        
        setTimeout(() => {
            statusEl.innerText = 'Uploaded ✓';
            statusEl.style.color = '#16a34a';
            el.style.borderColor = '#16a34a';
            
            window.uploadedDocsCount = (window.uploadedDocsCount || 0) + 1;
            if (window.uploadedDocsCount === 3) {
                // All required docs uploaded, trigger OCR
                document.getElementById('ocrLoading').classList.remove('hidden');
                setTimeout(() => {
                    document.getElementById('ocrLoading').classList.add('hidden');
                    document.getElementById('ocrResults').classList.remove('hidden');
                }, 2500);
            }
        }, 1000);
    };

    window.nextPipeStep = function(stepNum, mode) {
        document.getElementById('pipeStep1').classList.add('hidden');
        document.getElementById('pipeStep2').classList.add('hidden');
        document.getElementById('pipeStep3').classList.add('hidden');
        document.getElementById('pipeStep4').classList.add('hidden');
        
        if (stepNum === 2) {
            // Simulated Eligibility Check Delay
            document.getElementById('pipeStep2').classList.remove('hidden');
        } else if (stepNum === 3) {
            document.getElementById('pipeStep3').classList.remove('hidden');
        } else if (stepNum === 4) {
            document.getElementById('pipeStep4').classList.remove('hidden');
            window.applicationMode = mode;
            if (mode === 'assistant') {
                document.getElementById('formModeTitle').innerText = 'Step 4: Assistant Workflow';
                document.getElementById('assistantMatchBlock').classList.remove('hidden');
            } else {
                document.getElementById('formModeTitle').innerText = 'Step 4: Self Apply Workflow';
                document.getElementById('assistantMatchBlock').classList.add('hidden');
            }
        }
    };

    window.submitPipelineApplication = async function() {
        const btn = document.getElementById('finalSubmitBtn');
        btn.innerText = 'Submitting & Updating Tracker...';
        btn.disabled = true;
        
        try {
            // We use the same backend endpoint but we set a custom state directly or rely on the dashboard parsing
            const r = await fetch('/api/request_assistant', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify({ user_profile: window.currentUserProfile, opportunity: window.currentOpp })
            });
            const d = await r.json();
            
            // Wait to simulate backend processing
            setTimeout(() => {
                btn.innerText = 'Final Submit Application';
                btn.disabled = false;
                closeModal('pipelineModal');
                
                alert(`✅ Application Submitted Successfully!\\nTracking ID: ${d.task_id}\\n\\nYou can track this application in the Admin Dashboard and rate the workflow once approved.`);
                
                // Attempt to update task to "Submitted" immediately
                fetch('/api/tasks/update', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ task_id: d.task_id, status: 'Submitted' })
                }).then(() => loadTasks());
                
            }, 1500);
            
        } catch(e) {
            console.error(e);
            btn.innerText = 'Error - Retry';
            btn.disabled = false;
        }
    };

    // ── Rating Logic ───────────────────────────────
    let currentRating = 0;
    let currentRateTaskId = null;

    window.openRatingModal = function(taskId, assistantName) {
        currentRateTaskId = taskId;
        currentRating = 0;
        document.getElementById('rateAssistantName').innerText = assistantName || 'your assistant';
        document.getElementById('rateFeedback').value = '';
        document.querySelectorAll('#starRating span').forEach(s => s.innerText = '☆');
        openModal('rateModal');
    };

    window.setRating = function(val) {
        currentRating = val;
        const stars = document.querySelectorAll('#starRating span');
        stars.forEach((s, i) => {
            s.innerText = (i < val) ? '⭐' : '☆';
        });
    };

    window.submitRating = async function() {
        if (currentRating === 0) return alert('Please select a star rating.');
        // Simulated API send for AI learning loop
        const btn = document.querySelector('#rateModal .btn-primary');
        btn.innerText = 'Sending to AI Model...';
        setTimeout(() => {
            alert('✅ Feedback received! Our AI matching loop has been updated.');
            btn.innerText = 'Submit Feedback & Enhance AI';
            closeModal('rateModal');
        }, 1000);
    };
"""

if 'window.simulateFileUpload' not in js:
    js += pipeline_logic

# 4. Update loadTasks() for new states
old_load = """        let html = '';
        tasks.forEach(t => {
            let progressWidth = '16%';
            let s2 = '', s3 = '', s4 = '';
            if (t.status === 'Assigned')          { s2 = 'active'; progressWidth = '33%'; }
            else if (t.status === 'In Progress')  { s2 = 'completed'; s3 = 'active'; progressWidth = '66%'; }
            else if (t.status === 'Completed')    { s2 = 'completed'; s3 = 'completed'; s4 = 'completed'; progressWidth = '100%'; }

            html += `
            <div class="task-item">
                <div style="display:flex;justify-content:space-between;margin-bottom:15px;">
                    <div class="task-info">
                        <h4>${t.scheme_name}</h4>
                        <p><strong>Tracking ID:</strong> #SRT-${(t.task_id||'').substring(0,8).toUpperCase()}</p>
                        <p><strong>Assistant:</strong> ${t.assistant_name} (${t.language}) &nbsp;|&nbsp; <strong>Fee:</strong> ₹${t.fee}</p>
                    </div>
                    <div style="display:flex;gap:8px;align-items:flex-start;">
                        ${t.status !== 'In Progress' && t.status !== 'Completed'
                            ? `<button class="btn-ghost prog-btn" data-id="${t.task_id}" style="font-size:12px;">▶ Start</button>` : ''}
                        ${t.status !== 'Completed'
                            ? `<button class="btn-primary comp-btn" data-id="${t.task_id}" style="font-size:12px;">✓ Complete</button>` : ''}
                    </div>
                </div>
                <div class="tracking-wrapper" style="position:relative;display:flex;justify-content:space-between;padding-top:30px;">
                    <div style="position:absolute;top:15px;left:0;height:4px;background:#e5e7eb;width:100%;border-radius:4px;"></div>
                    <div style="position:absolute;top:15px;left:0;height:4px;background:#16a34a;border-radius:4px;transition:width 0.8s;width:${progressWidth};"></div>
                    ${['Requested','Assigned','In Progress','Completed'].map((label, i) => {"""

new_load = """        let html = '';
        tasks.forEach(t => {
            let progressWidth = '10%';
            let s2 = '', s3 = '', s4 = '', s5 = '';
            
            // Map the legacy backend status or new frontend states
            // States: Started -> Docs Verified -> Assigned -> Submitted -> Approved
            let stateMap = {
                'Requested': {w: '10%', s2:'', s3:'', s4:'', s5:''},
                'Docs Verified': {w: '30%', s2:'completed', s3:'', s4:'', s5:''},
                'Assigned': {w: '50%', s2:'completed', s3:'completed', s4:'', s5:''},
                'In Progress': {w: '50%', s2:'completed', s3:'completed', s4:'', s5:''}, // Legacy compatibility
                'Submitted': {w: '75%', s2:'completed', s3:'completed', s4:'completed', s5:''},
                'Completed': {w: '100%', s2:'completed', s3:'completed', s4:'completed', s5:'completed'},
                'Approved': {w: '100%', s2:'completed', s3:'completed', s4:'completed', s5:'completed'}
            };
            
            let status = t.status || 'Requested';
            // Default to Submitted if it just came from the new pipeline
            if (status === 'Assigned' && t.fee === 50) status = 'Assigned'; 
            
            let current = stateMap[status] || stateMap['Requested'];
            progressWidth = current.w;
            s2 = current.s2; s3 = current.s3; s4 = current.s4; s5 = current.s5;

            html += `
            <div class="task-item">
                <div style="display:flex;justify-content:space-between;margin-bottom:15px;">
                    <div class="task-info">
                        <h4>${t.scheme_name}</h4>
                        <p><strong>Tracking ID:</strong> #SRT-${(t.task_id||'').substring(0,8).toUpperCase()}</p>
                        <p><strong>Assistant/Mode:</strong> ${t.assistant_name} (${t.language}) &nbsp;|&nbsp; <strong>Fee:</strong> ₹${t.fee}</p>
                    </div>
                    <div style="display:flex;gap:8px;align-items:flex-start;">
                        ${status === 'Submitted'
                            ? `<button class="btn-ghost prog-btn" data-id="${t.task_id}" style="font-size:12px; border: 1px solid #16a34a; color: #16a34a;" onclick="updateTaskStatus('${t.task_id}', 'Approved')">✅ Approve Application</button>` : ''}
                        
                        ${(status === 'Completed' || status === 'Approved')
                            ? `<button class="btn-primary" style="font-size:12px; background: #f59e0b;" onclick="openRatingModal('${t.task_id}', '${t.assistant_name.replace(/'/g, "\\'")}')">⭐ Rate Assistant</button>` : ''}
                    </div>
                </div>
                <div class="tracking-wrapper" style="position:relative;display:flex;justify-content:space-between;padding-top:30px;">
                    <div style="position:absolute;top:15px;left:0;height:4px;background:#e5e7eb;width:100%;border-radius:4px;"></div>
                    <div style="position:absolute;top:15px;left:0;height:4px;background:#16a34a;border-radius:4px;transition:width 0.8s;width:${progressWidth};"></div>
                    ${['Started','Docs Verified','Assigned','Submitted','Approved'].map((label, i) => {"""

js = js.replace(old_load, new_load)

# Fix the map classes handling for the 5-step loop
old_map_loop = """                    ${['Requested','Assigned','In Progress','Completed'].map((label, i) => {
                        const classes = [s2,s3,s4];
                        const cls = i === 0 ? 'completed' : (classes[i-1] || '');"""
new_map_loop = """                    ${['Started','Docs Verified','Assigned','Submitted','Approved'].map((label, i) => {
                        const classes = [s2,s3,s4,s5];
                        const cls = i === 0 ? 'completed' : (classes[i-1] || '');"""

js = js.replace(old_map_loop, new_map_loop)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("app.js updated successfully")

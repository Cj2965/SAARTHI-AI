// ============================================================
// SAARTHI AI — app.js (Clean Rewrite)
// ============================================================

document.addEventListener('DOMContentLoaded', () => {

    // ── Smooth Scroll ─────────────────────────────────────────
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            e.preventDefault();
            const target = document.getElementById(href.substring(1));
            if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
    });

    // ── Helper: open / close any modal by ID ─────────────────
    function openModal(id) {
        const el = document.getElementById(id);
        if (el) el.classList.remove('hidden');
    }
    function closeModal(id) {
        const el = document.getElementById(id);
        if (el) el.classList.add('hidden');
    }

    // ── Small Modals (Sector / Profile popups) ────────────────
    window.openSmallModal  = id => openModal(id);
    window.openModal = openModal;
    window.closeSmallModal = id => closeModal(id);

    // ── Auth Modal ────────────────────────────────────────────
    let authMode = 'login';

    function openAuth(mode) {
        authMode = mode;
        const isLogin = mode === 'login';
        const title    = document.getElementById('authTitle');
        const subtitle = document.getElementById('authSubtitle');
        const nameGrp  = document.getElementById('authNameGroup');
        const submitBtn= document.getElementById('submitAuthBtn');
        const toggleBtn= document.getElementById('toggleAuthBtn');

        if (title)    title.innerText    = isLogin ? 'Welcome Back to Saarthi AI' : 'Join Saarthi AI';
        if (subtitle) subtitle.innerText = isLogin
            ? 'Sign in to manage your applications and access your assigned agents.'
            : 'Create an account to start applying for schemes or to become a Saarthi Assistant.';
        if (nameGrp)  isLogin ? nameGrp.classList.add('hidden') : nameGrp.classList.remove('hidden');
        if (submitBtn) submitBtn.innerText = isLogin ? 'Login' : 'Register';
        if (toggleBtn) toggleBtn.innerText = isLogin
            ? "Don't have an account? Register"
            : 'Already have an account? Login';
        openModal('authModal');
    }

    const loginNavBtn    = document.getElementById('loginNavBtn');
    const registerNavBtn = document.getElementById('registerNavBtn');
    const closeAuthBtn   = document.getElementById('closeAuthBtn');
    const toggleAuthBtn  = document.getElementById('toggleAuthBtn');
    const submitAuthBtn  = document.getElementById('submitAuthBtn');

    if (loginNavBtn)    loginNavBtn.addEventListener   ('click', () => openAuth('login'));
    if (registerNavBtn) registerNavBtn.addEventListener('click', () => openAuth('register'));
    if (closeAuthBtn)   closeAuthBtn.addEventListener  ('click', () => closeModal('authModal'));
    if (toggleAuthBtn)  toggleAuthBtn.addEventListener ('click', () => openAuth(authMode === 'login' ? 'register' : 'login'));
    if (submitAuthBtn)  submitAuthBtn.addEventListener ('click', () => {
        const email = document.getElementById('a_email');
        const pass  = document.getElementById('a_password');
        if (!email?.value || !pass?.value) return alert('Please fill in all details.');
        
        if (email.value === 'admin@saarthi.ai' && pass.value === 'admin123') {
            alert('Welcome Admin! You now have access to the Admin Dashboard.');
            document.getElementById('dashboardNavBtn').style.display = 'inline-block';
            document.getElementById('userProfileIcon').style.display = 'flex';
            document.getElementById('userProfileName').innerText = 'Admin';
            window.currentUserEmail = 'admin@saarthi.ai';
        } else {
            alert(`Successfully ${authMode === 'login' ? 'logged in' : 'registered'} as ${email.value}!`);
            document.getElementById('dashboardNavBtn').style.display = 'none'; 
            document.getElementById('userProfileIcon').style.display = 'flex';
            document.getElementById('userProfileName').innerText = email.value.split('@')[0];
            window.currentUserEmail = email.value;
        }
        document.getElementById('loginNavBtn').style.display = 'none';
        document.getElementById('registerNavBtn').style.display = 'none';
        closeModal('authModal');
    });

    // ── Dashboard Modal ───────────────────────────────────────
    const dashboardNavBtn  = document.getElementById('dashboardNavBtn');
    const closeDashboardBtn= document.getElementById('closeDashboardBtn');

    if (dashboardNavBtn) {
        dashboardNavBtn.addEventListener('click', e => {
            e.preventDefault();
            openModal('dashboardModal');
            loadTasks();
        });
    }
    if (closeDashboardBtn) closeDashboardBtn.addEventListener('click', () => closeModal('dashboardModal'));

    // ── Request Agent ─────────────────────────────────────────
    window.requestAgent = async function(agentName, language) {
        const newTask = {
            task_id:        'REQ-' + Math.floor(Math.random() * 100000),
            scheme_name:    'General Application Assistance',
            user_need:      'User explicitly requested help from ' + agentName,
            assistant_name: agentName,
            language:       language || 'English',
            status:         'Assigned',
            fee:            50
        };
        try {
            await fetch('/api/tasks/new', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify(newTask)
            });
            alert(`${agentName} has been assigned! Open Dashboard to track live progress.`);
            loadTasks();
        } catch(e) { console.error(e); }
    };

    // ── Sector Search helper ──────────────────────────────────
    window.searchBySector = function(sector) {
        closeModal('modalA');
        const qEl = document.getElementById('userQuery');
        if (qEl) qEl.value = 'Show me schemes for ' + sector;
        setTimeout(() => document.getElementById('searchBtn')?.click(), 200);
    };

    // ── Profile Filter helper ─────────────────────────────────
    window.filterSearch = function(filterName) {
        closeModal('modalB');
        document.getElementById('discover')?.scrollIntoView({ behavior: 'smooth' });
    };

    // ── Profile Search from Modal B ───────────────────────────
    window.submitProfileSearch = function() {
        const state  = document.getElementById('mb_state')?.value  || '';
        const gender = document.getElementById('mb_gender')?.value || '';
        const age    = document.getElementById('mb_age')?.value    || '';
        const caste  = document.getElementById('mb_caste')?.value  || '';
        const edu    = document.getElementById('mb_edu')?.value    || '';
        const eco    = document.getElementById('mb_eco')?.value    || '';
        const occ    = document.getElementById('mb_occupation')?.value || '';
        const need   = document.getElementById('mb_need')?.value   || '';

        const query = need || `I am a ${gender || 'citizen'} aged ${age || '25'} from ${state || 'India'}, ${caste ? 'category: '+caste+',' : ''} ${edu ? 'education: '+edu+',' : ''} ${eco ? 'income: '+eco+',' : ''} ${occ ? 'occupation: '+occ+',' : ''} looking for government schemes.`;

        // Pre-fill main discover form
        const qEl = document.getElementById('userQuery');
        if (qEl) qEl.value = query;
        if (state) { const sEl = document.getElementById('p_state'); if(sEl) sEl.value = state; }
        if (gender){ const gEl = document.getElementById('p_gender'); if(gEl) gEl.value = gender; }
        if (age)   { const aEl = document.getElementById('p_age');    if(aEl) aEl.value = age; }

        closeModal('modalB');
        // Instantly trigger search (which now opens resultsModal)
        setTimeout(() => document.getElementById('searchBtn')?.click(), 200);
    };

    // ── Scheme Search / Analyze ───────────────────────────────
    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {
        searchBtn.addEventListener('click', async () => {
            const query = document.getElementById('userQuery')?.value?.trim();
            if (!query) return alert('Please tell us what you need!');

            const profile = {
                state:      document.getElementById('p_state')?.value      || '',
                age:        parseInt(document.getElementById('p_age')?.value)    || 25,
                gender:     document.getElementById('p_gender')?.value     || '',
                income:     parseInt(document.getElementById('p_income')?.value) || 0,
                occupation: document.getElementById('p_occupation')?.value || '',
                language:   document.getElementById('p_language')?.value   || 'English'
            };

            const origText = searchBtn.innerText;
            searchBtn.innerText = 'Analyzing...';
            searchBtn.disabled = true;

            openModal('resultsModal');
            document.getElementById('loadingSpinner')?.classList.remove('hidden');
            const wrapper = document.getElementById('cardsWrapper');
            if (wrapper) wrapper.innerHTML = '';
            document.getElementById('emptyState')?.classList.add('hidden');

            try {
                const res  = await fetch('/api/analyze', {
                    method:  'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body:    JSON.stringify({ query, profile })
                });
                const data = await res.json();
                document.getElementById('loadingSpinner')?.classList.add('hidden');
                renderResults(data.results || [], profile);
            } catch(e) {
                console.error(e);
                document.getElementById('loadingSpinner')?.classList.add('hidden');
                alert('Error connecting to backend. Make sure the server is running.');
            } finally {
                searchBtn.innerText = origText;
                searchBtn.disabled  = false;
            }
        });
    }

    // ── Render Scheme Result Cards ────────────────────────────
    function renderResults(results, userProfile) {
        if (results) {
            window.currentResults = results;
            window.currentUserProfile = userProfile;
        } else {
            results = window.currentResults || [];
            userProfile = window.currentUserProfile || {};
        }
        
        // Apply Filters
        const searchQuery = (document.getElementById('schemeSearch')?.value || '').toLowerCase();
        const sectorQuery = document.getElementById('filterSector')?.value || '';
        const sortQuery = document.getElementById('sortSchemes')?.value || 'match';
        
        let filteredResults = results.filter(item => {
            const opp = item.opportunity || {};
            const nameMatch = (opp.name || '').toLowerCase().includes(searchQuery) || (opp.description || '').toLowerCase().includes(searchQuery);
            const sectorMatch = sectorQuery === '' || (opp.sector || '') === sectorQuery;
            return nameMatch && sectorMatch;
        });
        
        if (sortQuery === 'deadline') {
            filteredResults.sort((a, b) => {
                const dA = new Date((a.opportunity || {}).deadline || '2099-01-01').getTime();
                const dB = new Date((b.opportunity || {}).deadline || '2099-01-01').getTime();
                return dA - dB;
            });
        }
        
        const wrapper = document.getElementById('cardsWrapper');
        if (!wrapper) return;
        wrapper.innerHTML = '';

        if (!filteredResults || filteredResults.length === 0) {
            document.getElementById('emptyState')?.classList.remove('hidden');
            return;
        }
        document.getElementById('emptyState')?.classList.add('hidden');

        filteredResults.forEach((item, index) => {
            const opp   = item.opportunity || {};
            const el    = item.eligibility  || {};
            const score = el.confidence_score || (Math.floor(Math.random() * 15) + 82);

            let badgeClass = 'badge-partial';
            let badgeText  = 'Partially Eligible';
            if (el.status === 'eligible')     { badgeClass = 'badge-eligible';  badgeText = 'Eligible'; }
            if (el.status === 'not eligible') { badgeClass = 'badge-not';       badgeText = 'Not Eligible'; }

            const card = document.createElement('div');
            card.className = 'result-card';
            card.innerHTML = `
                <div class="result-badge ${badgeClass}">${badgeText}</div>
                <div class="result-sector">${opp.sector || 'General'}</div>
                <h3 class="result-name">${opp.name || 'Scheme'}</h3>
                <p class="result-desc">${(opp.description || '').substring(0, 110)}...</p>
                <div class="result-meta">
                    <span>✅ Match: <strong>${score}%</strong></span>
                    <span>📅 ${item.deadline_info?.deadline || 'Open'}</span>
                </div>
                <div class="result-actions">
                    <button class="btn-ghost read-btn">Read More</button>
                    <button class="btn-outline elig-btn">Check Eligibility</button>
                    <button class="btn-primary assist-btn">Apply with Assistant</button>
                    <button class="btn-save save-btn" title="Save">⭐</button>
                </div>
            `;
            wrapper.appendChild(card);

            // Read More → Scheme Details Modal
            card.querySelector('.read-btn').addEventListener('click', () => {
                const sdName   = document.getElementById('sd-name');
                const sdSector = document.getElementById('sd-sector');
                const sdContent= document.getElementById('sd-content');
                if (sdName)    sdName.innerText   = opp.name   || 'Scheme';
                if (sdSector)  sdSector.innerText = opp.sector || 'General';
                if (sdContent) sdContent.innerHTML = `
                    <div class="sd-block"><h4>Details</h4>
                        <p><strong>Department:</strong> ${opp.department   || 'Government of India'}</p>
                        <p><strong>State:</strong>      ${opp.state        || 'Central'}</p>
                        <p>${opp.description || ''}</p>
                    </div>
                    <div class="sd-block"><h4>Eligibility</h4>
                        <p><strong>Age:</strong>          ${opp.age_limit    || 'Any'}</p>
                        <p><strong>Income Limit:</strong> ${opp.income_limit || 'Any'}</p>
                        <p><strong>Target Group:</strong> ${opp.target_group || 'All Citizens'}</p>
                    </div>
                    <div class="sd-block"><h4>Documents Required</h4>
                        <ul>${(el.required_documents || ['Aadhaar Card','Income Certificate','Bank Passbook','Passport Photo'])
                              .map(d => `<li>${d}</li>`).join('')}</ul>
                    </div>
                    <div class="sd-block"><h4>How to Apply</h4>
                        <ol>
                            <li>Visit the official government portal or Saarthi platform.</li>
                            <li>Fill in your profile and upload documents.</li>
                            <li>Submit the application and track status here.</li>
                        </ol>
                    </div>`;
                openModal('schemeDetailsModal');
            });

            // Check Eligibility Quiz
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
            });

            // Apply with Assistant
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
                    alert(`✅ Assistant ${d.assistant_name} assigned!\nTask ID: ${d.task_id}\n\nOpen Dashboard to track live progress.`);
                    btn.innerText = 'Assigned ✓';
                    btn.style.background = '#16a34a';
                    loadTasks();
                } catch(e) {
                    btn.innerText = 'Apply with Assistant';
                    btn.disabled  = false;
                    alert('Could not assign assistant. Please try again.');
                }
            });

            // Save
            card.querySelector('.save-btn').addEventListener('click', () => {
                alert(`Scheme "${opp.name}" saved to your profile!`);
            });
        });
    }

    // ── Dashboard Task Loader ─────────────────────────────────
    let tasks = [];

    window.loadTasks = loadTasks;
    async function loadTasks() {
        const container = document.getElementById('tasksContainer');
        if (!container) return;
        try {
            const res  = await fetch('/api/tasks');
            tasks = await res.json();
            
            // FILTER LOGIC
            if (!window.currentUserEmail) {
                container.innerHTML = `<div style="text-align:center; padding:40px;"><div style="font-size:40px; margin-bottom:10px;">🔒</div><h3 style="color:#1e3a8a; margin:0 0 10px 0;">Please Login</h3><p style="color:#64748b; margin:0 0 20px 0;">You must be logged in to track your applications.</p><button class="btn-primary" onclick="closeSmallModal('dashboardModal'); document.getElementById('loginNavBtn').click();" style="padding: 10px 25px;">Login Now</button></div>`;
                return;
            } else if (window.currentUserEmail !== 'admin@saarthi.ai') {
                tasks = tasks.filter(t => t.user_profile && t.user_profile.email === window.currentUserEmail);
            }
            
        } catch(e) {
            container.innerHTML = '<p class="text-muted">Could not load tasks. Check backend.</p>';
            return;
        }

        if (tasks.length === 0) {
            container.innerHTML = '<p class="text-muted">No tasks yet. Discover a scheme and request an assistant!</p>';
            return;
        }

        let html = '';
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

            
            // Build alerts and actions based on status
            let pendingAlert = '';
            let actionText = '';
            if (status === 'Docs Verified') pendingAlert = '<span style="color:#b45309; background:#fffbeb; padding:4px 8px; border-radius:6px; font-size:11px; font-weight:bold;">⚠️ Action Needed: Missing Bank Passbook</span>';
            if (status === 'Assigned') pendingAlert = '<span style="color:#1d4ed8; background:#eff6ff; padding:4px 8px; border-radius:6px; font-size:11px; font-weight:bold;">🕒 Waiting for Assistant form review</span>';
            if (status === 'Started') pendingAlert = '<span style="color:#dc2626; background:#fee2e2; padding:4px 8px; border-radius:6px; font-size:11px; font-weight:bold;">📅 Deadline in 2 Days</span>';
            if (status === 'Approved') pendingAlert = '<span style="color:#16a34a; background:#dcfce7; padding:4px 8px; border-radius:6px; font-size:11px; font-weight:bold;">🎉 Application Approved!</span>';

            html += `
            <div class="task-item" style="border: 1px solid #e2e8f0; border-radius: 16px; padding: 25px; margin-bottom: 20px; background: #ffffff; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
                <div style="display:flex;justify-content:space-between; align-items: flex-start; margin-bottom:15px; border-bottom: 1px solid #f1f5f9; padding-bottom: 15px;">
                    <div class="task-info">
                        <div style="display:flex; align-items:center; gap: 10px; margin-bottom: 5px;">
                            <h4 style="margin:0; color:#1e293b; font-size: 20px;">${t.scheme_name}</h4>
                            ${pendingAlert}
                        </div>
                        <p style="margin: 3px 0; color:#64748b; font-size: 13px;"><strong>Tracking ID:</strong> #SRT-${(t.task_id||'').substring(0,8).toUpperCase()}</p>
                    </div>
                    <div style="display:flex;gap:8px;align-items:flex-start;">
                        ${status === 'Submitted'
                            ? `<button class="btn-ghost prog-btn" data-id="${t.task_id}" style="font-size:12px; border: 1px solid #16a34a; color: #16a34a; background:#dcfce7;" onclick="updateTaskStatus('${t.task_id}', 'Approved')">✅ Approve</button>` : ''}
                        ${(status === 'Completed' || status === 'Approved')
                            ? `<button class="btn-primary" style="font-size:12px; background: #f59e0b; border:none;" onclick="openRatingModal('${t.task_id}', '${t.assistant_name.replace(/'/g, "\'")}')">⭐ Rate Feedback</button>` : ''}
                    </div>
                </div>
                
                <!-- Timeline view -->
                <div class="tracking-wrapper" style="position:relative;display:flex;justify-content:space-between;padding-top:20px; padding-bottom: 10px; margin-bottom: 20px; background: #f8fafc; border-radius: 12px; padding-left: 20px; padding-right: 20px;">
                    <div style="position:absolute;top:32px;left:40px;right:40px;height:4px;background:#e2e8f0;border-radius:4px;"></div>
                    <div style="position:absolute;top:32px;left:40px;height:4px;background:#16a34a;border-radius:4px;transition:width 0.8s;width:calc(${progressWidth} - 60px);"></div>
                    ${['Started','Docs Verified','Assigned','Submitted','Approved'].map((label, i) => {
                        const classes = [s2,s3,s4,s5];
                        const cls = i === 0 ? 'completed' : (classes[i-1] || '');
                        return `<div class="track-step ${cls}" style="text-align:center;z-index:2; position: relative;">
                            <div class="track-icon" style="width:28px;height:28px;border-radius:50%;background:${cls==='completed'?'#16a34a':cls==='active'?'#f59e0b':'#e2e8f0'};color:${cls===''?'#94a3b8':'white'};display:flex;align-items:center;justify-content:center;font-size:12px;margin:0 auto 8px; border: 2px solid white; box-shadow: 0 0 0 2px ${cls==='completed'?'#16a34a':cls==='active'?'#f59e0b':'transparent'};">${cls==='completed'?'✓':cls==='active'?'●':(i+1)}</div>
                            <div class="track-label" style="font-size:12px; font-weight: 600; color:${cls==='completed'?'#1e293b':'#64748b'};">${label}</div>
                        </div>`;
                    }).join('')}
                </div>

                
                <!-- Applicant Details -->
                <div style="display:flex; gap: 20px; background: #f8fafc; padding: 15px 20px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #e2e8f0; align-items: center;">
                    <div style="font-size: 40px;">📝</div>
                    <div style="flex: 1;">
                        <h5 style="margin: 0; font-size: 14px; color: #334155;">Applicant Status Report</h5>
                        <p style="margin: 3px 0 0 0; font-size: 13px; color: #64748b;">
                            <strong>State:</strong> ${(t.user_profile && t.user_profile.state) || 'Karnataka'} | 
                            <strong>Income:</strong> ${(t.user_profile && t.user_profile.income) || '< ₹2.5L'} | 
                            <strong>Gender:</strong> ${(t.user_profile && t.user_profile.gender) || 'Not specified'}
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; font-size: 11px; color: #64748b; font-weight: bold;">DOCUMENTS SUBMITTED</p>
                        <p style="margin: 3px 0 0 0; font-size: 13px; color: #16a34a; font-weight: bold;">Aadhaar, PAN, Income Cert</p>
                    </div>
                </div>

                <!-- Assistant Info Card -->
                <div style="display:flex; gap: 20px; background: #eff6ff; padding: 15px 20px; border-radius: 12px; align-items: center;">
                    <div style="font-size: 40px;">👨🏽‍💼</div>
                    <div style="flex: 1;">
                        <h5 style="margin: 0; font-size: 15px; color: #1e3a8a;">Assigned Assistant: ${t.assistant_name}</h5>
                        <p style="margin: 3px 0 0 0; font-size: 12px; color: #3b82f6;">⭐ 4.9 | Speaks: ${t.language}</p>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; font-size: 11px; color: #64748b; font-weight: bold;">CURRENT ACTIVITY</p>
                        <p style="margin: 3px 0 0 0; font-size: 13px; color: #1d4ed8; font-weight: bold;">${status === 'Started' ? 'Waiting for Documents' : status === 'Docs Verified' ? 'Reviewing Documents' : status === 'Assigned' ? 'Filling Government Form' : status === 'Submitted' ? 'Waiting for Gov Approval' : 'Workflow Finished'}</p>
                    </div>
                </div>
            </div>`;
        });
        container.innerHTML = html;

        container.querySelectorAll('.prog-btn').forEach(btn => {
            btn.addEventListener('click', () => updateTaskStatus(btn.dataset.id, 'In Progress'));
        });
        container.querySelectorAll('.comp-btn').forEach(btn => {
            btn.addEventListener('click', () => updateTaskStatus(btn.dataset.id, 'Completed'));
        });
    }

    async function updateTaskStatus(taskId, status) {
        try {
            await fetch('/api/tasks/update', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify({ task_id: taskId, status })
            });
            loadTasks();
        } catch(e) { console.error(e); }
    }

    // Auto-poll dashboard every 5 seconds
    loadTasks();
    setInterval(loadTasks, 5000);

    // ── Scheme Details Modal close ────────────────────────────
    const closeSchemeModal = document.querySelector('#schemeDetailsModal .close-btn');
    if (closeSchemeModal) {
        closeSchemeModal.addEventListener('click', () => closeModal('schemeDetailsModal'));
    }

    // ── Floating Chat Widget ──────────────────────────────────
    const floatingChatBtn = document.getElementById('floatingChatBtn');
    const chatWidget      = document.getElementById('chatWidget');
    const closeChatBtn    = document.getElementById('closeChatBtn');
    const chatInput       = document.getElementById('chatInput');
    const sendChatBtn     = document.getElementById('sendChatBtn');
    const chatMessages    = document.getElementById('chatMessages');
    const voiceChatBtn    = document.getElementById('voiceChatBtn');

    if (floatingChatBtn) {
        floatingChatBtn.addEventListener('click', () => {
            chatWidget?.classList.remove('hidden');
            floatingChatBtn.style.display = 'none';
        });
    }
    if (closeChatBtn) {
        closeChatBtn.addEventListener('click', () => {
            chatWidget?.classList.add('hidden');
            if (floatingChatBtn) floatingChatBtn.style.display = 'flex';
        });
    }

    function addChatBubble(text, isUser) {
        if (!chatMessages) return;
        const div = document.createElement('div');
        div.style.cssText = `padding:10px 14px;border-radius:14px;max-width:82%;font-size:13px;
            align-self:${isUser ? 'flex-end' : 'flex-start'};
            background:${isUser ? 'var(--primary-blue, #1e40af)' : 'white'};
            color:${isUser ? 'white' : '#333'};
            border:1px solid ${isUser ? 'transparent' : '#eee'};`;
        div.innerText = text;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return div;
    }

    async function sendChat() {
        const text = chatInput?.value?.trim();
        if (!text) return;

        addChatBubble(text, true);
        chatInput.value = '';

        // Also trigger scheme search
        const qEl = document.getElementById('userQuery');
        if (qEl) qEl.value = text;
        setTimeout(() => document.getElementById('searchBtn')?.click(), 300);

        const loadingMsg = addChatBubble('Finding best schemes for you...', false);

        try {
            const res  = await fetch('/api/chat', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify({ prompt: text })
            });
            const data = await res.json();
            if (loadingMsg) loadingMsg.innerText = data.reply || 'Schemes loaded! See results below.';
        } catch(e) {
            if (loadingMsg) loadingMsg.innerText = 'Schemes are loading in the main dashboard!';
        }
    }

    if (sendChatBtn) sendChatBtn.addEventListener('click', sendChat);
    if (chatInput)   chatInput.addEventListener('keypress', e => { if (e.key === 'Enter') sendChat(); });

    // Voice recognition
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SR && voiceChatBtn) {
        const recognition = new SR();
        recognition.continuous    = false;
        recognition.interimResults= false;
        voiceChatBtn.addEventListener('click', () => {
            const lang = document.getElementById('p_language')?.value || 'English';
            const map  = { English:'en-IN', Hindi:'hi-IN', Kannada:'kn-IN', Tamil:'ta-IN',
                           Telugu:'te-IN', Marathi:'mr-IN', Bengali:'bn-IN' };
            recognition.lang = map[lang] || 'en-IN';
            recognition.start();
            voiceChatBtn.innerText = '🔴';
        });
        recognition.onresult = e => {
            if (chatInput) chatInput.value = e.results[0][0].transcript;
            voiceChatBtn.innerText = '🎤';
            sendChat();
        };
        recognition.onerror = () => { voiceChatBtn.innerText = '🎤'; };
    }

});

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
                
                alert(`✅ Application Submitted Successfully!\nTracking ID: ${d.task_id}\n\nYou can track this application in the Admin Dashboard and rate the workflow once approved.`);
                
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

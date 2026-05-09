import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

load_old = """        try {
            const res  = await fetch('/api/tasks');
            tasks = await res.json();
        } catch(e) {
            container.innerHTML = '<p class="text-muted">Could not load tasks. Check backend.</p>';
            return;
        }"""

load_new = """        try {
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
        }"""

js = js.replace(load_old, load_new)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated loadTasks to correctly filter tasks.")

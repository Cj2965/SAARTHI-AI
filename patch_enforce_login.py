import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

load_old = """        // FILTER: If normal user, only show their tasks
        if (window.currentUserEmail && window.currentUserEmail !== 'admin@saarthi.ai') {
            tasks = tasks.filter(t => t.user_profile && t.user_profile.email === window.currentUserEmail);
        }"""

load_new = """        // FILTER: If normal user, only show their tasks
        if (!window.currentUserEmail) {
            const container = document.getElementById('tasksContainer');
            container.innerHTML = `<div style="text-align:center; padding:40px;"><div style="font-size:40px; margin-bottom:10px;">🔒</div><h3 style="color:#1e3a8a; margin:0 0 10px 0;">Please Login</h3><p style="color:#64748b; margin:0 0 20px 0;">You must be logged in to track your applications.</p><button class="btn-primary" onclick="closeSmallModal('dashboardModal'); document.getElementById('loginNavBtn').click();" style="padding: 10px 25px;">Login Now</button></div>`;
            return;
        } else if (window.currentUserEmail !== 'admin@saarthi.ai') {
            tasks = tasks.filter(t => t.user_profile && t.user_profile.email === window.currentUserEmail);
        }"""

js = js.replace(load_old, load_new)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated loadTasks to enforce login")


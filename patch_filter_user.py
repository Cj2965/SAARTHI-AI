import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update login to store window.currentUserEmail
login_old = """        if (email.value === 'admin@saarthi.ai' && pass.value === 'admin123') {
            alert('Welcome Admin! You now have access to the Admin Dashboard.');
            document.getElementById('dashboardNavBtn').style.display = 'inline-block';
            document.getElementById('userProfileIcon').style.display = 'flex';
            document.getElementById('userProfileName').innerText = 'Admin';
        } else {
            alert(`Successfully ${authMode === 'login' ? 'logged in' : 'registered'} as ${email.value}!`);
            document.getElementById('dashboardNavBtn').style.display = 'none'; 
            document.getElementById('userProfileIcon').style.display = 'flex';
            document.getElementById('userProfileName').innerText = email.value.split('@')[0];
        }"""

login_new = """        if (email.value === 'admin@saarthi.ai' && pass.value === 'admin123') {
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
        }"""

js = js.replace(login_old, login_new)

# 2. Update submit application logic to append email
submit_old = """                user_profile: window.currentUserProfile || {},
                opportunity: window.currentOpp || {}"""

submit_new = """                user_profile: { ...(window.currentUserProfile || {}), email: window.currentUserEmail || 'guest@saarthi.ai' },
                opportunity: window.currentOpp || {}"""

js = js.replace(submit_old, submit_new)

# 3. Update loadTasks to filter by email if not admin
load_old = """        const res = await fetch('/api/tasks');
        const tasks = await res.json();
        
        const container = document.getElementById('tasksContainer');
        if (!tasks || tasks.length === 0) {"""

load_new = """        const res = await fetch('/api/tasks');
        let tasks = await res.json();
        
        // FILTER: If normal user, only show their tasks
        if (window.currentUserEmail && window.currentUserEmail !== 'admin@saarthi.ai') {
            tasks = tasks.filter(t => t.user_profile && t.user_profile.email === window.currentUserEmail);
        }
        
        const container = document.getElementById('tasksContainer');
        if (!tasks || tasks.length === 0) {"""

js = js.replace(load_old, load_new)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated app.js filtering and email logic.")


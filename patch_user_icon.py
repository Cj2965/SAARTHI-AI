import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add User Profile Icon to logo-area
old_logo_area = """        <div class="logo-area">
            <img src="img/logo.jpeg" alt="Saarthi AI" class="main-logo" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' viewBox=\\'0 0 100 100\\'><text y=\\'50\\' font-size=\\'40\\'>🦋</text></svg>'">
            <span class="logo-text"><span class="text-saffron">Saar</span><span class="text-blue">thi</span> AI</span>
        </div>"""

new_logo_area = """        <div class="logo-area" style="display: flex; align-items: center;">
            <img src="img/logo.jpeg" alt="Saarthi AI" class="main-logo" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' viewBox=\\'0 0 100 100\\'><text y=\\'50\\' font-size=\\'40\\'>🦋</text></svg>'">
            <span class="logo-text"><span class="text-saffron">Saar</span><span class="text-blue">thi</span> AI</span>
            <div id="userProfileIcon" style="display: none; align-items: center; gap: 8px; background: #e0f2fe; padding: 4px 12px; border-radius: 20px; font-weight: bold; color: #0369a1; margin-left: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid #bae6fd;">
                <span style="font-size: 18px;">👤</span><span id="userProfileName" style="font-size: 13px;">User</span>
            </div>
        </div>"""

text = text.replace(old_logo_area, new_logo_area)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(text)


with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update login logic to show profile icon and hide login/register buttons
old_login = """        if (email.value === 'admin@saarthi.ai' && pass.value === 'admin123') {
            alert('Welcome Admin! You now have access to the Admin Dashboard.');
            document.getElementById('dashboardNavBtn').style.display = 'inline-block';
        } else {
            alert(`Successfully ${authMode === 'login' ? 'logged in' : 'registered'} as ${email.value}!`);
            document.getElementById('dashboardNavBtn').style.display = 'none'; 
            // Normal users use the Track Applications button, which is always visible.
        }"""

new_login = """        if (email.value === 'admin@saarthi.ai' && pass.value === 'admin123') {
            alert('Welcome Admin! You now have access to the Admin Dashboard.');
            document.getElementById('dashboardNavBtn').style.display = 'inline-block';
            document.getElementById('userProfileIcon').style.display = 'flex';
            document.getElementById('userProfileName').innerText = 'Admin';
        } else {
            alert(`Successfully ${authMode === 'login' ? 'logged in' : 'registered'} as ${email.value}!`);
            document.getElementById('dashboardNavBtn').style.display = 'none'; 
            document.getElementById('userProfileIcon').style.display = 'flex';
            document.getElementById('userProfileName').innerText = email.value.split('@')[0];
        }
        document.getElementById('loginNavBtn').style.display = 'none';
        document.getElementById('registerNavBtn').style.display = 'none';"""

js = js.replace(old_login, new_login)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Added user profile icon and updated login logic.")

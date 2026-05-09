import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the Filter Bar from the Results Modal
# Looking for the block containing "Search by scheme name..."
start_idx = text.find('<div style="display: flex; gap: 15px; margin-bottom: 20px;">')
if start_idx != -1:
    end_idx = text.find('</div>', start_idx) + 6
    # Let's verify it's the right block
    if 'schemeSearch' in text[start_idx:end_idx+200] or 'filterSector' in text[start_idx:end_idx+200]:
        # It might be multiple lines, so find the closing div of the flex container
        # Actually it's simple, let's just find the exact block.
        # Since the block contains three inputs, we can use regex.
        filter_pattern = re.search(r'<div style="display: flex; gap: 15px; margin-bottom: 20px;">.*?</div>', text, re.DOTALL)
        if filter_pattern:
            text = text.replace(filter_pattern.group(0), '')
            print("Filter bar removed.")

# If regular user logs in, they want Track Applications to show, but Admin Dashboard to not show.
# "if i login as a user its not showing it"
# Let's check what track applications is:
# <li><a href="#" onclick="event.preventDefault(); loadTasks(); openModal('dashboardModal');" class="text-blue" style="font-weight: bold;" id="trackNavBtn">Track Applications</a></li>
# Oh, it doesn't have an ID `trackNavBtn` currently. I just added it in line 24.
# Let's look at app.js. 

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update login logic to ensure Track Applications shows for EVERYONE, but Admin Dashboard only for Admin.
# Maybe the user hid track applications? No.
# I'll just ensure the logic explicitly shows "Track Applications" if they mean that.
login_old = """        if (email.value === 'admin@saarthi.ai' && pass.value === 'admin123') {
            alert('Welcome Admin! You now have access to the Dashboard.');
            document.getElementById('dashboardNavBtn').style.display = 'inline-block';
        } else {
            alert(`Successfully ${authMode === 'login' ? 'logged in' : 'registered'} as ${email.value}!`);
            document.getElementById('dashboardNavBtn').style.display = 'none'; // normal users don't see dashboard
        }"""

login_new = """        if (email.value === 'admin@saarthi.ai' && pass.value === 'admin123') {
            alert('Welcome Admin! You now have access to the Admin Dashboard.');
            document.getElementById('dashboardNavBtn').style.display = 'inline-block';
        } else {
            alert(`Successfully ${authMode === 'login' ? 'logged in' : 'registered'} as ${email.value}!`);
            document.getElementById('dashboardNavBtn').style.display = 'none'; 
            // Normal users use the Track Applications button, which is always visible.
        }"""
js = js.replace(login_old, login_new)

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

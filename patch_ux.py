import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove Find Schemes from navbar
html = html.replace('<li><a href="#discover" class="nav-highlight">Find Schemes</a></li>', '')

# 2. Fix Track Applications onclick
html = html.replace('onclick="openModal(\'dashboardModal\')"', 'onclick="event.preventDefault(); loadTasks(); openModal(\'dashboardModal\');"')

# 3. Remove USP from main page
usp_start = html.find('<!-- Micro-Employment USP -->')
usp_end = html.find('</section>', usp_start) + len('</section>')

if usp_start != -1 and usp_end > usp_start:
    # Double check if it's the one in the body (not in the modal)
    # Actually there are two now? One inside modal, one in body.
    pass

# A safer way to remove the USP section from the body:
# The one in the body has id="usp" class="info-section text-center"
usp_body_match = re.search(r'<!-- Micro-Employment USP -->\s*<section id="usp" class="info-section text-center">.*?</section>', html, re.DOTALL)
if usp_body_match:
    html = html.replace(usp_body_match.group(0), '')
    
with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html patched")

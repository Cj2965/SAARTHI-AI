with open('frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

section = """
    <!-- 3 Ways to Discover -->
    <section id="discovery-methods" class="info-section">
        <div class="container text-center">
            <h2 class="section-title text-blue">Three Ways to Discover Schemes</h2>
            <p class="section-desc">Pick how you want to find the right government opportunity.</p>
            <div class="grid-3 mt-40">
                <div class="card hover-scale" onclick="openSmallModal('modalA')" style="padding:35px;cursor:pointer;background:rgba(255,255,255,0.88);display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:160px;">
                    <div style="font-size:40px;margin-bottom:12px;">&#128202;</div>
                    <h3 class="text-saffron" style="margin:0 0 8px 0;">Sector Search</h3>
                    <p class="text-muted" style="font-size:13px;">Browse by Education, Health, Agriculture...</p>
                </div>
                <div class="card hover-scale" onclick="openSmallModal('modalB')" style="padding:35px;cursor:pointer;background:rgba(255,255,255,0.88);display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:160px;">
                    <div style="font-size:40px;margin-bottom:12px;">&#128100;</div>
                    <h3 class="text-saffron" style="margin:0 0 8px 0;">Why Do You Need?</h3>
                    <p class="text-muted" style="font-size:13px;">Filter by State, Age, Gender, Caste...</p>
                </div>
                <div class="card hover-scale" onclick="document.getElementById('floatingChatBtn').click();" style="padding:35px;cursor:pointer;background:rgba(255,255,255,0.88);display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:160px;">
                    <div style="font-size:40px;margin-bottom:12px;">&#129302;</div>
                    <h3 class="text-saffron" style="margin:0 0 8px 0;">Talk with AI</h3>
                    <p class="text-muted" style="font-size:13px;">Just describe your need, AI finds schemes</p>
                </div>
            </div>
        </div>
    </section>
"""

marker = '    <!-- Micro-Employment USP -->\n    <section id="target"'
if marker in content:
    content = content.replace(marker, section + '    <!-- Micro-Employment USP -->\n    <section id="target"', 1)
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS: Discovery section restored!')
else:
    print('ERROR: marker not found')
    # print first 200 chars around likely location
    idx = content.find('Micro-Employment USP')
    print(repr(content[idx-10:idx+60]))

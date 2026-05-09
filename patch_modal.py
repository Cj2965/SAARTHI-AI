import re

# 1. Update index.html
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the results container
start_idx = html.find('<div id="resultsContainer"')
end_idx = html.find('</section>', start_idx)

if start_idx != -1 and end_idx != -1:
    results_html = html[start_idx:end_idx].strip()
    
    # Remove from original location
    html = html[:start_idx] + html[end_idx:]
    
    # Transform into a modal
    modal_html = f"""
    <!-- Results Modal -->
    <div id="resultsModal" class="modal hidden" style="align-items: flex-start; padding-top: 40px; z-index: 10002;">
        <div class="modal-card" style="width: 1100px; max-width: 95%; max-height: 85vh; overflow-y: auto; background: rgba(255, 255, 255, 0.97); backdrop-filter: blur(20px);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div>
                    <h2 style="margin:0; font-size:26px; color:#1d4ed8;">📋 Recommended Schemes</h2>
                    <p style="font-size: 13px; color: #475569; margin-top: 5px;">Based on your profile and search criteria</p>
                </div>
                <button onclick="closeSmallModal('resultsModal')" style="background:none; border:none; font-size:30px; cursor:pointer; color:#475569;">&times;</button>
            </div>
            
            <!-- Filters Bar -->
            <div class="dashboard-filters" style="display: flex; gap: 10px; justify-content: flex-start; margin-bottom: 20px; flex-wrap: wrap;">
                <input type="text" id="schemeSearch" placeholder="Search scheme by name..." style="padding: 8px 15px; border-radius: 8px; border: 1px solid #ddd; flex: 1;">
                <select id="filterSector" style="padding: 8px 15px; border-radius: 8px; border: 1px solid #ddd;">
                    <option value="">All Sectors</option>
                    <option value="Agriculture">Agriculture</option>
                    <option value="Finance & Business">Finance & Business</option>
                    <option value="Education & Jobs">Education & Jobs</option>
                    <option value="Health">Health</option>
                </select>
                <select id="sortSchemes" style="padding: 8px 15px; border-radius: 8px; border: 1px solid #ddd;">
                    <option value="match">Sort by: Match Score</option>
                    <option value="deadline">Sort by: Deadline</option>
                    <option value="newest">Sort by: Newest</option>
                </select>
            </div>

            <div id="loadingSpinner" class="loading-state hidden">
                <div class="spinner"></div>
                <p>AI is finding the best schemes for you...</p>
            </div>
            
            <div id="cardsWrapper" class="recommendations-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px;"></div>
            
            <div id="emptyState" class="hidden text-center mt-20" style="padding: 40px; background: rgba(255,255,255,0.8); border-radius: 12px;">
                <p>No matching schemes found. Try a broader search.</p>
            </div>
        </div>
    </div>
"""
    # Insert modal before Scheme Details Modal
    target_idx = html.find('<!-- Scheme Details Modal -->')
    html = html[:target_idx] + modal_html + '\n' + html[target_idx:]
    
    with open('frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html with resultsModal")

# 2. Update app.js
with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace inline showing logic with modal logic
old_search_logic = """        // Pre-fill main discover form
        const qEl = document.getElementById('userQuery');
        if (qEl) qEl.value = query;
        if (state) { const sEl = document.getElementById('p_state'); if(sEl) sEl.value = state; }
        if (gender){ const gEl = document.getElementById('p_gender'); if(gEl) gEl.value = gender; }
        if (age)   { const aEl = document.getElementById('p_age');    if(aEl) aEl.value = age; }

        closeModal('modalB');
        document.getElementById('discover')?.scrollIntoView({ behavior: 'smooth' });
        setTimeout(() => document.getElementById('searchBtn')?.click(), 400);"""

new_search_logic = """        // Pre-fill main discover form
        const qEl = document.getElementById('userQuery');
        if (qEl) qEl.value = query;
        if (state) { const sEl = document.getElementById('p_state'); if(sEl) sEl.value = state; }
        if (gender){ const gEl = document.getElementById('p_gender'); if(gEl) gEl.value = gender; }
        if (age)   { const aEl = document.getElementById('p_age');    if(aEl) aEl.value = age; }

        closeModal('modalB');
        // Instantly trigger search (which now opens resultsModal)
        setTimeout(() => document.getElementById('searchBtn')?.click(), 200);"""

js = js.replace(old_search_logic, new_search_logic)

old_sector_logic = """    // ── Sector Search helper ──────────────────────────────────
    window.searchBySector = function(sector) {
        closeModal('modalA');
        const qEl = document.getElementById('userQuery');
        if (qEl) qEl.value = 'Show me schemes for ' + sector;
        document.getElementById('discover')?.scrollIntoView({ behavior: 'smooth' });
        setTimeout(() => document.getElementById('searchBtn')?.click(), 400);
    };"""

new_sector_logic = """    // ── Sector Search helper ──────────────────────────────────
    window.searchBySector = function(sector) {
        closeModal('modalA');
        const qEl = document.getElementById('userQuery');
        if (qEl) qEl.value = 'Show me schemes for ' + sector;
        setTimeout(() => document.getElementById('searchBtn')?.click(), 200);
    };"""

js = js.replace(old_sector_logic, new_sector_logic)

old_btn_logic = """            const origText = searchBtn.innerText;
            searchBtn.innerText = 'Analyzing...';
            searchBtn.disabled = true;

            document.getElementById('resultsContainer')?.classList.remove('hidden');
            document.getElementById('loadingSpinner')?.classList.remove('hidden');
            const wrapper = document.getElementById('cardsWrapper');"""

new_btn_logic = """            const origText = searchBtn.innerText;
            searchBtn.innerText = 'Analyzing...';
            searchBtn.disabled = true;

            openModal('resultsModal');
            document.getElementById('loadingSpinner')?.classList.remove('hidden');
            const wrapper = document.getElementById('cardsWrapper');"""

js = js.replace(old_btn_logic, new_btn_logic)

# Chat widget search trigger logic
old_chat_trigger = """        // Also trigger scheme search
        const qEl = document.getElementById('userQuery');
        if (qEl) qEl.value = text;
        document.getElementById('discover')?.scrollIntoView({ behavior: 'smooth' });
        setTimeout(() => document.getElementById('searchBtn')?.click(), 500);"""

new_chat_trigger = """        // Also trigger scheme search
        const qEl = document.getElementById('userQuery');
        if (qEl) qEl.value = text;
        setTimeout(() => document.getElementById('searchBtn')?.click(), 300);"""

js = js.replace(old_chat_trigger, new_chat_trigger)


with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated app.js successfully")

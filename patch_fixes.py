import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update schemeDetailsModal z-index and back button
old_sd_modal = """<!-- Scheme Details Modal -->
    <div id="schemeDetailsModal" class="modal hidden" style="align-items: flex-start; padding-top: 40px;">
        <div class="modal-card" style="width: 800px; max-width: 95%; max-height: 85vh; overflow-y: auto; background: rgba(255, 255, 255, 0.98);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                <div>
                    <h2 id="sd-name" class="text-blue m-0" style="font-size: 24px;">Scheme Name</h2>
                    <span id="sd-sector" class="badge-partial mt-10" style="display: inline-block;">Sector</span>
                </div>
                <button class="close-btn" style="background: none; border: none; font-size: 32px; color: #333; cursor: pointer;">&times;</button>
            </div>"""

new_sd_modal = """<!-- Scheme Details Modal -->
    <div id="schemeDetailsModal" class="modal hidden" style="align-items: flex-start; padding-top: 40px; z-index: 10015;">
        <div class="modal-card" style="width: 800px; max-width: 95%; max-height: 85vh; overflow-y: auto; background: rgba(255, 255, 255, 0.98);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                <div>
                    <h2 id="sd-name" class="text-blue m-0" style="font-size: 24px;">Scheme Name</h2>
                    <span id="sd-sector" class="badge-partial mt-10" style="display: inline-block;">Sector</span>
                </div>
                <button class="close-btn" style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 8px; padding: 8px 15px; font-size: 14px; color: #334155; cursor: pointer; display: flex; align-items: center; gap: 5px; font-weight: bold;">&#128281; Back</button>
            </div>"""

html = html.replace(old_sd_modal, new_sd_modal)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html schemeDetailsModal")

# 2. Update app.js
with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make renderResults handle filtering
old_render = """    function renderResults(results, userProfile) {
        const wrapper = document.getElementById('cardsWrapper');
        if (!wrapper) return;
        wrapper.innerHTML = '';

        if (!results || results.length === 0) {
            document.getElementById('emptyState')?.classList.remove('hidden');
            return;
        }
        document.getElementById('emptyState')?.classList.add('hidden');

        results.forEach((item, index) => {"""

new_render = """    function renderResults(results, userProfile) {
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

        filteredResults.forEach((item, index) => {"""

js = js.replace(old_render, new_render)

# Add event listeners for the filters
filter_listeners = """
    // ── Filter Listeners ───────────────────────────────
    document.getElementById('schemeSearch')?.addEventListener('input', () => renderResults());
    document.getElementById('filterSector')?.addEventListener('change', () => renderResults());
    document.getElementById('sortSchemes')?.addEventListener('change', () => renderResults());
"""
if 'filterSector' not in js.split('── Filter Listeners')[0] and 'filterSector' not in js.split('// ── Scheme Details Modal close')[0]: # Just to ensure not duplicated roughly
    js += filter_listeners

with open('frontend/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated app.js with filters")

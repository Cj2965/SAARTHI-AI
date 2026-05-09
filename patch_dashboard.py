import re

# 1. Update index.html
with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix 'Who We Serve' Background
html = html.replace('class="info-section bg-blue text-white"', 'class="info-section bg-transparent text-dark"')
html = html.replace('class="section-desc text-white-muted mb-40"', 'class="section-desc text-muted mb-40"')

# Fix schemeDetailsModal Z-index and Back button
# I will use Regex because the exact string might have changed slightly
sd_pattern = r'(<div id="schemeDetailsModal" class="modal hidden"[^>]*>)\s*<div class="modal-card"[^>]*>\s*<div style="[^"]*">\s*<div>\s*<h2 id="sd-name"[^>]*>Scheme Name</h2>\s*<span id="sd-sector"[^>]*>Sector</span>\s*</div>\s*<button class="close-btn"[^>]*>&times;</button>'

sd_replacement = r"""\1
        <div class="modal-card" style="width: 800px; max-width: 95%; max-height: 85vh; overflow-y: auto; background: rgba(255, 255, 255, 0.98);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                <div>
                    <h2 id="sd-name" class="text-blue m-0" style="font-size: 24px;">Scheme Name</h2>
                    <span id="sd-sector" class="badge-partial mt-10" style="display: inline-block;">Sector</span>
                </div>
                <button class="close-btn" onclick="closeSmallModal('schemeDetailsModal')" style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 8px; padding: 8px 15px; font-size: 14px; color: #334155; cursor: pointer; display: flex; align-items: center; gap: 5px; font-weight: bold;">&#128281; Back</button>
"""
if '<button class="close-btn" onclick="closeSmallModal(\'schemeDetailsModal\')"' not in html:
    html = re.sub(sd_pattern, sd_replacement, html)
    # Also fix z-index for schemeDetailsModal specifically
    html = re.sub(r'(id="schemeDetailsModal" class="modal hidden" style="[^"]*)(")', r'\1 z-index: 10015;\2', html)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html")

# 2. Update app.js Dashboard Rendering for Rich UI
with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_dashboard_start = """            html += `
            <div class="task-item">
                <div style="display:flex;justify-content:space-between;margin-bottom:15px;">
                    <div class="task-info">
                        <h4>${t.scheme_name}</h4>"""

old_dashboard_end = """                        const cls = i === 0 ? 'completed' : (classes[i-1] || '');
                        return `<div class="track-step ${cls}" style="text-align:center;z-index:2;">
                            <div class="track-icon" style="width:28px;height:28px;border-radius:50%;background:${cls==='completed'?'#16a34a':cls==='active'?'#f59e0b':'#e5e7eb'};color:white;display:flex;align-items:center;justify-content:center;font-size:12px;margin:0 auto 6px;">${cls==='completed'?'✓':cls==='active'?'●':'○'}</div>
                            <div class="track-label" style="font-size:11px;">${label}</div>
                        </div>`;
                    }).join('')}
                </div>
            </div>`;
        });"""

new_dashboard = """            
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
                            ? `<button class="btn-primary" style="font-size:12px; background: #f59e0b; border:none;" onclick="openRatingModal('${t.task_id}', '${t.assistant_name.replace(/'/g, "\\'")}')">⭐ Rate Feedback</button>` : ''}
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
        });"""

start_idx = js.find('            html += `\n            <div class="task-item">')
end_idx = js.find('                </div>\n            </div>`;\n        });') + len('                </div>\n            </div>`;\n        });')

if start_idx != -1 and end_idx != -1:
    js = js[:start_idx] + new_dashboard + js[end_idx:]
    with open('frontend/app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Updated app.js Dashboard")
else:
    print("Could not find dashboard HTML block in app.js")


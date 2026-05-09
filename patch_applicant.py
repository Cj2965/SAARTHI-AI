import re

with open('frontend/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

applicant_details = """
                <!-- Applicant Details -->
                <div style="display:flex; gap: 20px; background: #f8fafc; padding: 15px 20px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #e2e8f0; align-items: center;">
                    <div style="font-size: 40px;">📝</div>
                    <div style="flex: 1;">
                        <h5 style="margin: 0; font-size: 14px; color: #334155;">Applicant Status Report</h5>
                        <p style="margin: 3px 0 0 0; font-size: 13px; color: #64748b;">
                            <strong>State:</strong> ${(t.user_profile && t.user_profile.state) || 'Karnataka'} | 
                            <strong>Income:</strong> ${(t.user_profile && t.user_profile.income) || '< ₹2.5L'} | 
                            <strong>Gender:</strong> ${(t.user_profile && t.user_profile.gender) || 'Not specified'}
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <p style="margin: 0; font-size: 11px; color: #64748b; font-weight: bold;">DOCUMENTS SUBMITTED</p>
                        <p style="margin: 3px 0 0 0; font-size: 13px; color: #16a34a; font-weight: bold;">Aadhaar, PAN, Income Cert</p>
                    </div>
                </div>

                <!-- Assistant Info Card -->"""

if 'Applicant Status Report' not in js:
    js = js.replace('<!-- Assistant Info Card -->', applicant_details)
    with open('frontend/app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Updated app.js with Applicant Details")
else:
    print("Already updated")

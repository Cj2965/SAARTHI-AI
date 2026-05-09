import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find microEmploymentModal and replace its contents
pattern = r'(<div id="microEmploymentModal".*?<div style="padding: 20px;">).*?(</div>\s*</div>\s*</div>\s*<!-- Floating Chat Widget)'

new_content = r"""\1
                <div style="text-align: center; margin-bottom: 30px;">
                    <div style="font-size: 50px; margin-bottom: 10px;">💡</div>
                    <h2 style="color: #1e3a8a; margin: 0 0 10px 0;">Become a Saarthi Assistant</h2>
                    <p style="color: #64748b; max-width: 600px; margin: 0 auto;">Saarthi helps citizens access life-changing government opportunities while creating massive digital employment for tech-savvy youths in rural and urban areas.</p>
                </div>
                
                <h3 style="color: #ea580c; border-bottom: 2px solid #fdba74; padding-bottom: 10px; margin-bottom: 20px;">How You Can Help & Earn</h3>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px;">
                    <div style="background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0;">
                        <h4 style="color: #1d4ed8; margin-top: 0;">1. Smart Matching</h4>
                        <p style="font-size: 14px; color: #475569;">When a citizen needs help applying for a scheme, Saarthi AI automatically routes the request to you based on your location and language skills.</p>
                    </div>
                    <div style="background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0;">
                        <h4 style="color: #1d4ed8; margin-top: 0;">2. Document Verification</h4>
                        <p style="font-size: 14px; color: #475569;">You securely review the uploaded documents (Aadhaar, PAN, Income Cert) using our built-in Digilocker tools and ensure they are clear and valid.</p>
                    </div>
                    <div style="background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0;">
                        <h4 style="color: #1d4ed8; margin-top: 0;">3. Form Filling</h4>
                        <p style="font-size: 14px; color: #475569;">You guide the applicant through complex government portals, filling out forms securely on their behalf using our AI auto-fill assistant.</p>
                    </div>
                    <div style="background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0;">
                        <h4 style="color: #1d4ed8; margin-top: 0;">4. Earn Instantly</h4>
                        <p style="font-size: 14px; color: #475569;">Once the application is successfully submitted and approved by the citizen, your wallet is instantly credited!</p>
                    </div>
                </div>

                <div style="background: #fffbeb; border: 1px solid #fde68a; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
                    <h4 style="color: #b45309; margin: 0 0 15px 0;">💰 Transparent Revenue Split Example</h4>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="text-align: center; flex: 1;">
                            <span style="display: block; font-size: 24px; font-weight: bold; color: #1e293b;">₹50</span>
                            <span style="font-size: 12px; color: #64748b;">User Pays</span>
                        </div>
                        <div style="font-size: 24px; color: #cbd5e1;">➔</div>
                        <div style="text-align: center; flex: 1; background: #dcfce7; padding: 10px; border-radius: 8px;">
                            <span style="display: block; font-size: 24px; font-weight: bold; color: #16a34a;">₹35</span>
                            <span style="font-size: 12px; color: #16a34a;">You Earn (Instant)</span>
                        </div>
                        <div style="font-size: 24px; color: #cbd5e1;">+</div>
                        <div style="text-align: center; flex: 1;">
                            <span style="display: block; font-size: 24px; font-weight: bold; color: #94a3b8;">₹15</span>
                            <span style="font-size: 12px; color: #64748b;">Platform Fee</span>
                        </div>
                    </div>
                </div>

                <div style="text-align: center; margin-top: 30px;">
                    <button class="btn-primary" style="font-size: 16px; padding: 12px 30px;" onclick="closeSmallModal('microEmploymentModal'); document.getElementById('registerNavBtn').click();">Register as an Assistant Today</button>
                </div>
\2"""

text = re.sub(pattern, new_content, text, flags=re.DOTALL)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated microEmploymentModal with detailed agent guide.")

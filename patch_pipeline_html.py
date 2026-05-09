import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

modals_to_add = """
    <!-- Application Pipeline Modal -->
    <div id="pipelineModal" class="modal hidden" style="z-index: 10010; align-items: flex-start; padding-top: 20px;">
        <div class="modal-card" style="width: 800px; max-width: 95%; max-height: 90vh; overflow-y: auto; background: #fff; border-radius: 20px;">
            <!-- Header -->
            <div style="background: linear-gradient(to right, #1e40af, #3b82f6); padding: 20px 30px; color: white; display: flex; justify-content: space-between; border-radius: 20px 20px 0 0;">
                <h2 style="margin: 0; font-size: 20px;">Application Pipeline: <span id="pipeSchemeName"></span></h2>
                <button onclick="closeSmallModal('pipelineModal')" style="background: none; border: none; color: white; font-size: 28px; cursor: pointer;">&times;</button>
            </div>
            
            <div style="padding: 30px;">
                <!-- Step 1: Document Upload & Verification -->
                <div id="pipeStep1">
                    <h3 style="color: #1e3a8a;">Step 1: Document Upload & OCR Verification</h3>
                    <p class="text-muted" style="margin-bottom: 20px; font-size: 14px;">Upload the required documents. Our system will extract text and verify details.</p>
                    <div style="display: flex; gap: 15px;">
                        <div style="flex: 1; border: 2px dashed #cbd5e1; padding: 20px; text-align: center; border-radius: 12px; cursor: pointer;" onclick="simulateFileUpload('aadhaar', this)">
                            <span style="font-size: 30px;">📄</span><br>Upload Aadhaar
                            <div class="upload-status" style="font-size: 12px; color: #64748b; margin-top: 5px;">Click to upload</div>
                        </div>
                        <div style="flex: 1; border: 2px dashed #cbd5e1; padding: 20px; text-align: center; border-radius: 12px; cursor: pointer;" onclick="simulateFileUpload('pan', this)">
                            <span style="font-size: 30px;">💳</span><br>Upload PAN
                            <div class="upload-status" style="font-size: 12px; color: #64748b; margin-top: 5px;">Click to upload</div>
                        </div>
                        <div style="flex: 1; border: 2px dashed #cbd5e1; padding: 20px; text-align: center; border-radius: 12px; cursor: pointer;" onclick="simulateFileUpload('income', this)">
                            <span style="font-size: 30px;">📜</span><br>Income Cert
                            <div class="upload-status" style="font-size: 12px; color: #64748b; margin-top: 5px;">Click to upload</div>
                        </div>
                    </div>
                    
                    <div id="ocrLoading" class="hidden" style="margin-top: 30px; text-align: center;">
                        <div class="spinner" style="margin: 0 auto; border-top-color: #1e40af;"></div>
                        <p style="margin-top: 10px; color: #1e40af; font-weight: bold;">OCR Extracting Text & Detecting Quality...</p>
                    </div>
                    
                    <div id="ocrResults" class="hidden" style="margin-top: 25px; padding: 20px; background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0;">
                        <h4 style="margin-bottom: 15px;">System Verification Results</h4>
                        <ul style="list-style: none; padding: 0; font-size: 14px; line-height: 1.8;">
                            <li style="color: #16a34a;">✅ <strong>Aadhaar:</strong> Verified (Data match: 98%)</li>
                            <li style="color: #d97706;">⚠️ <strong>PAN:</strong> Blurry upload detected. Will require manual assistant verification.</li>
                            <li style="color: #16a34a;">✅ <strong>Income Cert:</strong> Valid text extracted (Below ₹2.5L)</li>
                            <li style="color: #b91c1c;">⚠️ <strong>Bank Passbook:</strong> Missing upload.</li>
                        </ul>
                        <button class="btn-primary w-100 mt-20" onclick="nextPipeStep(2)">Proceed to Eligibility Check</button>
                    </div>
                </div>

                <!-- Step 2: Rule-based Eligibility Check -->
                <div id="pipeStep2" class="hidden">
                    <h3 style="color: #1e3a8a;">Step 2: Deterministic Eligibility Check</h3>
                    <p style="font-size: 14px; margin-bottom: 20px;">System is applying hard-coded rule-based logic to verify qualification...</p>
                    <div style="background: #eff6ff; padding: 20px; border-radius: 12px; border-left: 5px solid #3b82f6;">
                        <ul style="list-style: none; padding: 0; line-height: 2; font-size: 14px;">
                            <li>✅ <strong>Age Check:</strong> Profile age (>18) matches scheme rule.</li>
                            <li>✅ <strong>Income Limit:</strong> OCR Income (< ₹2.5L) meets requirement.</li>
                            <li>⚠️ <strong>Document Status:</strong> Missing Bank Passbook & Blurry PAN allowed for conditional proceeding.</li>
                        </ul>
                        <div style="margin-top: 15px; padding: 10px; background: #dcfce7; color: #16a34a; border-radius: 8px; font-weight: bold; text-align: center;">Result: ELIGIBLE</div>
                    </div>
                    <button class="btn-primary w-100 mt-20" onclick="nextPipeStep(3)">Proceed to Application Mode</button>
                </div>

                <!-- Step 3: Marketplace -->
                <div id="pipeStep3" class="hidden">
                    <h3 style="color: #1e3a8a;">Step 3: Application Mode Marketplace</h3>
                    <p style="font-size: 14px; margin-bottom: 20px;">Choose how you want to complete the government forms.</p>
                    <div style="display: flex; gap: 20px;">
                        <div style="flex: 1; border: 1px solid #e2e8f0; border-radius: 12px; padding: 25px; text-align: center; cursor: pointer; transition: all 0.3s;" class="hover-scale" onclick="nextPipeStep(4, 'self')">
                            <div style="font-size: 40px; margin-bottom: 10px;">✍️</div>
                            <h4 style="color: #334155;">Self Apply</h4>
                            <p style="font-size: 13px; color: #64748b; margin-top: 10px;">Free. Fill the complex government forms yourself.</p>
                        </div>
                        <div style="flex: 1; border: 2px solid #3b82f6; border-radius: 12px; padding: 25px; text-align: center; cursor: pointer; background: #eff6ff; transition: all 0.3s;" class="hover-scale" onclick="nextPipeStep(4, 'assistant')">
                            <div style="font-size: 40px; margin-bottom: 10px;">👨‍💼</div>
                            <h4 style="color: #1d4ed8;">Request Assistant</h4>
                            <p style="font-size: 13px; color: #64748b; margin-top: 10px;">₹50 Fee. Smart matching assigns best local expert based on language, rating, and availability.</p>
                        </div>
                    </div>
                </div>

                <!-- Step 4: Form Workflow & AI Recheck -->
                <div id="pipeStep4" class="hidden">
                    <h3 id="formModeTitle" style="color: #1e3a8a;">Step 4: Form Workflow</h3>
                    
                    <div id="assistantMatchBlock" class="hidden" style="margin-bottom: 20px; padding: 15px; background: #f0fdf4; border-radius: 10px; border: 1px solid #bbf7d0;">
                        <strong style="color: #16a34a; font-size: 15px;">✅ Assistant Automatically Matched!</strong><br>
                        <div style="display: flex; align-items: center; gap: 10px; margin-top: 10px;">
                            <div style="font-size: 30px;">👨🏽‍💼</div>
                            <div>
                                <strong>Rajesh K.</strong> (Speaks: Kannada, English)<br>
                                <span style="font-size: 12px; color: #64748b;">Rating: ⭐⭐⭐⭐⭐ (4.9) | Expertise: Govt Loans</span>
                            </div>
                        </div>
                        <p style="font-size: 12px; color: #16a34a; margin-top: 10px;">Rajesh is now assisting you. He will verify your blurry PAN card and fill the form.</p>
                    </div>

                    <div style="border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; background: #f8fafc;">
                        <h4 style="margin-bottom: 15px;">Application Draft (Filled)</h4>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                            <div><label style="font-size: 12px; color: #64748b;">Applicant Name</label><input type="text" value="Raj Kumar" disabled style="width:100%; padding: 8px; border-radius: 6px; border: 1px solid #cbd5e1;"></div>
                            <div><label style="font-size: 12px; color: #64748b;">State</label><input type="text" value="Karnataka" disabled style="width:100%; padding: 8px; border-radius: 6px; border: 1px solid #cbd5e1;"></div>
                            <div><label style="font-size: 12px; color: #64748b;">Aadhaar Link</label><input type="text" value="Verified ✅" disabled style="width:100%; padding: 8px; border-radius: 6px; border: 1px solid #cbd5e1; background: #dcfce7; color: #16a34a;"></div>
                            <div><label style="font-size: 12px; color: #64748b;">PAN Link</label><input type="text" value="Assistant Verified ✅" disabled style="width:100%; padding: 8px; border-radius: 6px; border: 1px solid #cbd5e1; background: #dcfce7; color: #16a34a;"></div>
                        </div>
                    </div>

                    <div id="aiRecheckBlock" style="margin-top: 20px; padding: 15px; background: #fffbeb; border-radius: 10px; border: 1px solid #fde68a;">
                        <h4 style="color: #b45309; margin-bottom: 10px;">🤖 AI Validation Recheck (Final Layer)</h4>
                        <p style="font-size: 13px; color: #92400e;">Before final submission, AI is re-validating the assistant's work...</p>
                        <ul style="font-size: 13px; margin-top: 10px; color: #16a34a; font-weight: 600; list-style: none; padding: 0;">
                            <li>✅ Name matches Aadhaar database exactly.</li>
                            <li>✅ No missing fields detected.</li>
                            <li>✅ Final workflow consistency check passed.</li>
                        </ul>
                    </div>

                    <button class="btn-primary w-100 mt-20" onclick="submitPipelineApplication()" id="finalSubmitBtn" style="font-size: 16px; padding: 15px; background: #16a34a;">Final Submit Application</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Rate Assistant Modal -->
    <div id="rateModal" class="modal hidden" style="z-index: 10020; align-items: center;">
        <div class="modal-card" style="width: 450px; text-align: center; background: white; border-radius: 20px; padding: 30px;">
            <div style="font-size: 40px; margin-bottom: 10px;">🌟</div>
            <h2 style="color: #1e3a8a;">Rate Your Assistant</h2>
            <p class="text-muted" style="margin-bottom: 20px;">Your feedback trains our AI matching loop!</p>
            
            <p style="font-size: 14px;">How was your experience with <strong id="rateAssistantName" style="color: #1d4ed8;"></strong>?</p>
            <div style="font-size: 40px; margin: 15px 0; display: flex; justify-content: center; gap: 5px;" id="starRating">
                <span style="cursor: pointer; transition: 0.2s;" onclick="setRating(1)">⭐</span>
                <span style="cursor: pointer; transition: 0.2s;" onclick="setRating(2)">⭐</span>
                <span style="cursor: pointer; transition: 0.2s;" onclick="setRating(3)">⭐</span>
                <span style="cursor: pointer; transition: 0.2s;" onclick="setRating(4)">⭐</span>
                <span style="cursor: pointer; transition: 0.2s;" onclick="setRating(5)">⭐</span>
            </div>
            
            <div style="text-align: left; margin-top: 20px;">
                <label style="font-size: 12px; font-weight: bold; color: #64748b;">Feedback (Communication, Speed, Accuracy):</label>
                <textarea id="rateFeedback" placeholder="Your feedback improves future matches..." style="width: 100%; height: 80px; padding: 10px; border-radius: 8px; border: 1px solid #cbd5e1; margin-top: 5px; font-family: inherit; font-size: 13px;"></textarea>
            </div>
            
            <button class="btn-primary w-100 mt-20" onclick="submitRating()" style="background: #1e40af;">Submit Feedback & Enhance AI</button>
            <button class="btn-ghost w-100 mt-10" onclick="closeSmallModal('rateModal')">Skip</button>
        </div>
    </div>
"""

# Insert modals before the Chat Widget
if 'id="pipelineModal"' not in html:
    html = html.replace('<!-- Floating Chat Widget (Single) -->', modals_to_add + '\n    <!-- Floating Chat Widget (Single) -->')

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Added HTML Modals")

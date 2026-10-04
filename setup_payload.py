import os

financial_text = """================================================================================
INTERBANK RTGS FINANCIAL CLEARING & SETTLEMENT DISPATCH
Message Reference : SWIFT-MT103-IN20261004-98421
Transaction Type  : High-Value Interbank Fund Transfer
Channel Security  : E2EE Encrypted Transport Layer (AES-128 / RSA-2048)
Timestamp (IST)   : 2026-10-04 13:21:00 IST
================================================================================

1. ORDERING CUSTOMER (DEBIT):
   - Account Holder  : Gujarat Industrial Solutions Pvt. Ltd.
   - Account Number  : 0928104000128491
   - Originating IFSC: SBIN0001824 (Surat Main Branch)
   - Clearing Branch : State Bank of India, Nanpura, Surat, Gujarat

2. BENEFICIARY CUSTOMER (CREDIT):
   - Beneficiary Name: Apex Hardware & Automation Corp.
   - Account Number  : 50200049281140
   - Destination IFSC: HDFC0000060 (Fort Branch, Mumbai)
   - Clearing Branch : HDFC Bank Ltd, Fort, Mumbai, Maharashtra

3. TRANSACTION DETAILS:
   - Transfer Amount : INR 12,50,000.00 (Twelve Lakh Fifty Thousand Rupees Only)
   - Settlement Type : Immediate Real-Time Gross Settlement (RTGS)
   - Purpose Code    : B2B Supplier Trade Invoice Settlement (#INV-2026-0814)
   - Regulatory Auth : Reserve Bank of India (RBI) Financial Clearing Net

4. INTEGRITY & AUDIT POLICY:
   This transaction payload requires multi-party end-to-end cryptographic verification.
   Any bit-level anomaly detected during transmission will trigger an immediate
   account-level freeze and raise an automated compliance audit flag.
================================================================================
"""

# Pad until file size >= 1024 bytes (1 KB)
while len(financial_text.encode("utf-8")) < 1024:
    financial_text += "# RBI-RTGS-AUDIT-RECORD-PAD: INTEGRITY VERIFICATION BLOCK CHECKPASS #\n"

with open("financial_payload.txt", "wb") as f:
    f.write(financial_text.encode("utf-8"))

print(f"Generated: financial_payload.txt | Size: {os.path.getsize('financial_payload.txt')} bytes (>= 1 KB)")

reference_data = {
    "8574": {
        "lab_result": "Blood test normal, WBC: 6,200 (Normal: 4,500-10,000),Platelets: 320K (Normal: 140K-450K),RBC: 5.5M (Normal: 5-6M)",
        "prescription": "Take Paracetamol, one tablet every 8 hours, for 5 days. Stay safe and take care!",
        "billing": "Total: $120."
    },
    "1786": {
        "lab_result": """Cholesterol high. Summary:

1. Hematocrit: 45% (Normal: 41-50%)
2. WBC: 6,200 (Normal: 4,500-10,000)
3. RBC: 5.5M (Normal: 5-6M)
4. Platelets: 320K (Normal: 140K-450K)
5. Eosinophils: 3% (Normal: 1-4%)

Lipoprotein Panel:
6. Total Cholesterol: 240 (Normal: ≤ 200)
7. LDL: 160 (Normal: < 100)
8. HDL: 35 (Normal: ≥ 40)
9. Triglycerides: 180 (Normal: < 150)

WBC Differential:
10. Neutrophils: 55% (Normal: 40-60%)
11. Lymphocytes: 30% (Normal: 20-40%)
12. Monocytes: 6% (Normal: 2-8%)
13. Basophils: 0.8% (Normal: 0.5-1%)

14. Typhoid Test: Negative
""",
        "prescription": "Take Paracetamol, one tablet every 8 hours, for 5 days. Stay safe and take care!",
        "billing": "Total: $150."
    }
}

def get_lab_result(reference_number):
    data = reference_data.get(reference_number)
    if data and 'lab_result' in data:
        return data['lab_result']
    return f"{reference_number} - Please enter your reference number in the message box above."

def get_prescription(reference_number):
    data = reference_data.get(reference_number)
    if data and 'prescription' in data:
        return data['prescription']
    return f"{reference_number} - Please enter your reference number in the message box above."

def get_billing(reference_number):
    data = reference_data.get(reference_number)
    if data and 'billing' in data:
        return data['billing']
    return f"{reference_number} - Please enter your reference number in the message box above."

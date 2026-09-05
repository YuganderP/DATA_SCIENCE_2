WARDS = {
    "ICU": {"available_beds": 2, "tags": {"critical", "ventilator", "emergency"}},
    "GENERAL": {"available_beds": 5, "tags": {"recovery", "observation", "routine"}},
    "CARDIOLOGY": {"available_beds": 1, "tags": {"heart", "critical", "monitoring"}},
}
LOG_FILE = "hospital_records.txt"


def inspect_audit_logs():
    try:
        file = open(LOG_FILE, "r")
    except FileNotFoundError:
        print("Log file not found")
    finally:
        data = file.readlines()
        for i, j in enumerate(data):
            print(f"{i}: {j}")
        file.close()


def admit_patient():
    patientId = input("Please enter the patient ID")
    ward = input("Please enter the ward name")
    if len(patientId) < 5:
        raise Exception("Invalid Patient ID")
    elif patientId[:3].upper() != "PAT":
        raise Exception("Invalid Patient ID")
    else:
        ward = ward.upper()
        if ward in WARDS.keys():
            beds = WARDS[ward]["available_beds"]

            if beds > 0:
                WARDS[ward]["available_beds"] = WARDS[ward]["available_beds"] - 1
                print(f"patient has been admitted to {ward}")
                file = open(LOG_FILE, "a")
                file.write(f"PATIENT: {patientId} | WARD: {ward} | ACTION: ADMITTED\n")
                file.close()
            else:
                print(f"{ward} is full ")
        else:
            raise Exception("Invalid Ward Name")


def discharge_patient():
    patientId = input("Please enter the patient ID")
    ward = input("Please enter the ward name")
    if len(patientId) < 5:
        raise Exception("Invalid Patient ID")
    elif patientId[:3].upper() != "PAT":
        raise Exception("Invalid Patient ID")
    else:
        ward = ward.upper()
        if ward in WARDS.keys():
            WARDS[ward]["available_beds"] = WARDS[ward]["available_beds"] + 1
            print("The patinet has been discharged")
            file = open(LOG_FILE, "a")
            file.write(f"PATIENT: {patientId} | WARD: {ward} | ACTION: DISCHARGED\n")
            file.close()
        else:
            raise Exception("Invalid Ward Name")


def view_ward_match_symptom():
    symptoms = input("Please enter your symptoms:")
    symptoms = symptoms.split(",")
    symptoms = set(symptoms)
    print(symptoms)
    match = 0
    tags = ""
    for i in WARDS:
        value = symptoms & WARDS[i]["tags"]
        print(len(value))
        print(match)

        if len(value) > match:
            match = len(value)
            tags = i

    if match:
        if WARDS[tags]["available_beds"] > 0:
            print(tags, "Available")
        else:
            print(tags, "Full")


start = True

while start:
    print("========================================")
    print("HOSPITAL PATIENT & WARD SYSTEM")
    print("========================================")
    print("1. View Wards & Match Symptoms (Sets) ")
    print("2. Admit Patient (Validation & Dict Update) ")
    print("3. Discharge Patient (Increase Bed Count & Log)")
    print("4. Inspect Audit Logs (File IO + Seek/Tell)")
    print("5. Exit ")
    option = input("Please select your opiton Number")
    try:
        option = int(option)

        if option > 5 or option <= 0:
            raise Exception("wrong option selected ")
    except Exception:
        print("Invalid opiton selected")

        start = False
    finally:
        if option == 1:
            view_ward_match_symptom()
        elif option == 2:
            admit_patient()

        elif option == 3:
            discharge_patient()
        elif option == 4:
            inspect_audit_logs()
        elif option == 5:
            break

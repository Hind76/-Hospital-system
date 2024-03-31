from datetime import datetime


class Patient:  # Defining a class for Patient
    def __init__(self, id, name, age, gender, address, phone_number, email, medical_condition, risk_level, height=None,
                 weight=None, allergies=None, previous_surgeries=None, vital_signs=None):
        # Initializing the Patient class with various attributes
        self.id = id  # Patient ID
        self.name = name  # Patient name
        self.age = age  # Patient age
        self.gender = gender  # Patient gender
        self.address = address  # Patient address
        self.phone_number = phone_number  # Patient phone number
        self.email = email  # Patient email
        self.medical_condition = medical_condition  # Patient's current medical condition
        self.risk_level = risk_level  # Patient's risk level
        self.height = height  # Patient's height (optional)
        self.weight = weight  # Patient's weight (optional)
        self.allergies = allergies if allergies else []  # Patient's allergies (default empty list)
        self.previous_surgeries = previous_surgeries if previous_surgeries else []  # Previous surgeries (default empty list)
        self.vital_signs = vital_signs if vital_signs else {}  # Patient's vital signs (default empty dictionary)
        self.prescriptions = []  # List to store patient's prescriptions

    def add_vital_sign(self, key, value):
        # Method to add a vital sign for the patient
        self.vital_signs[key] = value  # Adding a new vital sign to the patient's vital signs dictionary

    def add_prescription(self, prescription):
        # Method to add a prescription for the patient
        self.prescriptions.append(prescription)  # Appending a new prescription to the patient's prescription list

    def __lt__(self, other):
        # Special method for comparison (<) between Patient objects based on their ID
        return self.id < other.id  # Comparing patients based on their ID


class Doctor:  # Defining a class for Doctor
    def __init__(self, id, name, specialization, address, phone_number, email):
        # Initializing the Doctor class with various attributes
        self.id = id  # Doctor ID
        self.name = name  # Doctor name
        self.specialization = specialization  # Doctor's specialization
        self.address = address  # Doctor's address
        self.phone_number = phone_number  # Doctor's phone number
        self.email = email  # Doctor's email
        self.schedule = {}  # Dictionary to store doctor's schedule

    def add_schedule(self, date, time):
        # Method to add a schedule for the doctor
        if date in self.schedule:  # If date already exists in the schedule
            self.schedule[date].append(time)  # Append the new time to the existing date
        else:  # If date does not exist in the schedule
            self.schedule[date] = [time]  # Create a new entry for the date with the new time

    def is_available(self, date, time):
        # Method to check if the doctor is available at a specific date and time
        return self.schedule.get(date) and time not in self.schedule[date]  # Check if time slot is available

    def get_available_times(self, date):
        # Method to get the available times for the doctor on a specific date
        return [(time, idx + 1) for idx, time in enumerate(self.schedule.get(date, []))]
        # Return available times along with their indices


class Prescription:  # Defining a class for Prescription
    def __init__(self, medication, dosage, frequency, instructions):
        # Initializing the Prescription class with various attributes
        self.medication = medication  # Prescription medication
        self.dosage = dosage  # Dosage of the medication
        self.frequency = frequency  # Frequency of medication intake
        self.instructions = instructions  # Instructions for taking the medication


class HospitalSystem:  # Defining a class for HospitalSystem
    def __init__(self):
        # Initializing the HospitalSystem class with various attributes
        self.patients = []  # List to store patients
        self.doctors = []  # List to store doctors
        self.consultation_queue = []  # List to store patients in consultation queue
        self.arrival_queue = []  # List to store patients in arrival queue
        # Sample patient data
        self.add_patient("P001", "Abdualla Hassan", 35, "Male", "123 Main St", "555-123-4567", "Abdualla @example.com",
                         "Fever", 3, height="180 cm", weight="75 kg", allergies=["Penicillin"],
                         previous_surgeries=["Appendectomy"], vital_signs={"Body Temperature": "101°F"})
        self.add_patient("P002", "Nora Ahmaed", 40, "Female", "456 Oak St", "555-987-6543", "Nora@example.com",
                         "Diabetes", 2, height="165 cm", weight="90 kg", allergies=["Sulfa Drugs"],
                         vital_signs={"Blood Pressure": "120/80 mmHg"})
        self.add_patient("P003", "Maryam Saeed", 25, "Female", "789 Elm St", "555-555-5555", "Maryam@example.com",
                         "Broken Arm", 1, height="170 cm", weight="60 kg", vital_signs={"Pulse Rate": "80 bpm"})
        # Sample doctor data
        self.add_doctor("D001", "Dr. Smith", "Cardiologist", "100 Hospital Rd", "555-111-2222", "smith@example.com")
        self.add_doctor("D002", "Dr. Johnson", "Neurologist", "200 Hospital Rd", "555-333-4444", "johnson@example.com")
        self.add_doctor("D003", "Dr. Williams", "Pediatrician", "300 Hospital Rd", "555-555-6666",
                        "williams@example.com")
        # Sample doctor schedules
        self.doctors[0].add_schedule("2024-04-01", "10:00 AM")
        self.doctors[0].add_schedule("2024-04-01", "02:00 PM")
        self.doctors[1].add_schedule("2024-04-01", "09:00 AM")
        self.doctors[1].add_schedule("2024-04-01", "11:00 AM")
        self.doctors[2].add_schedule("2024-04-01", "11:00 AM")
        self.doctors[2].add_schedule("2024-04-01", "03:00 PM")

    def add_patient(self, id, name, age, gender, address, phone_number, email, medical_condition, risk_level,
                    height=None, weight=None, allergies=None, previous_surgeries=None, vital_signs=None):
        # Method to add a new patient to the system
        patient = Patient(id, name, age, gender, address, phone_number, email, medical_condition, risk_level, height,
                          weight, allergies, previous_surgeries, vital_signs)
        self.patients.append(patient)  # Add patient to the list of patients
        self.arrival_queue.append(patient)  # Add patient to the arrival queue
        self.consultation_queue.append(patient)  # Add patient to the consultation queue
        print(f"New patient {name} added successfully to the system.")  # Print confirmation message

    def add_doctor(self, id, name, specialization, address, phone_number, email):
        # Method to add a new doctor to the system
        doctor = Doctor(id, name, specialization, address, phone_number, email)
        self.doctors.append(doctor)  # Add doctor to the list of doctors

    def schedule_appointment(self, patient_id, doctor_id, date, time_idx):
        # Method to schedule an appointment between a patient and a doctor
        patient = self.search_patient(patient_id)  # Find patient by ID
        doctor = self.search_doctor(doctor_id)  # Find doctor by ID
        if patient and doctor:  # If both patient and doctor exist
            available_times = doctor.get_available_times(
                date)  # Get available times for the doctor on the specified date
            if available_times and time_idx <= len(
                    available_times):  # If there are available times and the selected index is valid
                time = available_times[time_idx - 1][0]  # Get the selected time
                doctor.add_schedule(date, time)  # Add appointment to doctor's schedule
                # Add patient to consultation queue
                self.consultation_queue.append(patient)
                print(f"Appointment scheduled successfully for {patient.name} with {doctor.name} on {date} at {time}.")
            else:
                print("Invalid time selection.")  # Print error message if time selection is invalid
        else:
            print("Patient or doctor not found.")  # Print error message if patient or doctor not found

    def display_calling_queue(self):
        # Method to display the calling queue (patients waiting for consultation) sorted by risk level
        print("\nCalling Queue:")
        sorted_queue = sorted(self.consultation_queue, key=lambda x: x.risk_level,
                              reverse=True)  # Sort the queue by risk level
        for patient in sorted_queue:
            print(
                f"Patient ID: {patient.id}, Name: {patient.name}, Risk Level: {patient.risk_level}, Arrival Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def remove_patient_from_queue(self, patient_id):
        # Method to remove a patient from the consultation queue
        patient = self.search_patient(patient_id)  # Find patient by ID
        if patient:
            if patient in self.consultation_queue:  # If patient is in consultation queue
                self.consultation_queue.remove(patient)  # Remove patient from the consultation queue
                print(f"{patient.name} removed from the consultation queue.")  # Print confirmation message
                self.display_calling_queue()  # Display updated calling queue
            else:
                print(
                    f"{patient.name} is not in the consultation queue.")  # Print error message if patient not in queue
        else:
            print("Patient not found.")  # Print error message if patient not found

    def display_patient_info(self, patient_id):
        # Method to display information of a specific patient
        patient = self.search_patient(patient_id)  # Find patient by ID
        if patient:
            print("\nPatient Information:")
            # Print various details of the patient
            print(f"ID: {patient.id}")
            print(f"Name: {patient.name}")
            print(f"Age: {patient.age}")
            print(f"Gender: {patient.gender}")
            print(f"Address: {patient.address}")
            print(f"Phone Number: {patient.phone_number}")
            print(f"Email: {patient.email}")
            print(f"Medical Condition: {patient.medical_condition}")
            print(f"Risk Level: {patient.risk_level}")
            print(f"Height: {patient.height}")
            print(f"Weight: {patient.weight}")
            print(f"Allergies: {', '.join(patient.allergies)}")
            print(f"Previous Surgeries: {', '.join(patient.previous_surgeries)}")
            print("Vital Signs:")
            for key, value in patient.vital_signs.items():
                print(f"{key}: {value}")
            print("Prescriptions:")
            for prescription in patient.prescriptions:
                print(f"Medication: {prescription.medication}")
                print(f"Dosage: {prescription.dosage}")
                print(f"Frequency: {prescription.frequency}")
                print(f"Instructions: {prescription.instructions}")
        else:
            print("Patient not found.")  # Print error message if patient not found

    def update_patient_info(self, patient_id, vital_signs, weight):
        # Method to update information of a specific patient
        patient = self.search_patient(patient_id)  # Find patient by ID
        if patient:
            for key, value in vital_signs.items():  # Update vital signs
                patient.add_vital_sign(key, value)
            patient.weight = weight  # Update patient's weight
            print(f"{patient.name}'s information updated successfully.")  # Print confirmation message
            self.display_patient_info(patient_id)  # Display updated patient information
        else:
            print("Patient not found.")  # Print error message if patient not found

    def purchase_prescription(self, patient_id):
        # Method for purchasing prescription for a patient
        patient = self.search_patient(patient_id)  # Find patient by ID
        if patient:
            print("Prescription Purchase:")
            print("1. Aspirin")
            print("2. Ibuprofen")
            print("3. Paracetamol")
            print("4. Antibiotics")
            print("5. Antihistamines")
            choice = input("Enter your choice: ")  # Prompt user to enter choice
            medications = {
                '1': ("Aspirin", "325 mg"),
                '2': ("Ibuprofen", "200 mg"),
                '3': ("Paracetamol", "500 mg"),
                '4': ("Antibiotics", "500 mg"),
                '5': ("Antihistamines", "10 mg")
            }
            if choice in medications:  # If choice is valid
                medication, dosage = medications[choice]  # Get medication and dosage
                frequency = "Once daily"  # Set frequency of medication
                instructions = "After meal"  # Set instructions for medication
                prescription = Prescription(medication, dosage, frequency, instructions)  # Create prescription object
                patient.add_prescription(prescription)  # Add prescription to patient
                self.consultation_queue.remove(patient)  # Remove patient from consultation queue
                print(
                    f"{medication} prescription purchased successfully for {patient.name}.")  # Print confirmation message
                print("Prescription Details:")
                # Print details of purchased prescription
                print(f"Medication: {medication}")
                print(f"Dosage: {dosage}")
                print(f"Frequency: {frequency}")
                print(f"Instructions: {instructions}")
            else:
                print("Invalid choice.")  # Print error message for invalid choice
        else:
            print("Patient not found.")  # Print error message if patient not found

    def search_patient(self, patient_id):
        # Method to search for a patient by ID
        for patient in self.patients:  # Iterate through list of patients
            if patient.id == patient_id:  # If patient ID matches
                return patient  # Return the patient object
        return None  # Return None if patient not found

    def search_doctor(self, doctor_id):
        # Method to search for a doctor by ID
        for doctor in self.doctors:  # Iterate through list of doctors
            if doctor.id == doctor_id:  # If doctor ID matches
                return doctor  # Return the doctor object
        return None  # Return None if doctor not found

    def display_doctor_schedule(self, doctor_id):
        # Method to display the schedule of a specific doctor
        doctor = self.search_doctor(doctor_id)  # Find doctor by ID
        if doctor:
            print(f"\nDoctor {doctor.name} Schedule:")
            for date, times in doctor.schedule.items():  # Iterate through doctor's schedule
                print(f"Date: {date}, Available Times:")  # Print date and available times
                for idx, time in enumerate(times, 1):  # Enumerate available times
                    print(f"{idx}. {time}")  # Print available times with indices
        else:
            print("Doctor not found.")  # Print error message if doctor not found

    def display_doctor_info(self, doctor_id):
        # Method to display information of a specific doctor
        doctor = self.search_doctor(doctor_id)  # Find doctor by ID
        if doctor:
            print("\nDoctor Information:")
            # Print various details of the doctor
            print(f"ID: {doctor.id}")
            print(f"Name: {doctor.name}")
            print(f"Specialization: {doctor.specialization}")
            print(f"Address: {doctor.address}")
            print(f"Phone Number: {doctor.phone_number}")
            print(f"Email: {doctor.email}")
            print("Schedule:")
            for date, times in doctor.schedule.items():  # Iterate through doctor's schedule
                print(f"Date: {date}, Available Times:")  # Print date and available times
                for time in times:  # Iterate through available times
                    print(time)  # Print each available time
        else:
            print("Doctor not found.")  # Print error message if doctor not found

    def display_arrival_queue(self):
        # Method to display the arrival queue (patients waiting for arrival)
        print("\nArrival Queue:")
        for patient in self.arrival_queue:
            print(
                f"Patient ID: {patient.id}, Name: {patient.name}, Risk Level: {patient.risk_level}, Arrival Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def menu(self):
        # Method to display the menu for hospital management system
        while True:  # Loop until user exits
            print("\nHospital Management System")  # Print system title
            print("1. Display Doctor's Schedule")  # Menu option 1
            print("2. Schedule Appointment")  # Menu option 2
            print("3. Remove Patient from Queue")  # Menu option 3
            print("4. Update Patient Information")  # Menu option 4
            print("5. Purchase Prescription")  # Menu option 5
            print("6. Display Calling Queue")  # Menu option 6
            print("7. Add New Patient")  # Menu option 7
            print("8. Display Patient Information")  # Menu option 8
            print("9. Display Doctor Information")  # Menu option 9
            print("10. Display Arrival Queue")  # Menu option 10
            print("11. Exit")  # Menu option 11
            choice = input("Enter your choice: ")  # Prompt user for choice
            if choice == '1':  # Option 1: Display Doctor's Schedule
                doctor_id = input("Enter doctor ID to view schedule: ")  # Prompt user for doctor ID
                self.display_doctor_schedule(doctor_id)  # Call method to display doctor's schedule
            elif choice == '2':  # Option 2: Schedule Appointment
                print("Doctor's Schedule:")
                for doctor in self.doctors:  # Iterate through list of doctors
                    print(f"Doctor ID: {doctor.id}, Name: {doctor.name}")  # Print doctor IDs and names
                    for date, times in doctor.schedule.items():  # Iterate through doctor's schedule
                        print(f"Date: {date}, Available Times:")  # Print date and available times
                        for idx, time in enumerate(times, 1):  # Enumerate available times
                            print(f"{idx}. {time}")  # Print available times with indices
                for patient in self.patients:  # Iterate through list of patients
                    print(f"patient ID: {patient.id}, Name: {patient.name}")  # Print patient IDs and names
                patient_id = input("Enter patient ID: ")  # Prompt user for patient ID
                doctor_id = input("Enter doctor ID: ")  # Prompt user for doctor ID
                date = input("Enter appointment date (YYYY-MM-DD): ")  # Prompt user for appointment date
                time_idx = int(input(
                    "Enter the number corresponding to the preferred appointment time: "))  # Prompt user for appointment time index
                self.schedule_appointment(patient_id, doctor_id, date, time_idx)  # Call method to schedule appointment
            elif choice == '3':  # Option 3: Remove Patient from Queue
                password = input("Enter password: ")  # Prompt user for password
                if password == "besthospital":  # Check if password is correct
                    patient_id = input("Enter patient ID to remove from the queue: ")  # Prompt user for patient ID
                    self.remove_patient_from_queue(patient_id)  # Call method to remove patient from queue
                else:
                    print("Incorrect password.")  # Print error message for incorrect password
            elif choice == '4':  # Option 4: Update Patient Information
                password = input("Enter password: ")  # Prompt user for password
                if password == "besthospital":  # Check if password is correct
                    patient_id = input("Enter patient ID to update information: ")  # Prompt user for patient ID
                    print("patient information before updating: ")
                    self.display_patient_info(patient_id)
                    vital_signs_input = input(
                        "Enter vital signs (key-value pairs, e.g., 'Blood Pressure:120/80 mmHg'): ")  # Prompt user for vital signs
                    vital_signs = dict(item.split(":") for item in
                                       vital_signs_input.split(","))  # Split input and create dictionary of vital signs
                    weight = input("Enter patient weight: ")  # Prompt user for patient weight
                    self.update_patient_info(patient_id, vital_signs,
                                             weight)  # Call method to update patient information
                else:
                    print("Incorrect password.")  # Print error message for incorrect password
            elif choice == '5':  # Option 5: Purchase Prescription
                patient_id = input("Enter patient ID to purchase prescription: ")  # Prompt user for patient ID
                self.purchase_prescription(patient_id)  # Call method to purchase prescription
            elif choice == '6':  # Option 6: Display Calling Queue
                self.display_calling_queue()  # Call method to display calling queue
            elif choice == '7':  # Option 7: Add New Patient
                # Prompt user for patient details
                id = input("Enter patient ID: ")
                name = input("Enter patient name: ")
                age = int(input("Enter patient age: "))
                gender = input("Enter patient gender: ")
                address = input("Enter patient address: ")
                phone_number = input("Enter patient phone number: ")
                email = input("Enter patient email: ")
                medical_condition = input("Enter patient's medical condition: ")
                risk_level = int(input("Enter patient's risk level (1-5): "))
                height = input("Enter patient height (optional): ")
                weight = input("Enter patient weight (optional): ")
                allergies = input("Enter patient allergies (comma-separated, optional): ").split(",")
                previous_surgeries = input("Enter patient previous surgeries (comma-separated, optional): ").split(",")
                vital_signs = input("Enter patient vital signs (key-value pairs, optional): ").split(",")
                vital_signs = dict(item.split(":") for item in vital_signs)
                # Call method to add new patient
                self.add_patient(id, name, age, gender, address, phone_number, email, medical_condition, risk_level,
                                 height, weight, allergies, previous_surgeries, vital_signs)
            elif choice == '8':  # Option 8: Display Patient Information
                password = input("Enter password: ")
                if password == "besthospital":
                    patient_id = input("Enter patient ID to display information: ")  # Prompt user for patient ID
                    self.display_patient_info(patient_id)  # Call method to display patient information
                else:
                    print("Incorrect password.")
            elif choice == '9':  # Option 9: Display Doctor Information
                password = input("Enter password: ")
                if password == "besthospital":
                    doctor_id = input("Enter doctor ID to display information: ")  # Prompt user for doctor ID
                    self.display_doctor_info(doctor_id)  # Call method to display doctor information
                else:
                    print("Incorrect password.")
            elif choice == '10':  # Option 10: Display Arrival Queue
                self.display_arrival_queue()  # Call method to display arrival queue
            elif choice == '11':  # Option 11: Exit
                print("Exiting...")  # Print exit message
                break  # Exit the loop
            else:  # Invalid choice
                print("Invalid choice. Please enter a number from 1 to 11.")  # Print error message for invalid choic


# Main function
if __name__ == "__main__":
    hospital_system = HospitalSystem()  # Create an instance of HospitalSystem
    hospital_system.menu()

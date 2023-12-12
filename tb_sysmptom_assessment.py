class TBSymptomAssessment:
    def __init__(self):
        self.user_data = {}

    def ask_question(self, question):
        response = input(question + " (Yes/No): ").lower()
        return response == 'yes'

    def ask_severity(self, symptom):
        severity = input(f"On a scale of 1 to 10, how severe is your {symptom.lower()}? ")
        return int(severity) if severity.isdigit() else 0

    def calculate_symptom_score(self):
        symptoms = ["persistent_cough", "coughing_up_blood_or_sputum", "chest_pain_or_discomfort",
                    "unintentional_weight_loss", "loss_of_appetite", "fatigue_and_weakness",
                    "night_sweats", "fever_or_chills", "shortness_of_breath", "swelling_of_the_neck_or_lymph_nodes"]

        total_score = 0
        for symptom in symptoms:
            severity_key = f'{symptom.lower().replace(" ", "_")}_severity'
            if severity_key in self.user_data:
                total_score += self.user_data[severity_key]

        return total_score

    def evaluate_risk(self, total_score):
        if total_score >= 30:
            return "High risk. Consult a healthcare professional immediately."
        elif 20 <= total_score < 30:
            return "Moderate risk. Monitor your symptoms and seek medical advice."
        else:
            return "Low risk. Continue to monitor your health."

    def tb_symptom_assessment(self):
        print("Welcome to the TB Symptom Self-Assessment Form.\n")

        # General Information
        self.user_data['contact_with_tb'] = self.ask_question("Have you been in contact with someone diagnosed with TB?")
        self.user_data['high_risk_environment'] = self.ask_question("Do you live or work in an environment with a higher risk of TB exposure?")
        self.user_data['previous_tb_diagnosis'] = self.ask_question("Have you ever been diagnosed with TB in the past?")

        # Symptoms
        symptoms = ["Persistent cough", "Coughing up blood or sputum", "Chest pain or discomfort",
                    "Unintentional weight loss", "Loss of appetite", "Fatigue and weakness",
                    "Night sweats", "Fever or chills", "Shortness of breath", "Swelling of the neck or lymph nodes"]

        for symptom in symptoms:
            if self.ask_question(f"Are you experiencing {symptom.lower()}?"):
                self.user_data[f'{symptom.lower().replace(" ", "_")}_severity'] = self.ask_severity(symptom)

        # Calculate Symptom Score
        total_score = self.calculate_symptom_score()

        # Additional Information
        self.user_data['additional_symptoms'] = input("Any other symptoms or concerns not listed above? ")

        # Medical History
        self.user_data['chronic_conditions'] = input("List any chronic medical conditions you currently have: ")
        self.user_data['current_medications'] = input("List any medications you are currently taking: ")

        # Emergency Contact
        self.user_data['emergency_contact_name'] = input("Emergency contact name: ")
        self.user_data['emergency_contact_relationship'] = input("Relationship to emergency contact: ")
        self.user_data['emergency_contact_phone'] = input("Emergency contact phone number: ")

        # Evaluate Risk and Provide Recommendation
        risk_evaluation = self.evaluate_risk(total_score)
        print("\nSymptom Score:", total_score)
        print("Risk Evaluation:", risk_evaluation)

        print("\nThank you for completing the TB Symptom Self-Assessment Form. Your information has been recorded.")

# Example of using the module
if __name__ == "__main__":
    tb_assessment = TBSymptomAssessment()
    tb_assessment.tb_symptom_assessment()
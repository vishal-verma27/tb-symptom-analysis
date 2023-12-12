class TBSelfAssessment:
    def __init__(self):
        self.questions_part_a = [
            "Cough for more than 2 weeks (not related to an existing diagnosis or condition)?",
            "Unexplained fever for more than 1 week?",
            "Recent unexplained weight loss?",
            "Coughing up blood?",
            "Excessive sweating during the night for more than 1 week?"
        ]

    def get_user_input(self, questions):
        answers = []
        for i, question in enumerate(questions, 1):
            answer = input(f"{i}. {question} (yes/no): ").lower()
            answers.append(answer == 'yes')
        return answers

    def analyze_answers_part_a(self, answers):
        if any(answers):
            print("\nMake an urgent appointment with your doctor or TB Control Unit for assessment of your symptom/s.")
            print("Further referral to a TB specialist may be recommended by your doctor.")
            clearance_required = input("Clearance for active TB required? (yes/no): ").lower()
            if clearance_required == 'yes':
                print("Clearance for active TB attached? (yes/no)")
                clearance_attached = input().lower()
                if clearance_attached == 'yes':
                    print("You can commence placement.")
                else:
                    print("Please provide clearance for active TB to your Education Provider Placement Coordinator.")
            else:
                print("Please provide clearance for active TB to your Education Provider Placement Coordinator.")
        else:
            print("\nNo significant symptoms detected.")

    def analyze_answers_part_b(self, answers):
        if answers[0] == 'no':  # Born in Australia
            print("\nNo further assessment required. You can commence placement.")
        else:
            print("\nTesting for latent TB infection is required.")
            print("You can still commence placement, but further assessment with a doctor or at a TB Control Unit is necessary.")

    def run_assessment(self):
        print("Welcome to the TB Self-Assessment Screening Test.")
        print("Answer the following questions to assess your risk of tuberculosis (TB).\n")

        answers_part_a = self.get_user_input(self.questions_part_a)
        self.analyze_answers_part_a(answers_part_a)

        print("\nPart B: TB exposure risk history")
        born_in_australia = input("Were you born in Australia? (yes/no): ").lower()
        answers_part_b = [born_in_australia]
        self.analyze_answers_part_b(answers_part_b)


if __name__ == "__main__":
    tb_assessment = TBSelfAssessment()
    tb_assessment.run_assessment()

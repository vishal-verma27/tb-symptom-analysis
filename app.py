from flask import Flask, request, render_template, jsonify, send_from_directory
from flask_cors import CORS
import json, os
import shutil, tb_model_predict
import pandas as pd
from fuzzywuzzy import process

app = Flask(__name__)
CORS(app)

# Define a mapping for severity scores
severity_mapping = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5,
                    '6': 6, '7': 7, '8': 8, '9': 9, '10': 10}

# Define a mapping for binary responses
binary_mapping = {'yes': 2, 'no': 0}

# Load the TB classification model
classifier = tb_model_predict.TuberculosisClassifierPredict("model\\tuberculosis_model.h5")

def calculate_assessment_score(data):
    total_score = 0
    total_score += binary_mapping.get(data.get('Have you been in contact with someone diagnosed with TB? (Yes/No)', ''), 0)
    total_score += binary_mapping.get(data.get('Do you live or work in an environment with a higher risk of TB exposure? (Yes/No)', ''), 0)
    total_score += binary_mapping.get(data.get('Have you ever been diagnosed with TB in the past? (Yes/No)', ''), 0)
    total_score += binary_mapping.get(data.get('Are you experiencing persistent cough? (Yes/No)', ''), 0)
    total_score += severity_mapping.get(data.get('On a scale of 1 to 10, how severe is your persistent cough?', ''), 0)
    total_score += binary_mapping.get(data.get('Are you experiencing coughing up blood or sputum? (Yes/No)', ''), 0)
    total_score += severity_mapping.get(data.get('On a scale of 1 to 10, how severe is your coughing up blood or sputum?', ''), 0)
    total_score += binary_mapping.get(data.get('Are you experiencing chest pain or discomfort? (Yes/No)', ''), 0)
    total_score += binary_mapping.get(data.get('Are you experiencing unintentional weight loss? (Yes/No)', ''), 0)
    total_score += binary_mapping.get(data.get('Are you experiencing loss of appetite? (Yes/No)', ''), 0)
    total_score += binary_mapping.get(data.get('Are you experiencing fatigue and weakness? (Yes/No)', ''), 0)
    total_score += severity_mapping.get(data.get('On a scale of 1 to 10, how severe is your fatigue and weakness?', ''), 0)
    total_score += binary_mapping.get(data.get('Are you experiencing night sweats? (Yes/No)', ''), 0)
    total_score += binary_mapping.get(data.get('Are you experiencing fever or chills? (Yes/No)', ''), 0)
    total_score += binary_mapping.get(data.get('Are you experiencing shortness of breath? (Yes/No)', ''), 0)
    total_score += severity_mapping.get(data.get('On a scale of 1 to 10, how severe is your shortness of breath?', ''), 0)

    return evaluate_risk(total_score=total_score), total_score


# Load your Excel file
file_path = 'dataset\\STO.xlsx'  # Replace with the actual file path
df = pd.read_excel(file_path)

def find_similar_address(state):
    # Use fuzzy matching to find the closest match for the provided State name
    matched_state = process.extractOne(state, df['State Name'])[0]

    # Filter DataFrame based on the matched State
    filtered_df = df[df['State Name'] == matched_state]

    if filtered_df.empty:
        return "No matching records found."

    # Get the best similar address
    best_address = {
        'State_Name': filtered_df.iloc[0]['State Name'], 
        'STO_Name': filtered_df.iloc[0]['STO Name'],
        'Email_Id': filtered_df.iloc[0]['Email Id'],
        'Office_No': filtered_df.iloc[0]['Phone no. Office'],
        'Residence_No': filtered_df.iloc[0]['Phone no. Res'],
        'Mobile_No': filtered_df.iloc[0]['Mobile No'],
        'Address': filtered_df.iloc[0]['Address'],
        'Pin_Code': filtered_df.iloc[0]['Pin Code']
    }

    return best_address

def evaluate_risk(total_score):
    if total_score >= 30:
        return "High risk. Consult a healthcare professional immediately."
    elif 20 <= total_score < 30:
        return "Moderate risk. Monitor your symptoms and seek medical advice."
    else:
        return "Low risk. Continue to monitor your health."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/receive_responses', methods=['POST'])
def receive_responses():
    data = request.json

    # Perform any analysis or processing on the received data
    print("Received data:", data)

    # Extract state from the received data
    state = data.get('State', '')

    # Call the similarity function
    similar_address = find_similar_address(state)
    print(similar_address)
    
    stateName = str(similar_address.get('State_Name'))
    stoName = str(similar_address.get('STO_Name'))
    emailId = str(similar_address.get('Email_Id'))
    officeNo = str(similar_address.get('Office_No'))
    residenceNo = str(similar_address.get('Residence_No'))
    mobileNo = str(similar_address.get('Mobile_No'))
    address = str(similar_address.get('Address'))
    pinCode = str(similar_address.get('Pin_Code'))

    # Print all the details
    print("Extracted details:\n")
    print(stateName,stoName,emailId,officeNo,residenceNo,mobileNo,address,pinCode)


    # Calculate assessment score
    result,total_score = calculate_assessment_score(data)

    # Returning a response back to the client
    return jsonify(
        {
        "result": result,
        "total_score":total_score,
        "stateName":stateName,
        "stoName":stoName,
        "emailId":emailId,
        "officeNo":officeNo,
        "residenceNo":residenceNo,
        "mobileNo":mobileNo,
        "address":address,
        "pinCode":pinCode
        }) 

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<path:filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Remove existing files in the upload folder
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected image file"}), 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        print("Saving file to:", filename)
        file.save(filename)

        # Construct the correct image path
        processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    
        # Send the image to the TB classifier
        result = classifier.classify_image(processed_image_path)  # Assuming `filename` is the path to the uploaded image
        # tb_prediction_label = result.get('prediction', 'Unknown')
        classification_label = result["Label"]
        probability_percentage = result["Probability"] * 100
        tb_prediction = f"According to the Chest X-Ray Image Analysis, there is a {probability_percentage:.2f}% chance of {classification_label}."

        # Return the processed image path
        return jsonify({"result": "Image processed successfully", "processed_image_path": processed_image_path,"tb_prediction": tb_prediction}), 200
    else:
        return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
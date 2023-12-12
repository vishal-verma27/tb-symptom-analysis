let currentQuestion = -1; // Initialize with -1 to indicate the greeting state
let userResponses = {};
const startKeyword = "start my assessment";
let globalTbPrediction = "";
const questions = [
  "Have you been in contact with someone diagnosed with TB? (Yes/No)", //0
  "Do you live or work in an environment with a higher risk of TB exposure? (Yes/No)", //1
  "Have you ever been diagnosed with TB in the past? (Yes/No)", //2
  "Are you experiencing persistent cough? (Yes/No)", //3
  "On a scale of 1 to 10, how severe is your persistent cough?",//4
  "Are you experiencing coughing up blood or sputum? (Yes/No)",//5
  "On a scale of 1 to 10, how severe is your coughing up blood or sputum?",//6
  "Are you experiencing chest pain or discomfort? (Yes/No)",//7
  "On a scale of 1 to 10, how severe is your chest pain or discomfort?", //8
  "Are you experiencing unintentional weight loss? (Yes/No)",//9
  "On a scale of 1 to 10, how severe is your unintentional weight loss?",//10
  "Are you experiencing loss of appetite? (Yes/No)",//11
  "On a scale of 1 to 10, how severe is your loss of appetite?",//12
  "Are you experiencing fatigue and weakness? (Yes/No)",//13
  "On a scale of 1 to 10, how severe is your fatigue and weakness?",//14
  "Are you experiencing night sweats? (Yes/No)",//15
  "On a scale of 1 to 10, how severe is your night sweats?",//16
  "Are you experiencing fever or chills? (Yes/No)",//17
  "On a scale of 1 to 10, how severe is your fever or chills?",//18
  "Are you experiencing shortness of breath? (Yes/No)",//19
  "On a scale of 1 to 10, how severe is your shortness of breath?",//20
  "Are you experiencing swelling of the neck or lymph nodes? (Yes/No)",//21
  "On a scale of 1 to 10, how severe is your swelling of the neck or lymph nodes?",//22
  "Do you have your Chest X-Ray image? (PNG format)", //23
  "Please upload a chest X-ray image (PNG format)...", // 24

//  demographic and location details
  "Area Pin Code",//25
  "State",//26
  "Gender: [M] Male [F] Female [O] Other",//27
  "Age",//28
  "Ethnicity",//29
  "Emergency contact name",//30
  "Relationship to emergency contact",//31
  "Emergency contact phone number. (e.g., +91-9090909090)"//32
];

function handleUserResponse(response) {
//   const trimmedResponse = response.trim();
  const trimmedResponse = response.trim().toLowerCase();

  // Check if the user is starting the assessment
  if (currentQuestion === -1) {
    if (trimmedResponse === startKeyword) {
      currentQuestion++; // Move to the first question
      askQuestion();
    } else {
      // Greet the user and prompt them to start the assessment
      addMessage('bot', 'chatbot.png', 'Hello! To start the health assessment,\n please enter: "' + startKeyword + '"');
    }
    return;
  }

  // Validate responses for specific questions
  switch (currentQuestion) {
    case 0:
    case 1:
    case 2:
    case 3:
    case 5:
    case 7:
    case 9:
    case 11:
    case 13:
    case 15:
    case 17:
    case 19:
    case 21:
    case 23:
      if (trimmedResponse.toLowerCase() !== 'yes' && trimmedResponse.toLowerCase() !== 'no') {
        displayErrorAndAskAgain('Please enter a valid response (Yes/No).');
        return;
      }
      break;
      case 26: // Validate State
        if (!isValidText(trimmedResponse)) {
          displayErrorAndAskAgain('Please enter a valid text for State!');
          return;
        }
        break;
    case 27: // Validate Gender
      if (!['m', 'f', 'o'].includes(trimmedResponse.toLowerCase())) {
        displayErrorAndAskAgain('Please enter a valid gender (M/F/O).');
        return;
      }
      break;
    case 28: // Validate Age
      const age = parseInt(trimmedResponse, 10);
      if (isNaN(age) || age < 0 || age > 150) {
        displayErrorAndAskAgain('Please enter a valid age.');
        return;
      }
      break;
    case 29: // Validate Ethnicity
    if (!isValidText(trimmedResponse)) {
      displayErrorAndAskAgain('Please enter a valid text for Ethnicity.');
      return;
    }
    break;
    case 30: // Validate Emergency contact name
    if (!isValidText(trimmedResponse)) {
      displayErrorAndAskAgain('Please enter a valid text for Emergency contact name.');
      return;
    }
    break;
    case 31: // Validate Relationship to emergency contact
      if (!isValidText(trimmedResponse)) {
        displayErrorAndAskAgain('Please enter a valid text for Relationship to emergency contact.');
        return;
      }
      break;
    case 32: // Validate Emergency contact phone number
      if (!isValidPhoneNumber(trimmedResponse)) {
        displayErrorAndAskAgain('Please enter a valid phone number (e.g., +91-9090909090) for Emergency contact phone number.');
        return;
      }
      break;
        case 4: // Severity of persistent cough
        case 6: // Severity of coughing up blood or sputum
        case 8: // Severity of chest pain or discomfort
        case 10: // Severity of unintentional weight loss
        case 12: // Severity of loss of appetite
        case 14: // Severity of fatigue and weakness
        case 16: // Severity of night sweats
        case 18: // Severity of fever or chills
        case 20: // Severity of shortness of breath
        case 22: // Severity of swelling of the neck or lymph nodes
            const severityScore = parseInt(trimmedResponse, 10);
            if (isNaN(severityScore) || severityScore < 1 || severityScore > 10) {
                displayErrorAndAskAgain('Please enter a severity score between 1 and 10.');
                return;
            }
            break;
      default:
        break;
  }

  userResponses[questions[currentQuestion]] = trimmedResponse.toLowerCase();

  // If the current question is about symptoms and the user responds with 'No'
  // then skip the severity scale question and move to the next symptom question.
  if (
    (currentQuestion === 3 || currentQuestion === 5 || currentQuestion === 7 || currentQuestion === 9 || currentQuestion === 11 || currentQuestion === 13 || currentQuestion === 15 || currentQuestion === 17 || currentQuestion === 19 || currentQuestion === 21  || currentQuestion === 23) &&
    trimmedResponse.toLowerCase() === 'no'
  ) {
    currentQuestion += 2; // Skip the next
  } else {
    currentQuestion++; // Move to the next question
  }

  if (
    (currentQuestion === 24)
  ) {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/png';
    fileInput.classList.add('file-input'); // Add a class for styling
    fileInput.addEventListener('change', function (event) {
      handleFileUpload(event.target.files);
    });
    const inputContainer = document.getElementById('input-container');
    inputContainer.appendChild(fileInput);
   
  }

  if (currentQuestion === questions.length) {
    displaySummary();
    saveResponsesToJson();
  } else {
    askQuestion();
  }
}

function isValidAreaPinCode(areaPinCode) {
    // Validate area pin code using a regular expression
    const pinCodeRegex = /^\d{6}$/;
    return pinCodeRegex.test(areaPinCode);
  }
  
  function isValidGender(gender) {
    // Validate gender (M/F/O)
    return ['m', 'f', 'o'].includes(gender.toLowerCase());
  }
  
  function isValidText(text) {
    // Add your text validation logic here
    // For simplicity, we'll consider any non-empty string as valid
    return text.trim() !== '';
  }
  
  function isValidPhoneNumber(phoneNumber) {
    // Validate phone number using a regular expression
    const phoneRegex = /^\+\d{1,3}-\d{10}$/;
    return phoneRegex.test(phoneNumber);
  }


function displayErrorAndAskAgain(errorMessage) {
  addMessage('bot', 'chatbot.png', errorMessage);
  askQuestion(); // Ask the same question again
}

function askQuestion() {
    if (currentQuestion >= 0 && currentQuestion < questions.length) {
      addMessage('bot', 'chatbot.png', questions[currentQuestion]);
    }
  }

function displaySummary() {
  let summary = "Summary of Entered Response:\n";
  for (const [question, response] of Object.entries(userResponses)) {
    summary += `${question}: ${response}\n`;
  }
  addMessage('bot', 'chatbot.png', summary);
}

function saveResponsesToJson() {
  const jsonString = JSON.stringify(userResponses, null, 2);

  // Send the data to the Flask server
  fetch('http://localhost:5000/receive_responses', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: jsonString,
  })
  .then(response => response.json())
  .then(data => {
      // Display the assessment score in the chat
      if(globalTbPrediction === ""){
        addMessage('bot', 'chatbot.png', 'Assessment Score: ' + data.result + '\n\n Please Note: The lack of an X-ray image hinders tuberculosis diagnosis because X-rays are essential for identifying characteristic patterns associated with the disease, and their absence limits the ability to accurately evaluate and confirm tuberculosis.');
      }

      if(globalTbPrediction !== ""){
        addMessage('bot', 'chatbot.png', 'Assessment Score: ' + data.result);
        addMessage('bot', 'chatbot.png', 'Chest X-Ray Analysis: ' + globalTbPrediction);
      }

      if(data.total_score > 20){
        // Display additional results from the JSON data
            summary  = "Nearest State TB Health Facility Details:\n";
            summary += `State Name: ${data.stateName}\n`;
            summary += `STO Name: ${data.stoName}\n`;
            summary += `Email ID: ${data.emailId}\n`;
            summary += `Office No: ${data.officeNo}\n`;
            summary += `Residence No: ${data.residenceNo}\n`;
            summary += `Mobile No: ${data.mobileNo}\n`;
            summary += `Address: ${data.address}\n`;
            summary += `Pin Code: ${data.pinCode}\n`;
        addMessage('bot', 'chatbot.png', summary);
        addMessage('bot', 'chatbot.png', 'Thank you! Have a great day.');
      }
      else{
        addMessage('bot', 'chatbot.png', 'Thank you! Have a great day.');
      }
  })
  .catch((error) => {
      console.error('Error:', error);
  });
}

// Handle input change for file upload
document.getElementById('user-input').addEventListener('change', function (event) {
  const files = event.target.files;
  handleFileUpload(files);
});


function sendMessage() {
  var userInput = document.getElementById('user-input').value;
  if (userInput.trim() === '') {
    return;
  }

  addMessage('user', 'user.png', userInput);
  handleUserResponse(userInput);

  document.getElementById('user-input').value = '';
  var chatMessages = document.getElementById('chat-messages');
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addMessage(sender, avatar, message) {
  var chatMessages = document.getElementById('chat-messages');
  var messageDiv = document.createElement('div');
  messageDiv.className = 'message';
  var avatarImage = document.createElement('img');
  // avatarImage.src = avatar;
  avatarImage.src = (sender === 'user') ? '/static/images/user.png' : '/static/images/chatbot.png'; // Update image sources
  avatarImage.className = sender + '-avatar';
  var messageContent = document.createElement('div');
  messageContent.className = sender + '-message';
  messageContent.innerText = message;
  messageDiv.appendChild(avatarImage);
  messageDiv.appendChild(messageContent);
  chatMessages.appendChild(messageDiv);
  // Scroll to the end of the chat messages container
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function restartChat() {
  location.reload();
}

function handleFileUpload(files) {
  if (files.length > 0) {
    const file = files[0];
    const fileType = file.type;

    if (fileType === 'image/png') {
      // File is valid, proceed with sending to the server
      sendImageToServer(file);
    } else {
      displayErrorAndAskAgain('Please upload a valid PNG image.');
    }
  }
}

function sendImageToServer(file) {
  const formData = new FormData();
  formData.append('image', file);

  fetch('http://localhost:5000/upload_image', {
    method: 'POST',
    body: formData,
  })
  .then(response => response.json())
  .then(data => {
    addMessage('bot', 'chatbot.png',data.result);
    // Hide the upload button after successfully processing the image
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
      fileInput.style.display = 'none';
    }

    // Check if there is a Tuberculosis prediction and store it in the global variable
    if (data.tb_prediction) {
      globalTbPrediction = data.tb_prediction;
    } else{
      globalTbPrediction = "There is some error!"
    }

    // Ask the next question or perform any other actions
    currentQuestion++;
    askQuestion();
  })
  .catch(error => {
    console.error('Error:', error);
  });
}
// Call askQuestion to initiate the conversation
askQuestion();
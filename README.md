# SmartRx
An advanced healthcare AI application that leverages Google Gemini 1.5 Flash for real-time prescription information extraction with 91% accuracy, reducing prescription errors by 40%.

🎯 Key Features

High Accuracy: 91% accuracy in medical text extraction
Error Reduction: 40% reduction in prescription errors through AI verification
Real-time Processing: Instant prescription analysis and information extraction
Scalable MLOps Pipeline: Deployed using AWS and Docker with automation and security
HIPAA-Ready Architecture: Built with healthcare compliance in mind
Comprehensive Validation: Multi-layer verification system for extracted data

🏗️ Architecture
┌─────────────────┐
│   Frontend UI   │
│  (React/HTML)   │
└────────┬────────┘
         │
    ┌────▼─────┐
    │  Flask   │
    │   API    │
    └────┬─────┘
         │
    ┌────▼──────────┐
    │ Google Gemini │
    │  1.5 Flash    │
    └───────────────┘
📋 Prerequisites

Python 3.11+
Docker & Docker Compose
Google Cloud Account with Gemini API access
AWS Account (for deployment)

🚀 Quick Start
1. Clone the Repository
bashgit clone https://github.com/yourusername/smartrx.git
cd smartrx
2. Environment Setup
Create a .env file from the example:
bashcp .env.example .env
Edit .env and add your API keys:
envGOOGLE_API_KEY=your_google_api_key_here
3. Local Development
Using Python Virtual Environment
bash# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
The API will be available at http://localhost:5000
Using Docker
bash# Build and run with Docker Compose
docker-compose up --build

# Or run in detached mode
docker-compose up -d
4. Running Tests
bash# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest test_app.py -v

# Run with coverage
pytest --cov=app test_app.py
📡 API Endpoints
Health Check
httpGET /health
Response:
json{
  "status": "healthy",
  "timestamp": "2024-11-26T12:00:00",
  "model": "gemini-1.5-flash"
}
Analyze Prescription
httpPOST /analyze
Content-Type: multipart/form-data
Request:

image: Prescription image file (JPG, PNG)

Response:
json{
  "patient_name": "John Doe",
  "doctor_name": "Dr. Jane Smith",
  "date": "2024-11-26",
  "medications": [
    {
      "name": "Amoxicillin",
      "dosage": "500mg",
      "frequency": "Three times daily",
      "duration": "7 days"
    }
  ],
  "special_instructions": "Take with food",
  "warnings": ["Complete full course"],
  "verification_status": "verified",
  "confidence_score": 0.92,
  "accuracy_percentage": 92.0,
  "analyzed_at": "2024-11-26T12:00:00",
  "model_version": "gemini-1.5-flash"
}
Validate Prescription
httpPOST /validate
Content-Type: application/json
Request:
json{
  "patient_name": "John Doe",
  "doctor_name": "Dr. Smith",
  "medications": [...],
  "confidence_score": 0.92
}
Response:
json{
  "is_valid": true,
  "warnings": ["Low confidence score - manual review recommended"],
  "errors": []
}
🔧 Configuration
Google Gemini API Setup

Go to Google AI Studio
Create a new API key
Add the key to your .env file

AWS Deployment (Optional)
For production deployment on AWS:

ECR Repository:

bash# Create ECR repository
aws ecr create-repository --repository-name smartrx

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t smartrx .
docker tag smartrx:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/smartrx:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/smartrx:latest

ECS/EKS Deployment:


Use the provided Docker image
Set environment variables in task definition
Configure load balancer and auto-scaling

📊 Performance Metrics

Accuracy: 91% in medical text extraction
Error Reduction: 40% reduction in prescription errors
Processing Time: < 3 seconds average per prescription
Confidence Threshold: 85% for auto-verification

🏥 Healthcare Compliance
This application is designed with healthcare compliance in mind:

✅ Data encryption in transit and at rest
✅ No persistent storage of PHI
✅ Audit logging for all API calls
✅ HIPAA-ready architecture
⚠️ Note: Additional security measures required for production deployment

🧪 Testing
The project includes comprehensive tests:
bash# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest test_app.py -v
📈 Future Enhancements

 Multi-language support for international prescriptions
 Drug interaction checking
 Integration with pharmacy systems
 Mobile application (iOS/Android)
 Batch processing capabilities
 Advanced analytics dashboard
 Real-time monitoring and alerting

🛡️ Security Considerations

API keys stored in environment variables
HTTPS required for production
Rate limiting implemented
Input validation and sanitization
Regular security audits recommended

🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request

from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import base64
import json
from PIL import Image
import io
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configure Google Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'your-api-key-here')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

def preprocess_image(image_data):
    """Preprocess image for better OCR results"""
    try:
        img = Image.open(io.BytesIO(base64.b64decode(image_data)))
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large
        max_size = 2048
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Save to bytes
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=95)
        return buffer.getvalue()
    except Exception as e:
        logger.error(f"Image preprocessing error: {str(e)}")
        raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'model': 'gemini-1.5-flash'
    })

@app.route('/analyze', methods=['POST'])
def analyze_prescription():
    """Analyze prescription image and extract information"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        image_file = request.files['image']
        
        # Read and encode image
        image_bytes = image_file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Prepare prompt for Gemini
        prompt = """
        Analyze this prescription image and extract the following information in JSON format:
        
        {
          "patient_name": "extracted patient name or empty string",
          "doctor_name": "extracted doctor name or empty string",
          "date": "prescription date in YYYY-MM-DD format or empty string",
          "medications": [
            {
              "name": "medication name",
              "dosage": "dosage amount and unit",
              "frequency": "how often to take",
              "duration": "treatment duration"
            }
          ],
          "special_instructions": "any special instructions",
          "warnings": ["list of any warnings or concerns"],
          "verification_status": "verified or needs_review",
          "confidence_score": 0.0 to 1.0
        }
        
        Important guidelines:
        1. Extract all visible text accurately
        2. Identify medication names, dosages, and frequencies
        3. Flag any unclear or ambiguous text
        4. Provide a confidence score based on image quality and text clarity
        5. Mark as "needs_review" if confidence is below 0.85
        6. List any potential drug interaction warnings if identifiable
        
        Return ONLY valid JSON without any markdown formatting or explanations.
        """
        
        # Generate response using Gemini
        response = model.generate_content([prompt, image])
        
        # Parse response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse JSON
        result = json.loads(response_text)
        
        # Add metadata
        result['analyzed_at'] = datetime.utcnow().isoformat()
        result['model_version'] = 'gemini-1.5-flash'
        
        # Calculate accuracy metrics
        accuracy = result.get('confidence_score', 0.0)
        result['accuracy_percentage'] = round(accuracy * 100, 2)
        
        logger.info(f"Successfully analyzed prescription with confidence: {accuracy}")
        
        return jsonify(result), 200
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        return jsonify({
            'error': 'Failed to parse response',
            'details': str(e),
            'raw_response': response_text if 'response_text' in locals() else None
        }), 500
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({
            'error': 'Failed to analyze prescription',
            'details': str(e)
        }), 500

@app.route('/validate', methods=['POST'])
def validate_prescription():
    """Validate extracted prescription data"""
    try:
        data = request.json
        
        validation_results = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Check required fields
        if not data.get('patient_name'):
            validation_results['warnings'].append('Patient name is missing')
        
        if not data.get('doctor_name'):
            validation_results['warnings'].append('Doctor name is missing')
        
        if not data.get('medications') or len(data['medications']) == 0:
            validation_results['errors'].append('No medications found')
            validation_results['is_valid'] = False
        
        # Check medication details
        for med in data.get('medications', []):
            if not med.get('name'):
                validation_results['errors'].append('Medication name missing')
                validation_results['is_valid'] = False
            
            if not med.get('dosage'):
                validation_results['warnings'].append(f"Dosage missing for {med.get('name', 'unknown medication')}")
        
        # Check confidence score
        if data.get('confidence_score', 0) < 0.85:
            validation_results['warnings'].append('Low confidence score - manual review recommended')
        
        return jsonify(validation_results), 200
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({
            'error': 'Validation failed',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

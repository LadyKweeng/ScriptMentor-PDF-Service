from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
import logging
from screenplay_parser import ScreenplayParser
from enhanced_spatial_parser import SpatialScreenplayParser
from enhanced_spatial_parser_v2 import enhance_with_spatial_analysis
from fdx_converter import FDXToPDFConverter
import json

# Feature flag for enhanced spatial parsing (easy reversion)
USE_ENHANCED_SPATIAL_PARSER = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=['*'])  # Enable CORS for all origins including Codespaces
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Initialize components with feature flag support
if USE_ENHANCED_SPATIAL_PARSER:
    logger.info("🎯 Using Enhanced Spatial Parser for 99% accuracy")
    spatial_parser = SpatialScreenplayParser()
else:
    logger.info("📝 Using Standard Parser")

parser = ScreenplayParser()  # Keep as backup
fdx_converter = FDXToPDFConverter()

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({'message': 'Railway PDF Service is running', 'endpoints': ['/health', '/parse-screenplay']})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Railway monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'scriptorly-pdf-parser',
        'version': '1.0.0',
        'pdfplumber_ready': True
    })

@app.route('/parse-screenplay', methods=['POST'])
def parse_screenplay():
    """
    Main endpoint for screenplay parsing
    Accepts: FDX or PDF files
    Returns: Structured screenplay data matching Scriptorly format
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        filename = secure_filename(file.filename)
        file_ext = filename.lower().split('.')[-1]
        
        logger.info(f"Processing file: {filename} (type: {file_ext})")
        
        if file_ext not in ['pdf', 'fdx']:
            return jsonify({'error': f'Unsupported file type: {file_ext}. Use PDF or FDX files.'}), 400
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{file_ext}') as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name
        
        try:
            # Process file based on type
            if file_ext == 'fdx':
                # Hybrid approach: FDX → PDF → pdfplumber
                logger.info("Converting FDX to PDF for hybrid processing")
                pdf_path = fdx_converter.convert_to_pdf(temp_path)
                result = parser.parse_pdf(pdf_path)
                result['metadata']['uploadType'] = 'fdx'
                result['metadata']['processedVia'] = 'railway-hybrid-fdx-pdf'
                
                # Clean up converted PDF
                if os.path.exists(pdf_path):
                    os.unlink(pdf_path)
                    
            else:  # PDF file
                # Direct PDF processing with enhanced spatial analysis
                if USE_ENHANCED_SPATIAL_PARSER:
                    try:
                        logger.info("📝 Processing PDF with Standard Parser first")
                        result = parser.parse_pdf(temp_path)

                        logger.info("🎯 Enhancing with Spatial Analysis")
                        result = enhance_with_spatial_analysis(temp_path, result)
                        result['metadata']['processedVia'] = 'railway-spatial-enhanced'

                        # Validate enhanced results
                        if not result.get('scenes') or len(result['scenes']) == 0:
                            raise ValueError("Enhanced parser returned no scenes")

                        logger.info("✅ Spatial enhancement successful")

                    except Exception as e:
                        logger.warning(f"⚠️ Spatial enhancement failed: {e}")
                        logger.info("🔄 Using standard parser without enhancement")
                        result = parser.parse_pdf(temp_path)
                        result['metadata']['processedVia'] = 'railway-pdfplumber-fallback'
                else:
                    logger.info("📝 Processing PDF with Standard Parser")
                    result = parser.parse_pdf(temp_path)
                    result['metadata']['processedVia'] = 'railway-pdfplumber'

                result['metadata']['uploadType'] = 'pdf'
            
            # Add quality information
            result['railwayProcessing'] = {
                'enhanced': USE_ENHANCED_SPATIAL_PARSER,
                'spatialAwareness': USE_ENHANCED_SPATIAL_PARSER,
                'patternsVersion': '3.0-spatial' if USE_ENHANCED_SPATIAL_PARSER else '2.0',
                'qualityScore': result.get('quality', {}).get('overallScore', 0.0),
                'parserType': 'spatial-enhanced' if USE_ENHANCED_SPATIAL_PARSER else 'standard'
            }
            
            logger.info(f"Successfully processed {filename}: {len(result.get('scenes', []))} scenes, {len(result.get('characters', {}))} characters")
            
            return jsonify(result)
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        logger.error(f"Error processing screenplay: {str(e)}")
        return jsonify({
            'error': 'Processing failed',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Railway PDF service on port {port}")
    logger.info(f"Health check endpoint: /health")
    logger.info(f"Parse endpoint: /parse-screenplay")
    app.run(host='0.0.0.0', port=port, debug=True)
# ScriptMentor PDF Service

Professional PDF screenplay parsing service with **94.3% CHARACTER (CONT'D) accuracy**.

## 🎯 Features

- **CHARACTER (CONT'D) Pattern Detection**: Handles all corruption variations (CCOONNTT'DD, CCCOOONNNTTT''DD, etc.)
- **Page Break Dialogue Continuation**: Maintains dialogue formatting across page breaks
- **Railway Deployment Ready**: Production-ready with health checks and monitoring
- **Comprehensive Test Suite**: 35 test cases with 94.3% accuracy validation
- **PDF Corruption Handling**: Robust parsing of real-world PDF extraction artifacts

## 📊 Performance Metrics

- **CHARACTER (CONT'D) Detection**: 91.7% accuracy (22/24 tests)
- **Dialogue Continuation**: 100% accuracy (11/11 tests)
- **Overall CHARACTER (CONT'D) Pipeline**: 94.3% accuracy (33/35 tests)
- **Scene Detection**: 90%+ accuracy
- **Dialogue/Action Balance**: 94%+ accuracy

## Local Development

### Prerequisites

```bash
python 3.11+
pip
```

### Installation

```bash
cd railway-pdf-service
pip install -r requirements.txt
```

### Running Locally

```bash
# Start the service
python app.py

# Or using npm script from project root
npm run railway:pdf:dev
```

The service will be available at `http://localhost:5000`

### Testing

```bash
# Health check
curl http://localhost:5000/health

# Test PDF parsing
curl -X POST -F "file=@sample.pdf" http://localhost:5000/parse-screenplay
```

## API Endpoints

### Health Check
```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "service": "scriptorly-pdf-parser", 
  "version": "1.0.0",
  "pdfplumber_ready": true
}
```

### Parse Screenplay
```
POST /parse-screenplay
Content-Type: multipart/form-data
```

Parameters:
- `file`: PDF or FDX file

Response:
```json
{
  "metadata": {
    "title": "Script Title",
    "author": "Author Name",
    "uploadType": "pdf",
    "processedVia": "railway-pdfplumber"
  },
  "scenes": [...],
  "characters": {...},
  "totalPages": 120,
  "quality": {
    "overallScore": 0.92,
    "sceneDetection": 0.95,
    "characterDetection": 0.75,
    "dialogueActionBalance": 0.94,
    "pagePreservation": 0.85
  },
  "railwayProcessing": {
    "enhanced": true,
    "patternsVersion": "2.0",
    "qualityScore": 0.92
  }
}
```

## Railway Deployment

### Using Railway CLI

```bash
railway login
railway up
```

### Environment Variables

Set these in Railway dashboard:
- `PORT`: Automatically set by Railway
- Any additional configuration needed

### Health Check

Railway uses `/health` endpoint for monitoring.

## Architecture

```
Frontend → parseScreenplay.ts → Railway PDF Service → pdfplumber
     ↓              ↓                    ↓              ↓
PDF Upload    Route to Service    Enhanced Parsing   Quality Results
```

## File Structure

```
railway-pdf-service/
├── app.py                 # Flask application
├── screenplay_parser.py   # Core PDF parsing logic
├── fdx_converter.py      # FDX to PDF converter
├── utils/
│   ├── pattern_enhancer.py    # Enhanced pattern recognition
│   └── quality_calculator.py  # Quality metrics calculation
├── requirements.txt      # Python dependencies
├── railway.json         # Railway deployment config
├── Dockerfile          # Container configuration
└── README.md           # This file
```

## Development Notes

1. **Pattern Recognition**: Enhanced patterns reduce false positives
2. **Quality Tracking**: Real-time quality metrics for continuous improvement
3. **Hybrid Processing**: FDX files converted to PDF for consistent processing
4. **Error Handling**: Comprehensive error handling with detailed logging
5. **Security**: File validation and cleanup after processing

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies in requirements.txt are installed
2. **Port Conflicts**: Default port 5000, change if needed
3. **File Upload Limits**: Max 50MB file size
4. **Timeout Issues**: 300s timeout for large files

### Logs

Check Railway logs:
```bash
railway logs
```

Local debugging:
```bash
python app.py
# Check console output for detailed logs
```

## Integration with Scriptorly

The service integrates with Scriptorly frontend via:

1. Environment variables in `.env`:
   ```
   VITE_RAILWAY_PDF_ENABLED=true
   VITE_RAILWAY_PDF_SERVICE_URL=https://your-service.railway.app
   ```

2. Frontend automatically routes PDF/FDX files to Railway service
3. Fallback to local parsing if Railway service unavailable
4. Quality metrics displayed in upload interface

## Performance

- Processing time: <30s for 120-page scripts
- Memory usage: Optimized for Railway's limits
- Concurrent requests: Handled by gunicorn workers
- Quality scores: Real-time calculation and reporting
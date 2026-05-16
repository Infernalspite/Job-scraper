# Setup Guide - Job-Scraper Frontend

## 📋 Prerequisites

Before setting up the frontend, ensure you have:
- Python 3.8 or higher
- pip package manager
- A modern web browser (Chrome, Firefox, Safari, Edge)

## 🛠️ Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Key packages installed:
- **flask** - Web framework
- **PyPDF2** - PDF processing
- **sentence-transformers** - AI semantic matching
- **spacy** - NLP processing
- **openpyxl** - Excel generation

### 2. Download Spacy Language Model

```bash
python -m spacy download en_core_web_sm
```

This downloads the English language model for NLP processing (~40MB).

## 🚀 Running the Application

### Development Mode

```bash
python app.py
```

You'll see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Production Mode

```bash
export FLASK_ENV=production
flask run --host=0.0.0.0 --port=5000
```

## 🌐 Accessing the Frontend

1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. You should see the Job-Scraper interface

## 📁 Project Structure

```
Job-scraper/
├── app.py                    # Flask server
├── main.py                   # CLI alternative
├── requirements.txt          # Dependencies
├── config.py                 # Configuration
├── templates/
│   └── index.html           # HTML interface
├── static/
│   ├── css/
│   │   └── style.css        # Styles
│   └── js/
│       └── app.js           # JavaScript logic
└── uploads/                 # Uploaded resumes (auto-created)
```

## ⚙️ Configuration

### Default Settings (config.py)

```python
# Location preference if not detected from resume
LOCATION_PREFERENCE = "San Francisco"

# Minimum match score threshold
MIN_MATCH_SCORE = 0.3

# Job search keywords
SEARCH_KEYWORDS = ["python", "machine learning", "data"]
```

### Custom Configuration

Edit `config.py` to adjust:
- Default location
- Minimum match threshold
- Search keywords
- Job sources
- Export settings

## 🎯 Usage Workflow

### Step 1: Upload Resume
1. Click the upload area or drag-and-drop a PDF
2. System extracts role, location, and skills
3. Review extracted information

### Step 2: Fetch Jobs
1. Click "Fetch Jobs" button
2. System scrapes from configured sources
3. View job statistics per source

### Step 3: Match Jobs
1. Click "Match Jobs" button
2. AI analyzes job descriptions
3. Generates match scores

### Step 4: Export
1. Click "Download Excel" button
2. Excel file downloads to your computer
3. Contains all matched jobs with scores

## 🔌 API Endpoints

### Upload Resume
```bash
POST /api/upload-resume
Content-Type: multipart/form-data

Response: {
  "success": true,
  "resume_data": {
    "role": "Data Scientist",
    "location": "San Francisco",
    "skills": ["python", "machine learning", ...]
  },
  "filename": "resume.pdf"
}
```

### Fetch Jobs
```bash
POST /api/fetch-jobs

Response: {
  "success": true,
  "jobs": [...],
  "total_jobs": 500,
  "source_counts": {
    "LinkedIn": 200,
    "Indeed": 300
  }
}
```

### Match Jobs
```bash
POST /api/match-jobs
Content-Type: application/json

Body: {
  "resume_data": {...},
  "jobs": [...]
}

Response: {
  "success": true,
  "matched_jobs": [...],
  "match_count": 45
}
```

### Export Excel
```bash
POST /api/export-excel
Content-Type: application/json

Body: {
  "matched_jobs": [...]
}

Response: Binary Excel file
```

## 🖥️ System Requirements

### Minimum
- CPU: 2-core processor
- RAM: 4 GB
- Storage: 2 GB free space
- Network: Internet connection for job fetching

### Recommended
- CPU: 4-core processor or better
- RAM: 8 GB or more
- Storage: 5 GB SSD
- Network: Broadband connection

## ⏱️ Performance Notes

- **First Run**: Takes 5-10 minutes (downloading AI models)
- **Resume Upload**: 1-5 seconds
- **Job Fetching**: 2-5 minutes (depends on sources)
- **Job Matching**: 1-3 minutes (depends on job count)
- **Excel Export**: 5-10 seconds

## 🐛 Troubleshooting

### Port 5000 Already in Use
```bash
# Check what's using port 5000
lsof -i :5000

# Use a different port
export FLASK_PORT=5001
python app.py
```

### ModuleNotFoundError
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
python -m spacy download en_core_web_sm
```

### Resume Upload Fails
- Ensure PDF file is readable
- File size must be < 10 MB
- Check file is valid PDF format

### No Jobs Matched
- Lower `MIN_MATCH_SCORE` in config.py
- Review resume for clarity
- Check job sources are configured

### Frontend not Loading
- Verify Flask server is running
- Check http://localhost:5000 in browser
- Check browser console for errors (F12)

## 🔐 Security Considerations

- Uploaded resumes stored in `uploads/` folder
- Implement file validation before processing
- Use HTTPS in production
- Sanitize user inputs

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [Spacy NLP](https://spacy.io/)
- [PyPDF2 Guide](https://pypdf.readthedocs.io/)

## 🚀 Deployment Options

### Local Development
```bash
python app.py
```

### Docker (Recommended)
```bash
docker build -t job-scraper .
docker run -p 5000:5000 job-scraper
```

### Cloud Platforms
- **Heroku**: Push to Heroku using Git
- **AWS**: Deploy to EC2 or Elastic Beanstalk
- **Google Cloud**: Deploy to App Engine
- **Azure**: Deploy to App Service

## 📧 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review GitHub Issues
3. Create a new issue with details

---

**Last Updated**: 2026-05-16
**Version**: 1.0.0

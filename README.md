# Job Scraper - AI-Powered Job Matching

A sophisticated Python application that intelligently scrapes jobs from multiple sources, parses your resume using AI, and matches you with the best job opportunities.

## 🌟 Key Features

### 📄 Resume Processing
- **PDF Parsing**: Extract text from PDF resumes
- **Smart NLP**: Extract role, location, and skills
- **AI Analysis**: LLM-based resume understanding

### 🔍 Job Scraping
- **Multi-Source**: LinkedIn, Indeed, Glassdoor, and more
- **Deduplication**: Remove duplicate listings
- **Data Export**: Save to CSV or Excel

### 🤖 AI Job Matching
- **Semantic Analysis**: Sentence transformers for intelligent matching
- **Match Scoring**: Calculate relevance percentage (0-100%)
- **Smart Filtering**: Role and location-based filtering

### 💻 Web Interface
- **User-Friendly**: Modern, responsive design
- **Drag & Drop**: Easy resume upload
- **4-Step Workflow**: Simple, intuitive process
- **Excel Export**: Download results professionally formatted

## 📦 Requirements

- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Run Application
```bash
python app.py
```

### 3. Access Web Interface
Open browser to: **http://localhost:5000**

### 4. Follow 4-Step Process
1. **Upload** your PDF resume
2. **Fetch** jobs from multiple sources
3. **Match** jobs using AI
4. **Export** results to Excel

## 📁 Project Structure

```
Job-Scraper/
├── app.py                 # Flask web server
├── main.py                # CLI entry point
├── config.py              # Configuration
├── requirements.txt       # Dependencies
│
├── Core Modules:
├── pdf_reader.py          # PDF extraction
├── resume_parser.py       # Resume analysis
├── slm_resume_reader.py   # LLM parsing
├── job_fetcher.py         # Job scraping
├── deduplicator.py        # Deduplication
├── matcher.py             # AI matching
├── exporter.py            # Excel export
├── database.py            # Database
│
├── Frontend:
├── templates/index.html   # Web interface
├── static/css/style.css   # Styling
└── static/js/app.js       # JavaScript
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
LOCATION_PREFERENCE = "San Francisco"
MIN_MATCH_SCORE = 0.3
SEARCH_KEYWORDS = ["python", "machine learning"]
JOB_SOURCES = ["linkedin", "indeed"]
```

## 🎯 Usage

### Web Interface (Recommended)
```bash
python app.py
# Visit http://localhost:5000
```

### Command Line
```bash
python main.py
# Reads from: data/resume.pdf
# Outputs: matched_jobs.xlsx
```

## 🔌 API Endpoints

### POST /api/upload-resume
Upload and parse resume PDF

### POST /api/fetch-jobs
Fetch jobs from configured sources

### POST /api/match-jobs
Run AI matching algorithm

### POST /api/export-excel
Export matched jobs to Excel

### GET /api/health
Health check endpoint

## 🧠 How It Works

1. **Resume Processing**
   - Extract text from PDF
   - Use NLP to identify role, skills, location

2. **Job Fetching**
   - Query multiple job boards
   - Collect job details
   - Remove duplicates

3. **AI Matching**
   - Convert resume to semantic embeddings
   - Compare with all job descriptions
   - Calculate match scores

4. **Export**
   - Sort by match score
   - Generate Excel file
   - Include all job details

## ⏱️ Performance

- **Resume Upload**: 1-5 seconds
- **Job Fetching**: 2-5 minutes
- **AI Matching**: 1-3 minutes
- **Excel Export**: 5-10 seconds

## 📚 Technology Stack

- **Backend**: Flask, Python 3.8+
- **NLP**: Spacy, Sentence Transformers
- **PDF**: PyPDF2
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Export**: OpenPyXL

## 🐛 Troubleshooting

### Port Already in Use
```bash
export FLASK_PORT=5001
python app.py
```

### Resume Not Parsing
- Ensure PDF contains readable text (not scanned image)
- File must be < 10 MB
- Verify PDF format is valid

### No Jobs Matched
- Lower `MIN_MATCH_SCORE` in config.py
- Update job sources
- Review resume clarity

### Slow Performance
- First run downloads AI models (~5 minutes)
- Use SSD for faster processing
- Increase RAM for better performance

## 🔐 Security & Privacy

- All processing happens locally
- Resumes stored in local uploads folder
- No data sent to external servers
- No tracking or analytics

## 📖 Documentation

- **SETUP_GUIDE.md** - Detailed setup instructions
- **API Documentation** - REST API reference
- **Configuration Guide** - Config options

## 🤝 Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch
3. Submit pull request

## 📝 License

MIT License - Free to use and modify

## 📧 Support

For issues or questions:
- Check troubleshooting section
- Review GitHub Issues
- Create new issue with details

---

**Version**: 1.0.0  
**Status**: Active Development  
**Last Updated**: 2026-05-16

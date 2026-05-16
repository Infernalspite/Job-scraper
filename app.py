from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import sys
import tempfile

# Add project root to path so modules package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.pdf_reader import extract_text_from_pdf
from modules.slm_resume_reader import parse_resume_smart
from modules.job_fetcher import fetch_all_jobs
from modules.deduplicator import remove_duplicates
from modules.matcher import match_jobs
from modules.exporter import export_to_excel
from config import LOCATION_PREFERENCE

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Handle resume file upload and parsing"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF files are allowed'}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        print(f"Reading resume from {filepath}...")
        text = extract_text_from_pdf(filepath)

        print("Parsing resume...")
        resume_data = parse_resume_smart(text)

        if not resume_data.get("location"):
            resume_data["location"] = LOCATION_PREFERENCE

        return jsonify({
            'success': True,
            'resume_data': resume_data,
            'filename': filename
        })

    except Exception as e:
        print(f"Error uploading resume: {str(e)}")
        return jsonify({'error': f'Failed to process resume: {str(e)}'}), 500


@app.route('/api/fetch-jobs', methods=['POST'])
def fetch_jobs():
    """Fetch jobs from configured sources"""
    try:
        print("Fetching jobs...")
        jobs, counts = fetch_all_jobs()

        print("Removing duplicates...")
        jobs = remove_duplicates(jobs)

        return jsonify({
            'success': True,
            'jobs': jobs[:100],
            'total_jobs': len(jobs),
            'source_counts': counts
        })

    except Exception as e:
        print(f"Error fetching jobs: {str(e)}")
        return jsonify({'error': f'Failed to fetch jobs: {str(e)}'}), 500


@app.route('/api/match-jobs', methods=['POST'])
def match_jobs_route():
    """Match jobs with resume"""
    try:
        data = request.json
        resume_data = data.get('resume_data')
        jobs = data.get('jobs')

        if not resume_data or not jobs:
            return jsonify({'error': 'Missing resume data or jobs'}), 400

        print("Matching jobs using AI...")
        matched_jobs = match_jobs(jobs, resume_data)

        return jsonify({
            'success': True,
            'matched_jobs': matched_jobs,
            'match_count': len(matched_jobs)
        })

    except Exception as e:
        print(f"Error matching jobs: {str(e)}")
        return jsonify({'error': f'Failed to match jobs: {str(e)}'}), 500


@app.route('/api/export-excel', methods=['POST'])
def export_excel():
    """Export matched jobs to Excel"""
    try:
        data = request.json
        matched_jobs = data.get('matched_jobs')

        if not matched_jobs:
            return jsonify({'error': 'No jobs to export'}), 400

        print("Exporting to Excel...")
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            tmp_path = tmp.name

        export_to_excel(matched_jobs, tmp_path)

        return send_file(
            tmp_path,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='matched_jobs.xlsx'
        )

    except Exception as e:
        print(f"Error exporting to Excel: {str(e)}")
        return jsonify({'error': f'Failed to export: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

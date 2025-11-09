# Job Search & AI Keyword Analysis Toolkit

A comprehensive Model Context Protocol (MCP) server for GitHub Copilot that provides job search functionality, PDF analysis, and AI-powered keyword generation using Google Gemini 2.0 Flash.

## 🚀 Features

### Multi-Platform Job Search
- **LinkedIn Simulation**: High-quality simulated LinkedIn job data with realistic company and salary information
- **The Muse Jobs API**: Live job data from real companies like Meta, Google, Atlassian, TikTok
- **Intelligent Fallbacks**: Market-accurate job generation when APIs are unavailable
- **Combined Search**: Aggregated results from multiple sources with deduplication

### AI-Powered PDF & Keyword Analysis
- **PDF Parser**: Extract text and structured data from PDF documents
- **Gemini AI Integration**: Advanced keyword extraction using Google's Gemini 2.0 Flash
- **Job Matching**: Compare resumes against job descriptions
- **ATS Optimization**: Optimize documents for Applicant Tracking Systems
- **Industry Research**: Generate industry-specific keywords and trends

### GitHub Copilot Ready
- **MCP Compatible**: All functions work seamlessly with GitHub Copilot
- **Structured JSON**: Standardized response format for AI consumption
- **Async Support**: Real-time job searching capabilities
- **Error Handling**: Robust fallback mechanisms

## 📁 Project Structure

```
/
├── mcp_server.py              # Main MCP server with all tools
├── job_searcher.py            # Job search APIs and generation
├── job_saver.py               # JSON format job saving utility
├── pdf_parser.py              # PDF text extraction and analysis
├── keyword_generator.py       # AI-powered keyword generation
├── demo.py                    # Job search system demonstration
├── keyword_demo.py            # Keyword tools demonstration  
├── gemini_pdf_demo.py         # PDF + AI analysis demo
├── keyword_tools_guide.md     # Comprehensive usage guide
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration
└── job_search_results/        # Saved search results (JSON)
```

## 🛠 Quick Start

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (add your Gemini API key)
# GEMINI_API_KEY=your_api_key_here
```

### Basic Usage
```bash
# Test job search system
python demo.py

# Test keyword generation tools
python keyword_demo.py

# Test PDF analysis with AI
python gemini_pdf_demo.py

# Start MCP server for GitHub Copilot
python mcp_server.py
```

## 🔧 Available MCP Tools

### Job Search
- **`search_linkedin_jobs`** - LinkedIn-style job simulation
- **`search_muse_jobs`** - The Muse API + realistic fallbacks  
- **`search_combined_jobs`** - Combined platform search

### PDF Processing
- **`parse_pdf_document`** - Full PDF analysis with metadata
- **`extract_pdf_text`** - Extract text only from PDFs
- **`batch_parse_pdfs`** - Process multiple PDFs
- **`extract_job_keywords_from_pdf`** - AI-powered PDF keyword extraction

### AI Keyword Generation
- **`generate_keywords_from_text`** - Extract keywords from text
- **`generate_keywords_from_pdf`** - Extract keywords from PDFs
- **`generate_job_match_keywords`** - Compare job vs resume
- **`generate_industry_keywords`** - Industry-specific terms
- **`optimize_keywords_for_ats`** - ATS optimization

## 💡 Use Cases

### Job Search Optimization
```bash
# Find jobs and analyze them
python -c "
from keyword_generator import KeywordGenerator
generator = KeywordGenerator()

# Analyze job description
job_keywords = generator.generate_keywords_from_text(job_description, 'job_description')

# Compare with your resume
match_analysis = generator.generate_job_match_keywords(job_description, resume_text)

# Get ATS optimization tips
ats_tips = generator.optimize_keywords_for_ats(resume_text, 'target_job_title')
"
```

### Industry Research
```bash
# Research industry keywords
python keyword_demo.py
```

### PDF Document Analysis
```bash
# Analyze PDFs with AI
python gemini_pdf_demo.py
```

## 📊 Job Data Format

All jobs are saved in a standardized JSON format:

```json
{
  "search_metadata": {
    "query": {"keywords": "data scientist", "location": "California", "limit": 30},
    "total_results": 26,
    "collected_at": "2025-11-08T17:46:27.760114",
    "source": "job_search_mcp_server"
  },
  "jobs": [
    {
      "company": "Meta",
      "position": "Senior Data Scientist",
      "apply_link": "https://linkedin.com/jobs/view/linkedin_1",
      "location": "California",
      "salary": "$120,000 - $180,000",
      "description": "We are seeking a talented Senior Data Scientist...",
      "requirements": "SQL, Python, Machine Learning, Statistics",
      "benefits": "Health insurance, 401k, Stock options, Flexible PTO",
      "job_type": "full_time",
      "experience_level": "senior_level",
      "posted_date": "2025-11-08",
      "deadline": null,
      "days_since_posted": 3,
      "remote_option": "onsite",
      "visa_sponsorship": true,
      "source": "linkedin/linkedin_1",
      "collection_method": "mcp_linkedin_simulation",
      "collected_at": "2025-11-08T17:46:27.760075",
      "field": "Data Science",
      "company_type": "big_tech"
    }
  ]
}
```

## 🤖 AI Keyword Analysis Format

AI keyword extraction provides structured analysis:

```json
{
  "technical_skills": ["Python", "AWS", "Docker"],
  "soft_skills": ["Communication", "Leadership"],
  "programming_languages": ["Python", "JavaScript"],
  "tools_technologies": ["TensorFlow", "React"],
  "job_titles": ["Data Scientist", "ML Engineer"],
  "companies": ["Google", "Microsoft"],
  "certifications": ["AWS Certified"],
  "industries": ["Technology", "Finance"],
  "document_summary": "Brief description of content",
  "match_score": "75%",
  "ats_score": "8/10",
  "generated_at": "2025-11-08T20:00:00"
}
```

## 🔑 Environment Setup

Required environment variables in `.env`:

```env
# Google Gemini AI API Key
GEMINI_API_KEY=your_gemini_api_key_here

# LinkedIn Credentials (optional for enhanced simulation)
LINKEDIN_EMAIL=your_email@gmail.com
LINKEDIN_PASSWORD=your_password
```

## 📚 Documentation

- **Keyword Tools Guide**: `keyword_tools_guide.md` - Comprehensive usage documentation
- **Demo Scripts**: Run any `*_demo.py` file for interactive examples
- **API Reference**: Check `mcp_server.py` for all available tools

## ✅ Ready for Production

This toolkit is production-ready and GitHub Copilot compatible! 🚀

### Quick Test
```bash
# Test all functionality
python demo.py && python keyword_demo.py && python gemini_pdf_demo.py
```

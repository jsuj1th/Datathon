# AI-Powered Keyword Generation Tools

## Overview

The keyword generation tools use Google's Gemini 2.0 Flash model to extract and analyze job-relevant keywords from various sources. These tools are perfect for optimizing resumes, analyzing job descriptions, and improving your job search strategy.

## 🚀 Quick Start

### Setup
1. Get your Gemini API key: https://makersuite.google.com/app/apikey
2. Add it to your `.env` file: `GEMINI_API_KEY=your_actual_key_here`
3. Install dependencies: `pip install google-generativeai python-dotenv`

### Basic Usage
```python
from keyword_generator import KeywordGenerator

generator = KeywordGenerator()
result = generator.generate_keywords_from_text(text, "resume")
print(result)
```

## 🛠️ Available Tools

### 1. Text Keyword Extraction
```python
generate_keywords_from_text(text, context="general")
```
- **Purpose**: Extract keywords from any text
- **Contexts**: `job_description`, `resume`, `cover_letter`, `general`
- **Use Case**: Analyze job postings or resume content

**Example:**
```python
job_text = "Senior Data Scientist with Python and ML experience..."
result = generator.generate_keywords_from_text(job_text, "job_description")
```

### 2. PDF Keyword Extraction
```python
generate_keywords_from_pdf(file_path, context="auto")
```
- **Purpose**: Extract keywords directly from PDF files
- **Auto-detection**: Automatically detects if it's a resume, job description, etc.
- **Use Case**: Process PDF resumes or job descriptions

**Example:**
```python
result = generator.generate_keywords_from_pdf("resume.pdf", "auto")
```

### 3. Job Matching Analysis
```python
generate_job_match_keywords(job_description, resume_text)
```
- **Purpose**: Compare job requirements with your resume
- **Output**: Match score, missing keywords, recommendations
- **Use Case**: Optimize resume for specific job applications

**Example:**
```python
result = generator.generate_job_match_keywords(job_desc, resume)
# Result includes: match_score, missing_keywords, recommended_additions
```

### 4. Industry-Specific Keywords
```python
generate_industry_keywords(industry, role="")
```
- **Purpose**: Get comprehensive industry and role-specific keywords
- **Industries**: technology, healthcare, finance, etc.
- **Use Case**: Research industry trends and requirements

**Example:**
```python
result = generator.generate_industry_keywords("technology", "data scientist")
# Get tech industry keywords specifically for data science roles
```

### 5. ATS Optimization
```python
optimize_keywords_for_ats(text, target_job="")
```
- **Purpose**: Optimize content for Applicant Tracking Systems
- **Output**: ATS score, optimization recommendations
- **Use Case**: Make your resume ATS-friendly

**Example:**
```python
result = generator.optimize_keywords_for_ats(resume_text, "Software Engineer")
# Get ATS optimization tips and keyword recommendations
```

## 📊 Output Format

All tools return structured JSON with relevant categories:

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
  "keywords": ["Machine Learning", "API"],
  "document_summary": "Brief description of content",
  "generated_at": "2025-11-08T17:45:00"
}
```

## 🎯 Use Cases

### Resume Optimization
1. **Extract keywords** from target job descriptions
2. **Analyze your resume** to see current keywords
3. **Compare and optimize** using job matching analysis
4. **ATS optimize** your final resume

### Job Search Strategy
1. **Research industry keywords** for your field
2. **Analyze multiple job postings** to find common requirements
3. **Track trending skills** and technologies
4. **Tailor applications** for each position

### Career Development
1. **Identify skill gaps** in your target roles
2. **Discover certification opportunities**
3. **Learn industry terminology** and buzzwords
4. **Plan learning roadmap** based on market demands

## 🔧 MCP Server Integration

All tools are available through the MCP server:

```bash
# Start the MCP server
python mcp_server.py
```

Available endpoints:
- `generate_keywords_from_text`
- `generate_keywords_from_pdf`  
- `generate_job_match_keywords`
- `generate_industry_keywords`
- `optimize_keywords_for_ats`

## 📝 Demo Scripts

### Run Full Demo
```bash
python keyword_demo.py
```
Shows all keyword generation capabilities with sample data.

### Test Individual Tools
```bash
python keyword_generator.py
```
Quick test of basic functionality.

## 💡 Tips for Best Results

### For Job Descriptions
- Use `context="job_description"` for better extraction
- Focus on requirements and qualifications sections
- Extract both technical and soft skills

### For Resumes
- Use `context="resume"` for optimal analysis
- Include all sections (experience, education, skills)
- Pay attention to action verbs and achievements

### For Job Matching
- Use complete job descriptions and full resume text
- Review missing keywords carefully
- Focus on high-impact recommended additions

### For ATS Optimization
- Aim for ATS score of 7+ out of 10
- Include variations of important keywords
- Use standard section headers (Experience, Education, Skills)

## ⚠️ Important Notes

- **API Costs**: Monitor your Gemini API usage
- **Rate Limits**: Respect API rate limits for batch processing
- **Data Privacy**: Don't include sensitive information in prompts
- **Accuracy**: AI suggestions should be reviewed and validated

## 🚀 Advanced Usage

### Batch Processing
```python
# Process multiple files
results = []
for file in pdf_files:
    result = generator.generate_keywords_from_pdf(file)
    results.append(result)
```

### Save Results
```python
# Save keywords for later analysis
file_path = generator.save_keywords(result, "analysis_results.json")
```

### Custom Analysis
```python
# Combine multiple tools for comprehensive analysis
job_keywords = generator.generate_keywords_from_text(job_desc, "job_description")
resume_keywords = generator.generate_keywords_from_text(resume, "resume")
match_analysis = generator.generate_job_match_keywords(job_desc, resume)
ats_optimization = generator.optimize_keywords_for_ats(resume, job_title)
```

## 📞 Support

- Check your `.env` file for correct API key
- Ensure all dependencies are installed
- Review error messages for specific issues
- Test with sample data first

---

**Next Steps**: Use these tools to enhance your job search strategy and optimize your application materials for better results!

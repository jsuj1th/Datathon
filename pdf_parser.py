#!/usr/bin/env python3
"""
PDF Parser Tool
A comprehensive tool for parsing and extracting information from PDF files.
Useful for job applications, resumes, job descriptions, and other documents.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

try:
    import PyPDF2
    import pdfplumber
    import fitz  # PyMuPDF
    PDF_LIBS_AVAILABLE = True
except ImportError:
    PDF_LIBS_AVAILABLE = False
    print("⚠️  PDF libraries not installed. Run 'pip install PyPDF2 pdfplumber PyMuPDF' to enable PDF parsing.")

# Gemini AI integration
try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    GEMINI_AVAILABLE = True
    # Load environment variables
    load_dotenv()
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  Gemini AI not installed. Run 'pip install google-generativeai python-dotenv' to enable AI keyword extraction.")

class PDFParser:
    """
    A comprehensive PDF parser that can extract text, metadata, and structured information
    from PDF files using multiple parsing libraries for best results.
    """
    
    def __init__(self):
        self.supported_extensions = ['.pdf']
        self.gemini_model = None
        
        # Initialize Gemini AI if available
        if GEMINI_AVAILABLE:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key and api_key != 'your_gemini_api_key_here':
                try:
                    genai.configure(api_key=api_key)
                    self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
                    print("✅ Gemini 2.5 Flash initialized successfully")
                except Exception as e:
                    print(f"⚠️  Failed to initialize Gemini AI: {e}")
            else:
                print("⚠️  GEMINI_API_KEY not found in .env file. Add your API key to enable AI keyword extraction.")
        
    def parse_pdf(self, file_path: str, method: str = "auto") -> Dict[str, Any]:
        """
        Parse a PDF file and extract comprehensive information.
        
        Args:
            file_path: Path to the PDF file
            method: Parsing method ('pypdf2', 'pdfplumber', 'pymupdf', 'auto')
            
        Returns:
            Dictionary containing extracted information
        """
        if not PDF_LIBS_AVAILABLE:
            raise ImportError("PDF libraries not installed. Run 'pip install PyPDF2 pdfplumber PyMuPDF'")
            
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")
            
        if file_path.suffix.lower() not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        result = {
            "file_info": {
                "filename": file_path.name,
                "file_path": str(file_path),
                "file_size": file_path.stat().st_size,
                "parsed_at": datetime.now().isoformat()
            },
            "metadata": {},
            "content": {
                "raw_text": "",
                "pages": [],
                "page_count": 0
            },
            "structured_data": {},
            "parsing_method": method
        }
        
        try:
            if method == "auto":
                # Try different methods and use the best result
                result.update(self._parse_with_best_method(file_path))
            elif method == "pypdf2":
                result.update(self._parse_with_pypdf2(file_path))
            elif method == "pdfplumber":
                result.update(self._parse_with_pdfplumber(file_path))
            elif method == "pymupdf":
                result.update(self._parse_with_pymupdf(file_path))
            else:
                raise ValueError(f"Unknown parsing method: {method}")
                
            # Extract structured information
            result["structured_data"] = self._extract_structured_data(result["content"]["raw_text"])
            
        except Exception as e:
            result["error"] = str(e)
            print(f"❌ Error parsing PDF: {e}")
            
        return result
    
    def _parse_with_best_method(self, file_path: Path) -> Dict[str, Any]:
        """Try different parsing methods and return the best result."""
        methods = ["pdfplumber", "pymupdf", "pypdf2"]
        best_result = None
        best_score = 0
        
        for method in methods:
            try:
                if method == "pdfplumber":
                    result = self._parse_with_pdfplumber(file_path)
                elif method == "pymupdf":
                    result = self._parse_with_pymupdf(file_path)
                elif method == "pypdf2":
                    result = self._parse_with_pypdf2(file_path)
                
                # Score based on text length and quality
                text_length = len(result.get("content", {}).get("raw_text", ""))
                score = text_length
                
                if score > best_score:
                    best_score = score
                    best_result = result
                    best_result["parsing_method"] = method
                    
            except Exception as e:
                print(f"⚠️  Method {method} failed: {e}")
                continue
        
        return best_result or {"content": {"raw_text": "", "pages": [], "page_count": 0}}
    
    def _parse_with_pypdf2(self, file_path: Path) -> Dict[str, Any]:
        """Parse PDF using PyPDF2."""
        result = {"content": {"raw_text": "", "pages": [], "page_count": 0}, "metadata": {}}
        
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Extract metadata
            if reader.metadata:
                result["metadata"] = {
                    "title": reader.metadata.get('/Title', ''),
                    "author": reader.metadata.get('/Author', ''),
                    "subject": reader.metadata.get('/Subject', ''),
                    "creator": reader.metadata.get('/Creator', ''),
                    "producer": reader.metadata.get('/Producer', ''),
                    "creation_date": str(reader.metadata.get('/CreationDate', '')),
                    "modification_date": str(reader.metadata.get('/ModDate', ''))
                }
            
            # Extract text from all pages
            pages = []
            for i, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    pages.append({
                        "page_number": i + 1,
                        "text": page_text,
                        "char_count": len(page_text)
                    })
                except Exception as e:
                    pages.append({
                        "page_number": i + 1,
                        "text": "",
                        "error": str(e)
                    })
            
            result["content"]["pages"] = pages
            result["content"]["page_count"] = len(pages)
            result["content"]["raw_text"] = "\n\n".join([p["text"] for p in pages])
        
        return result
    
    def _parse_with_pdfplumber(self, file_path: Path) -> Dict[str, Any]:
        """Parse PDF using pdfplumber (best for tables and structured content)."""
        result = {"content": {"raw_text": "", "pages": [], "page_count": 0}, "metadata": {}}
        
        with pdfplumber.open(file_path) as pdf:
            # Extract metadata
            if pdf.metadata:
                result["metadata"] = {
                    "title": pdf.metadata.get('Title', ''),
                    "author": pdf.metadata.get('Author', ''),
                    "subject": pdf.metadata.get('Subject', ''),
                    "creator": pdf.metadata.get('Creator', ''),
                    "producer": pdf.metadata.get('Producer', ''),
                    "creation_date": str(pdf.metadata.get('CreationDate', '')),
                    "modification_date": str(pdf.metadata.get('ModDate', ''))
                }
            
            # Extract text and tables from all pages
            pages = []
            for i, page in enumerate(pdf.pages):
                try:
                    page_text = page.extract_text() or ""
                    
                    # Try to extract tables
                    tables = []
                    try:
                        page_tables = page.extract_tables()
                        for table in page_tables or []:
                            if table:
                                tables.append(table)
                    except:
                        pass
                    
                    pages.append({
                        "page_number": i + 1,
                        "text": page_text,
                        "char_count": len(page_text),
                        "tables": tables,
                        "table_count": len(tables)
                    })
                except Exception as e:
                    pages.append({
                        "page_number": i + 1,
                        "text": "",
                        "error": str(e)
                    })
            
            result["content"]["pages"] = pages
            result["content"]["page_count"] = len(pages)
            result["content"]["raw_text"] = "\n\n".join([p["text"] for p in pages if p["text"]])
        
        return result
    
    def _parse_with_pymupdf(self, file_path: Path) -> Dict[str, Any]:
        """Parse PDF using PyMuPDF (best for complex layouts and images)."""
        result = {"content": {"raw_text": "", "pages": [], "page_count": 0}, "metadata": {}}
        
        doc = fitz.open(file_path)
        
        # Extract metadata
        metadata = doc.metadata
        if metadata:
            result["metadata"] = {
                "title": metadata.get('title', ''),
                "author": metadata.get('author', ''),
                "subject": metadata.get('subject', ''),
                "creator": metadata.get('creator', ''),
                "producer": metadata.get('producer', ''),
                "creation_date": metadata.get('creationDate', ''),
                "modification_date": metadata.get('modDate', '')
            }
        
        # Extract text from all pages
        pages = []
        for page_num in range(doc.page_count):
            try:
                page = doc[page_num]
                page_text = page.get_text()
                
                # Get page dimensions
                rect = page.rect
                
                pages.append({
                    "page_number": page_num + 1,
                    "text": page_text,
                    "char_count": len(page_text),
                    "width": rect.width,
                    "height": rect.height
                })
            except Exception as e:
                pages.append({
                    "page_number": page_num + 1,
                    "text": "",
                    "error": str(e)
                })
        
        result["content"]["pages"] = pages
        result["content"]["page_count"] = len(pages)
        result["content"]["raw_text"] = "\n\n".join([p["text"] for p in pages if p["text"]])
        
        doc.close()
        return result
    
    def _extract_structured_data(self, text: str) -> Dict[str, Any]:
        """Extract structured information from the raw text."""
        structured = {
            "emails": self._extract_emails(text),
            "phone_numbers": self._extract_phone_numbers(text),
            "urls": self._extract_urls(text),
            "dates": self._extract_dates(text),
            "skills": self._extract_potential_skills(text),
            "companies": self._extract_potential_companies(text),
            "statistics": {
                "word_count": len(text.split()),
                "character_count": len(text),
                "line_count": len(text.split('\n'))
            }
        }
        
        # Try to detect document type
        structured["document_type"] = self._detect_document_type(text)
        
        # Add AI-powered keyword extraction if Gemini is available
        if self.gemini_model:
            structured["ai_keywords"] = self._extract_keywords_with_gemini(text)
            structured["ai_analysis"] = self._analyze_document_with_gemini(text)
        else:
            structured["ai_keywords"] = []
            structured["ai_analysis"] = "Gemini AI not available"
        
        return structured
    
    def _extract_keywords_with_gemini(self, text: str) -> Dict[str, Any]:
        """Extract keywords using Gemini AI."""
        if not self.gemini_model:
            return {"error": "Gemini AI not available"}
        
        try:
            prompt = f"""
            Analyze the following document text and extract relevant keywords and information. 
            Please provide a JSON response with the following structure:
            {{
                "technical_skills": ["list of technical skills found"],
                "soft_skills": ["list of soft skills found"],
                "job_titles": ["list of job titles or positions mentioned"],
                "companies": ["list of companies or organizations mentioned"],
                "education": ["list of educational qualifications or institutions"],
                "certifications": ["list of certifications or credentials"],
                "programming_languages": ["list of programming languages"],
                "tools_technologies": ["list of tools and technologies"],
                "industries": ["list of industries or domains"],
                "keywords": ["list of other relevant keywords"],
                "document_summary": "brief summary of the document content"
            }}
            
            Document text:
            {text[:4000]}  # Limit text to avoid token limits
            """
            
            response = self.gemini_model.generate_content(prompt)
            
            # Try to parse the JSON response
            try:
                # Clean the response text and extract JSON
                response_text = response.text.strip()
                if response_text.startswith('```json'):
                    response_text = response_text[7:]
                if response_text.endswith('```'):
                    response_text = response_text[:-3]
                
                keywords_data = json.loads(response_text.strip())
                return keywords_data
                
            except json.JSONDecodeError:
                # If JSON parsing fails, return the raw response
                return {
                    "raw_response": response.text,
                    "error": "Failed to parse AI response as JSON"
                }
                
        except Exception as e:
            return {
                "error": f"Gemini API error: {str(e)}"
            }
    
    def _analyze_document_with_gemini(self, text: str) -> Dict[str, Any]:
        """Analyze document type and purpose using Gemini AI."""
        if not self.gemini_model:
            return {"error": "Gemini AI not available"}
        
        try:
            prompt = f"""
            Analyze this document and provide insights about its type, purpose, and key information.
            Please respond in JSON format:
            {{
                "document_type": "resume|job_description|cover_letter|other",
                "confidence": "high|medium|low",
                "purpose": "brief description of document purpose",
                "key_sections": ["list of main sections or topics"],
                "relevance_score": "1-10 rating for job search relevance",
                "recommendations": ["list of improvement suggestions if applicable"]
            }}
            
            Document text (first 3000 characters):
            {text[:3000]}
            """
            
            response = self.gemini_model.generate_content(prompt)
            
            try:
                response_text = response.text.strip()
                if response_text.startswith('```json'):
                    response_text = response_text[7:]
                if response_text.endswith('```'):
                    response_text = response_text[:-3]
                
                analysis_data = json.loads(response_text.strip())
                return analysis_data
                
            except json.JSONDecodeError:
                return {
                    "raw_response": response.text,
                    "error": "Failed to parse AI response as JSON"
                }
                
        except Exception as e:
            return {
                "error": f"Gemini API error: {str(e)}"
            }
    
    def extract_job_keywords(self, file_path: str) -> Dict[str, Any]:
        """
        Extract job-relevant keywords from a PDF using AI analysis.
        
        Args:
            file_path: Path to the PDF file
            
        Returns:
            Dictionary containing AI-extracted job-relevant information
        """
        if not PDF_LIBS_AVAILABLE:
            return {"error": "PDF libraries not installed"}
        
        if not self.gemini_model:
            return {"error": "Gemini AI not available. Check your API key in .env file"}
        
        try:
            # Extract text from PDF
            text = self.extract_text_only(file_path)
            
            if not text.strip():
                return {"error": "No text could be extracted from PDF"}
            
            # Get AI analysis
            keywords_data = self._extract_keywords_with_gemini(text)
            analysis_data = self._analyze_document_with_gemini(text)
            
            # Combine results
            result = {
                "file_info": {
                    "filename": Path(file_path).name,
                    "file_path": str(file_path),
                    "processed_at": datetime.now().isoformat()
                },
                "text_length": len(text),
                "ai_keywords": keywords_data,
                "ai_analysis": analysis_data
            }
            
            return result
            
        except Exception as e:
            return {"error": f"Failed to extract keywords: {str(e)}"}
    
    def _extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return list(set(re.findall(email_pattern, text)))
    
    def _extract_phone_numbers(self, text: str) -> List[str]:
        """Extract phone numbers from text."""
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # US format
            r'\b\(\d{3}\)\s*\d{3}[-.]?\d{4}\b',  # (xxx) xxx-xxxx
            r'\b\+\d{1,3}[-.\s]?\d{1,14}[-.\s]?\d{1,14}\b'  # International
        ]
        
        phones = []
        for pattern in phone_patterns:
            phones.extend(re.findall(pattern, text))
        
        return list(set(phones))
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text."""
        url_pattern = r'https?://[^\s<>"\']+|www\.[^\s<>"\']+'
        return list(set(re.findall(url_pattern, text)))
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract potential dates from text."""
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # MM/DD/YYYY
            r'\b\d{1,2}-\d{1,2}-\d{4}\b',  # MM-DD-YYYY
            r'\b\w+ \d{1,2}, \d{4}\b',     # Month DD, YYYY
            r'\b\d{4}-\d{2}-\d{2}\b'       # YYYY-MM-DD
        ]
        
        dates = []
        for pattern in date_patterns:
            dates.extend(re.findall(pattern, text))
        
        return list(set(dates))
    
    def _extract_potential_skills(self, text: str) -> List[str]:
        """Extract potential technical skills and keywords."""
        # Common technical skills and keywords
        skill_keywords = [
            'python', 'java', 'javascript', 'react', 'nodejs', 'sql', 'mysql', 'postgresql',
            'mongodb', 'redis', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git',
            'machine learning', 'deep learning', 'ai', 'data science', 'analytics',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib',
            'html', 'css', 'bootstrap', 'angular', 'vue', 'flask', 'django', 'fastapi',
            'restapi', 'graphql', 'microservices', 'devops', 'ci/cd', 'jenkins',
            'linux', 'bash', 'powershell', 'agile', 'scrum', 'project management'
        ]
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in skill_keywords:
            if skill in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_potential_companies(self, text: str) -> List[str]:
        """Extract potential company names."""
        # This is a simplified approach - in practice, you might use NER
        company_indicators = ['Inc.', 'LLC', 'Corp.', 'Corporation', 'Company', 'Ltd.']
        potential_companies = []
        
        for line in text.split('\n'):
            line = line.strip()
            for indicator in company_indicators:
                if indicator in line and len(line) < 100:  # Reasonable length
                    potential_companies.append(line)
                    break
        
        return list(set(potential_companies))
    
    def _detect_document_type(self, text: str) -> str:
        """Try to detect the type of document based on content."""
        text_lower = text.lower()
        
        resume_indicators = ['resume', 'cv', 'curriculum vitae', 'experience', 'education', 'skills', 'objective']
        job_desc_indicators = ['job description', 'responsibilities', 'requirements', 'qualifications', 'apply now']
        cover_letter_indicators = ['dear hiring manager', 'cover letter', 'sincerely', 'best regards']
        
        resume_score = sum(1 for indicator in resume_indicators if indicator in text_lower)
        job_desc_score = sum(1 for indicator in job_desc_indicators if indicator in text_lower)
        cover_letter_score = sum(1 for indicator in cover_letter_indicators if indicator in text_lower)
        
        if resume_score > job_desc_score and resume_score > cover_letter_score:
            return "resume"
        elif job_desc_score > cover_letter_score:
            return "job_description"
        elif cover_letter_score > 0:
            return "cover_letter"
        else:
            return "unknown"

    def save_parsed_data(self, parsed_data: Dict[str, Any], output_file: str = None) -> str:
        """Save parsed PDF data to JSON file."""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = parsed_data["file_info"]["filename"].replace('.pdf', '')
            output_file = f"parsed_{filename}_{timestamp}.json"
        
        # Create output directory
        output_dir = Path(__file__).parent / "parsed_pdfs"
        output_dir.mkdir(exist_ok=True)
        
        output_path = output_dir / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved parsed PDF data to: {output_path}")
        return str(output_path)

    def extract_text_only(self, file_path: str, method: str = "auto") -> str:
        """Extract only the text content from a PDF file."""
        parsed_data = self.parse_pdf(file_path, method)
        return parsed_data.get("content", {}).get("raw_text", "")

    def batch_parse_pdfs(self, directory: str, pattern: str = "*.pdf") -> List[Dict[str, Any]]:
        """Parse multiple PDF files in a directory."""
        directory_path = Path(directory)
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        pdf_files = list(directory_path.glob(pattern))
        results = []
        
        print(f"📄 Found {len(pdf_files)} PDF files to parse...")
        
        for pdf_file in pdf_files:
            print(f"Processing: {pdf_file.name}")
            try:
                parsed_data = self.parse_pdf(str(pdf_file))
                results.append(parsed_data)
            except Exception as e:
                print(f"❌ Failed to parse {pdf_file.name}: {e}")
                results.append({
                    "file_info": {"filename": pdf_file.name, "error": str(e)},
                    "error": str(e)
                })
        
        return results

def main():
    """Example usage of the PDF parser."""
    parser = PDFParser()
    
    # Example: Parse a single PDF
    # pdf_path = input("Enter path to PDF file: ")
    # if pdf_path and Path(pdf_path).exists():
    #     result = parser.parse_pdf(pdf_path)
    #     parser.save_parsed_data(result)
    #     print(f"Document type detected: {result['structured_data']['document_type']}")
    #     print(f"Word count: {result['structured_data']['statistics']['word_count']}")
    
    print("PDF Parser Tool initialized!")
    print("Usage examples:")
    print("  parser = PDFParser()")
    print("  result = parser.parse_pdf('resume.pdf')")
    print("  text = parser.extract_text_only('document.pdf')")
    print("  results = parser.batch_parse_pdfs('/path/to/pdfs/')")

if __name__ == "__main__":
    main()

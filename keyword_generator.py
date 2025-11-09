#!/usr/bin/env python3
"""
Keyword Generator Tool
Uses Gemini AI to extract and generate job-relevant keywords from various text sources.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    GEMINI_AVAILABLE = True
    load_dotenv()
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from pdf_parser import PDFParser
    PDF_PARSER_AVAILABLE = True
except ImportError:
    PDF_PARSER_AVAILABLE = False

class KeywordGenerator:
    """Generate job-relevant keywords from text, PDFs, or job descriptions using Gemini AI."""
    
    def __init__(self):
        self.gemini_model = None
        self.pdf_parser = None
        
        # Initialize Gemini AI
        if GEMINI_AVAILABLE:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key and api_key != 'your_gemini_api_key_here':
                try:
                    genai.configure(api_key=api_key)
                    self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    print("✅ Keyword Generator initialized with Gemini 2.0 Flash")
                except Exception as e:
                    print(f"⚠️  Failed to initialize Gemini AI: {e}")
        
        # Initialize PDF parser
        if PDF_PARSER_AVAILABLE:
            self.pdf_parser = PDFParser()
    
    def generate_keywords_from_text(self, text: str, context: str = "general") -> Dict[str, Any]:
        """
        Generate keywords from raw text using Gemini AI.
        
        Args:
            text: Input text to analyze
            context: Context type ('job_description', 'resume', 'cover_letter', 'general')
            
        Returns:
            Dictionary with extracted keywords and analysis
        """
        if not self.gemini_model:
            return {"error": "Gemini AI not available. Check your API key."}
        
        try:
            prompt = self._build_keyword_prompt(text, context)
            response = self.gemini_model.generate_content(prompt)
            
            return self._parse_gemini_response(response)
            
        except Exception as e:
            return {"error": f"Gemini AI error: {str(e)}"}
    
    def generate_keywords_from_pdf(self, file_path: str, context: str = "auto") -> Dict[str, Any]:
        """
        Generate keywords from a PDF file.
        
        Args:
            file_path: Path to PDF file
            context: Context type or 'auto' to detect automatically
            
        Returns:
            Dictionary with extracted keywords and analysis
        """
        if not self.pdf_parser:
            return {"error": "PDF parser not available"}
        
        try:
            # Extract text from PDF
            text = self.pdf_parser.extract_text_only(file_path)
            
            if not text.strip():
                return {"error": "No text could be extracted from PDF"}
            
            # Auto-detect context if needed
            if context == "auto":
                context = self._detect_document_context(text)
            
            # Generate keywords
            keywords_result = self.generate_keywords_from_text(text, context)
            
            # Add file information
            if "error" not in keywords_result:
                keywords_result["file_info"] = {
                    "filename": Path(file_path).name,
                    "file_path": str(file_path),
                    "text_length": len(text),
                    "processed_at": datetime.now().isoformat()
                }
            
            return keywords_result
            
        except Exception as e:
            return {"error": f"Failed to process PDF: {str(e)}"}
    
    def generate_job_match_keywords(self, job_description: str, resume_text: str) -> Dict[str, Any]:
        """
        Generate keywords for job matching by comparing job description with resume.
        
        Args:
            job_description: Text of job description
            resume_text: Text of resume/CV
            
        Returns:
            Dictionary with matching analysis and keyword recommendations
        """
        if not self.gemini_model:
            return {"error": "Gemini AI not available"}
        
        try:
            prompt = f"""
            Analyze the following job description and resume to identify keyword matches and gaps.
            Provide recommendations for improving keyword alignment.
            
            Return JSON format:
            {{
                "matching_keywords": ["keywords that match between job and resume"],
                "missing_keywords": ["important job keywords not found in resume"],
                "recommended_additions": ["specific keywords to add to resume"],
                "skill_gaps": ["technical skills mentioned in job but missing from resume"],
                "strength_areas": ["areas where resume exceeds job requirements"],
                "match_score": "percentage match score (0-100)",
                "improvement_suggestions": ["specific suggestions for better alignment"],
                "ats_keywords": ["keywords important for ATS (Applicant Tracking System)"],
                "industry_terms": ["industry-specific terms to include"],
                "action_verbs": ["strong action verbs relevant to this role"]
            }}
            
            JOB DESCRIPTION:
            {job_description[:3000]}
            
            RESUME:
            {resume_text[:3000]}
            """
            
            response = self.gemini_model.generate_content(prompt)
            return self._parse_gemini_response(response)
            
        except Exception as e:
            return {"error": f"Job matching analysis failed: {str(e)}"}
    
    def generate_industry_keywords(self, industry: str, role: str = "") -> Dict[str, Any]:
        """
        Generate industry-specific keywords and terms.
        
        Args:
            industry: Industry name (e.g., "technology", "healthcare", "finance")
            role: Optional specific role (e.g., "software engineer", "data scientist")
            
        Returns:
            Dictionary with industry-specific keywords
        """
        if not self.gemini_model:
            return {"error": "Gemini AI not available"}
        
        try:
            role_context = f" for {role} roles" if role else ""
            prompt = f"""
            Generate comprehensive keywords and terms for the {industry} industry{role_context}.
            
            Return JSON format:
            {{
                "industry_keywords": ["core industry terms and buzzwords"],
                "technical_skills": ["relevant technical skills and tools"],
                "soft_skills": ["important soft skills for this industry"],
                "certifications": ["valuable certifications in this field"],
                "job_titles": ["common job titles in this industry"],
                "company_types": ["types of companies in this industry"],
                "industry_trends": ["current trends and emerging technologies"],
                "required_experience": ["typical experience requirements"],
                "education_background": ["relevant educational backgrounds"],
                "regulatory_terms": ["industry-specific regulations or standards"],
                "tools_platforms": ["commonly used tools and platforms"],
                "methodologies": ["standard methodologies and frameworks"]
            }}
            
            Industry: {industry}
            {f'Specific Role: {role}' if role else ''}
            """
            
            response = self.gemini_model.generate_content(prompt)
            result = self._parse_gemini_response(response)
            
            if "error" not in result:
                result["industry"] = industry
                result["role"] = role
                result["generated_at"] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            return {"error": f"Industry keyword generation failed: {str(e)}"}
    
    def optimize_keywords_for_ats(self, text: str, target_job: str = "") -> Dict[str, Any]:
        """
        Optimize keywords specifically for ATS (Applicant Tracking Systems).
        
        Args:
            text: Text to optimize (resume, cover letter, etc.)
            target_job: Target job title or description
            
        Returns:
            Dictionary with ATS optimization recommendations
        """
        if not self.gemini_model:
            return {"error": "Gemini AI not available"}
        
        try:
            job_context = f" for {target_job}" if target_job else ""
            prompt = f"""
            Analyze the following text and provide ATS (Applicant Tracking System) optimization recommendations{job_context}.
            
            Return JSON format:
            {{
                "ats_score": "current ATS friendliness score (1-10)",
                "critical_keywords": ["must-have keywords for ATS scanning"],
                "keyword_density": "assessment of keyword density (low/optimal/high)",
                "missing_keywords": ["important keywords not found in text"],
                "formatting_issues": ["ATS formatting problems to fix"],
                "skill_variations": ["alternative ways to phrase skills"],
                "action_verbs": ["ATS-friendly action verbs to use"],
                "section_recommendations": ["recommended sections for better ATS parsing"],
                "keyword_placement": ["where to strategically place keywords"],
                "optimization_tips": ["specific tips for improving ATS compatibility"]
            }}
            
            {f'Target Job: {target_job}' if target_job else ''}
            
            Text to analyze:
            {text[:4000]}
            """
            
            response = self.gemini_model.generate_content(prompt)
            return self._parse_gemini_response(response)
            
        except Exception as e:
            return {"error": f"ATS optimization failed: {str(e)}"}
    
    def _build_keyword_prompt(self, text: str, context: str) -> str:
        """Build appropriate prompt based on context."""
        context_prompts = {
            "job_description": "Analyze this job description and extract key requirements, skills, and qualifications.",
            "resume": "Analyze this resume and extract skills, experience, and qualifications.",
            "cover_letter": "Analyze this cover letter and extract key themes and skills highlighted.",
            "general": "Analyze this text and extract relevant keywords and themes."
        }
        
        context_instruction = context_prompts.get(context, context_prompts["general"])
        
        return f"""
        {context_instruction}
        
        Return response in JSON format:
        {{
            "technical_skills": ["list of technical skills found"],
            "soft_skills": ["list of soft skills and competencies"],
            "job_titles": ["job titles or positions mentioned"],
            "companies": ["companies or organizations mentioned"],
            "education": ["educational qualifications or institutions"],
            "certifications": ["certifications or credentials"],
            "programming_languages": ["programming languages"],
            "tools_technologies": ["tools, platforms, and technologies"],
            "industries": ["industries or business domains"],
            "experience_keywords": ["experience-related terms"],
            "achievement_keywords": ["achievement and accomplishment terms"],
            "action_verbs": ["strong action verbs used"],
            "keywords": ["other relevant keywords"],
            "key_phrases": ["important phrases and expressions"],
            "document_summary": "brief summary of the content",
            "keyword_density": "assessment of keyword usage",
            "context_type": "detected document type"
        }}
        
        Text to analyze:
        {text[:4000]}
        """
    
    def _detect_document_context(self, text: str) -> str:
        """Auto-detect document context from text."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['resume', 'cv', 'curriculum vitae', 'experience', 'education']):
            return "resume"
        elif any(word in text_lower for word in ['job description', 'responsibilities', 'requirements', 'we are looking']):
            return "job_description"
        elif any(word in text_lower for word in ['dear hiring', 'cover letter', 'i am writing', 'position']):
            return "cover_letter"
        else:
            return "general"
    
    def _parse_gemini_response(self, response) -> Dict[str, Any]:
        """Parse and clean Gemini AI response."""
        try:
            response_text = response.text.strip()
            
            # Clean common formatting issues
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            # Parse JSON
            result = json.loads(response_text.strip())
            result["generated_at"] = datetime.now().isoformat()
            return result
            
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse AI response as JSON",
                "raw_response": response.text
            }
    
    def save_keywords(self, keywords_data: Dict[str, Any], filename: str = None) -> str:
        """Save keywords data to JSON file."""
        if "error" in keywords_data:
            return "Cannot save data with errors"
        
        # Create output directory
        output_dir = Path(__file__).parent / "keyword_results"
        output_dir.mkdir(exist_ok=True)
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            context = keywords_data.get("context_type", "keywords")
            filename = f"{context}_{timestamp}.json"
        
        # Ensure .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        # Save to file
        file_path = output_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(keywords_data, f, indent=2, ensure_ascii=False)
        
        return str(file_path)

# Quick test function
def test_keyword_generator():
    """Test the keyword generator with sample text."""
    generator = KeywordGenerator()
    
    if not generator.gemini_model:
        print("❌ Gemini AI not available. Check your API key.")
        return
    
    sample_text = """
    Senior Software Engineer position at Google
    Requirements: 5+ years Python, React, AWS experience
    Skills: Machine Learning, Docker, Kubernetes, PostgreSQL
    Nice to have: TensorFlow, Jenkins, Agile methodology
    """
    
    print("🧪 Testing Keyword Generator...")
    result = generator.generate_keywords_from_text(sample_text, "job_description")
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print("✅ Keywords extracted successfully!")
        for key, value in result.items():
            if isinstance(value, list) and value:
                print(f"  {key}: {', '.join(value[:3])}")

if __name__ == "__main__":
    test_keyword_generator()

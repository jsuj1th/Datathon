#!/usr/bin/env python3
"""
Gemini AI + PDF Parser Demo
Demonstrates how to extract keywords from PDFs using Gemini AI.
"""

import os
import json
from pathlib import Path
from pdf_parser import PDFParser

def demo_gemini_pdf_analysis():
    """Demonstrate Gemini AI integration with PDF parser."""
    print("🤖 Gemini AI + PDF Parser Demo")
    print("=" * 60)
    
    # Check if Gemini API key is configured
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("⚠️  GEMINI_API_KEY not found in .env file")
        print("📝 To set up Gemini AI:")
        print("   1. Get your API key from: https://makersuite.google.com/app/apikey")
        print("   2. Add it to your .env file: GEMINI_API_KEY=your_actual_key_here")
        print("   3. Run this demo again")
        return
    
    # Initialize parser
    parser = PDFParser()
    
    # Check if demo PDFs directory exists
    demo_dir = Path(__file__).parent / "demo_pdfs"
    demo_dir.mkdir(exist_ok=True)
    
    pdf_files = list(demo_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("📂 No PDF files found in demo_pdfs directory")
        print("📝 To test Gemini AI analysis:")
        print("   1. Add some PDF files (resumes, job descriptions) to the 'demo_pdfs' folder")
        print("   2. Run this script again")
        
        # Create a sample text file for testing
        sample_text_file = demo_dir / "sample_resume.txt"
        sample_content = """
        John Smith
        Senior Software Engineer
        Email: john.smith@email.com
        Phone: (555) 123-4567
        
        TECHNICAL SKILLS
        • Programming: Python, JavaScript, Java, TypeScript
        • Web Technologies: React, Node.js, Express, HTML5, CSS3
        • Databases: PostgreSQL, MongoDB, Redis
        • Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
        • Tools: Git, Jenkins, Jira, VS Code
        
        EXPERIENCE
        Senior Software Engineer | Google Inc. | 2020 - Present
        • Led development of microservices architecture serving 10M+ users
        • Implemented CI/CD pipelines reducing deployment time by 60%
        • Mentored team of 5 junior developers
        
        Software Engineer | Microsoft Corp. | 2018 - 2020
        • Developed scalable web applications using React and Node.js
        • Optimized database queries improving performance by 40%
        
        EDUCATION
        Bachelor of Science in Computer Science
        Stanford University | 2018
        
        CERTIFICATIONS
        • AWS Certified Solutions Architect
        • Google Cloud Professional Developer
        """
        
        with open(sample_text_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        print(f"📄 Created sample text file: {sample_text_file}")
        print("   (Note: This is a .txt file, not PDF. Add real PDFs to test PDF parsing)")
        
        # Demo the AI analysis on sample text
        print("\n🧠 Testing Gemini AI analysis on sample text...")
        if parser.gemini_model:
            keywords = parser._extract_keywords_with_gemini(sample_content)
            analysis = parser._analyze_document_with_gemini(sample_content)
            
            print("\n🔍 AI Keywords Extraction:")
            if "error" not in keywords:
                for key, value in keywords.items():
                    if isinstance(value, list) and value:
                        print(f"   {key}: {', '.join(value[:5])}{'...' if len(value) > 5 else ''}")
                    elif value and key != "document_summary":
                        print(f"   {key}: {value}")
                
                if "document_summary" in keywords:
                    print(f"\n📄 Summary: {keywords['document_summary']}")
            else:
                print(f"   Error: {keywords['error']}")
            
            print("\n📊 Document Analysis:")
            if "error" not in analysis:
                for key, value in analysis.items():
                    print(f"   {key}: {value}")
            else:
                print(f"   Error: {analysis['error']}")
        
        return
    
    # Process found PDF files
    print(f"📄 Found {len(pdf_files)} PDF files:")
    for pdf_file in pdf_files:
        print(f"   - {pdf_file.name}")
    
    # Analyze the first PDF file
    first_pdf = pdf_files[0]
    print(f"\n🔍 Analyzing: {first_pdf.name}")
    print("-" * 40)
    
    try:
        # Extract keywords using AI
        result = parser.extract_job_keywords(str(first_pdf))
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return
        
        print("✅ Analysis complete!")
        print(f"📊 File: {result['file_info']['filename']}")
        print(f"📏 Text length: {result['text_length']} characters")
        
        # Display AI keywords
        ai_keywords = result.get('ai_keywords', {})
        if "error" not in ai_keywords:
            print("\n🔍 AI-Extracted Keywords:")
            for category, items in ai_keywords.items():
                if isinstance(items, list) and items and category != "document_summary":
                    print(f"   📌 {category.title()}: {', '.join(items[:3])}{'...' if len(items) > 3 else ''}")
            
            if "document_summary" in ai_keywords:
                print(f"\n📄 AI Summary:")
                print(f"   {ai_keywords['document_summary']}")
        
        # Display AI analysis
        ai_analysis = result.get('ai_analysis', {})
        if "error" not in ai_analysis:
            print(f"\n📊 Document Analysis:")
            print(f"   📁 Type: {ai_analysis.get('document_type', 'unknown')}")
            print(f"   🎯 Confidence: {ai_analysis.get('confidence', 'unknown')}")
            print(f"   📈 Relevance Score: {ai_analysis.get('relevance_score', 'unknown')}/10")
            print(f"   🎯 Purpose: {ai_analysis.get('purpose', 'unknown')}")
        
        # Save detailed results
        output_dir = Path(__file__).parent / "ai_analysis_results"
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / f"ai_analysis_{first_pdf.stem}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")

def show_api_setup_instructions():
    """Show instructions for setting up Gemini API."""
    print("\n🚀 Setting up Gemini AI API:")
    print("=" * 40)
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Create a new API key")
    print("4. Copy the API key")
    print("5. Add it to your .env file:")
    print("   GEMINI_API_KEY=your_actual_api_key_here")
    print("\n⚠️  Keep your API key secure and never share it publicly!")

if __name__ == "__main__":
    demo_gemini_pdf_analysis()
    show_api_setup_instructions()

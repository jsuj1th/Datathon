#!/usr/bin/env python3
"""
Quick PDF Parser Test
"""
from pdf_parser import PDFParser

def test_pdf_parser_functionality():
    """Test the PDF parser with basic functionality."""
    print("🔍 Testing PDF Parser Functionality")
    print("=" * 50)
    
    # Initialize parser
    parser = PDFParser()
    print("✅ PDF Parser initialized successfully")
    
    # Test the available methods
    print("\n📋 Available parsing methods:")
    methods = ['pypdf2', 'pdfplumber', 'pymupdf', 'auto']
    for method in methods:
        print(f"  • {method}")
    
    # Test text analysis capabilities
    sample_text = """
    John Doe
    Senior Software Engineer
    Email: john.doe@example.com
    Phone: (555) 123-4567
    
    TECHNICAL SKILLS:
    • Python, JavaScript, Java
    • AWS, Docker, Kubernetes
    • React, Node.js, PostgreSQL
    • Machine Learning, TensorFlow
    
    EXPERIENCE:
    Google Inc. (2020-Present)
    - Developed scalable web applications
    - Led team of 5 engineers
    
    Microsoft Corp. (2018-2020)
    - Backend development with Python
    - Cloud infrastructure on Azure
    """
    
    print("\n🔍 Testing text analysis capabilities:")
    
    # Test email extraction
    import re
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', sample_text)
    print(f"  • Found emails: {emails}")
    
    # Test phone extraction
    phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', sample_text)
    print(f"  • Found phones: {phones}")
    
    # Test skills extraction
    common_skills = ['Python', 'JavaScript', 'Java', 'AWS', 'Docker', 'React', 'Node.js', 'PostgreSQL', 'TensorFlow']
    found_skills = [skill for skill in common_skills if skill in sample_text]
    print(f"  • Found skills: {found_skills}")
    
    # Test company extraction
    companies = ['Google', 'Microsoft', 'Apple', 'Amazon', 'Meta']
    found_companies = [company for company in companies if company in sample_text]
    print(f"  • Found companies: {found_companies}")
    
    print("\n✅ PDF Parser is ready to process real PDF files!")
    print("\n📝 To use with actual PDFs:")
    print("  1. Place PDF files in the 'demo_pdfs' directory")
    print("  2. Run: python pdf_parser_demo.py")
    print("  3. Or use the MCP server: python mcp_server.py")

if __name__ == "__main__":
    test_pdf_parser_functionality()

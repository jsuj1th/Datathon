#!/usr/bin/env python3
"""
PDF Parser Demo
Demonstrates how to use the PDF parser tool for job-related documents.
"""

import os
from pathlib import Path
from pdf_parser import PDFParser

def demo_pdf_parser():
    """Demonstrate PDF parser functionality."""
    print("🔍 PDF Parser Tool Demo")
    print("=" * 50)
    
    parser = PDFParser()
    
    # Create a demo directory for PDF files
    demo_dir = Path(__file__).parent / "demo_pdfs"
    demo_dir.mkdir(exist_ok=True)
    
    print(f"📁 Demo directory created: {demo_dir}")
    print("\nTo test the PDF parser:")
    print("1. Place PDF files (resumes, job descriptions, etc.) in the 'demo_pdfs' directory")
    print("2. Run the examples below")
    
    # Check if there are any PDF files to process
    pdf_files = list(demo_dir.glob("*.pdf"))
    
    if pdf_files:
        print(f"\n📄 Found {len(pdf_files)} PDF files:")
        for pdf_file in pdf_files:
            print(f"  - {pdf_file.name}")
        
        # Parse the first PDF as an example
        first_pdf = pdf_files[0]
        print(f"\n🔍 Parsing: {first_pdf.name}")
        
        try:
            result = parser.parse_pdf(str(first_pdf))
            
            # Display summary
            print("\n📊 Parsing Results:")
            print(f"  • File: {result['file_info']['filename']}")
            print(f"  • Size: {result['file_info']['file_size']:,} bytes")
            print(f"  • Pages: {result['content']['page_count']}")
            print(f"  • Method: {result.get('parsing_method', 'auto')}")
            print(f"  • Document Type: {result['structured_data']['document_type']}")
            
            # Statistics
            stats = result['structured_data']['statistics']
            print(f"  • Word Count: {stats['word_count']:,}")
            print(f"  • Character Count: {stats['character_count']:,}")
            
            # Extracted data
            structured = result['structured_data']
            if structured['emails']:
                print(f"  • Emails found: {len(structured['emails'])}")
                for email in structured['emails'][:3]:  # Show first 3
                    print(f"    - {email}")
            
            if structured['phone_numbers']:
                print(f"  • Phone numbers found: {len(structured['phone_numbers'])}")
                for phone in structured['phone_numbers'][:3]:  # Show first 3
                    print(f"    - {phone}")
            
            if structured['skills']:
                print(f"  • Technical skills found: {len(structured['skills'])}")
                skills_str = ", ".join(structured['skills'][:10])  # Show first 10
                print(f"    - {skills_str}")
            
            # Save the result
            output_file = parser.save_parsed_data(result)
            print(f"\n✅ Detailed results saved to: {Path(output_file).name}")
            
        except Exception as e:
            print(f"❌ Error parsing {first_pdf.name}: {e}")
    
    else:
        print("\n📝 No PDF files found in demo_pdfs directory.")
        print("Add some PDF files to test the parser!")
    
    print("\n" + "=" * 50)
    print("🔧 Usage Examples:")
    
    # Show usage examples
    examples = [
        ("Parse a single PDF:", "result = parser.parse_pdf('resume.pdf')"),
        ("Extract text only:", "text = parser.extract_text_only('document.pdf')"),
        ("Batch parse PDFs:", "results = parser.batch_parse_pdfs('pdf_folder/')"),
        ("Use specific method:", "result = parser.parse_pdf('file.pdf', method='pdfplumber')"),
    ]
    
    for description, code in examples:
        print(f"\n{description}")
        print(f"  {code}")
    
    print("\n🎯 Perfect for:")
    use_cases = [
        "Parsing job descriptions from PDFs",
        "Extracting resume information",
        "Analyzing cover letters", 
        "Processing application documents",
        "Extracting structured data from forms",
        "Batch processing multiple documents"
    ]
    
    for use_case in use_cases:
        print(f"  • {use_case}")

def create_sample_pdf_info():
    """Create a sample info file about PDF parsing."""
    info_file = Path(__file__).parent / "pdf_parser_info.md"
    
    content = """# PDF Parser Tool

## Overview
The PDF Parser Tool is a comprehensive utility for extracting and analyzing content from PDF files. It's particularly useful for job search applications, resume parsing, and document analysis.

## Features

### Multiple Parsing Methods
- **PyPDF2**: Basic text extraction, good for simple documents
- **pdfplumber**: Excellent for tables and structured content
- **PyMuPDF**: Best for complex layouts and detailed formatting
- **Auto**: Automatically chooses the best method

### Extracted Information
- **Basic Content**: Raw text, page count, metadata
- **Structured Data**: Emails, phone numbers, URLs, dates
- **Document Analysis**: Word count, character count, document type detection
- **Technical Skills**: Automatic detection of programming languages and technologies
- **Company Names**: Extraction of potential company mentions

### Document Type Detection
- Resume/CV detection
- Job description identification
- Cover letter recognition
- General document classification

## Use Cases

### Job Search Applications
- Parse job descriptions from PDF postings
- Extract requirements and skills from job ads
- Analyze company information from documents
- Process application materials

### Resume Analysis
- Extract contact information
- Identify technical skills and experience
- Parse education and work history
- Detect formatting and structure

### Batch Processing
- Process multiple resumes at once
- Analyze job posting collections
- Compare document content
- Generate summary reports

## Installation
```bash
pip install PyPDF2 pdfplumber PyMuPDF
```

## Quick Start
```python
from pdf_parser import PDFParser

# Initialize parser
parser = PDFParser()

# Parse a PDF file
result = parser.parse_pdf('resume.pdf')

# Extract just text
text = parser.extract_text_only('document.pdf')

# Batch process
results = parser.batch_parse_pdfs('pdf_directory/')
```

## Integration with Job Search
The PDF parser integrates seamlessly with the existing job search tools:
- Parse job descriptions saved as PDFs
- Extract requirements for skills matching
- Process resume collections for analysis
- Analyze application documents
"""
    
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"📝 Created PDF parser documentation: {info_file}")

if __name__ == "__main__":
    demo_pdf_parser()
    create_sample_pdf_info()

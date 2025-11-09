#!/usr/bin/env python3
"""
Keyword Generation Demo
Demonstrates the AI-powered keyword generation tools.
"""

import json
from keyword_generator import KeywordGenerator

def demo_keyword_tools():
    """Demonstrate all keyword generation tools."""
    print("🔑 AI-Powered Keyword Generation Demo")
    print("=" * 60)
    
    generator = KeywordGenerator()
    
    if not generator.gemini_model:
        print("❌ Gemini AI not available. Check your API key in .env file.")
        return
    
    print("✅ Keyword Generator initialized with Gemini 2.0 Flash")
    print("\n" + "=" * 60)
    
    # Demo 1: Extract keywords from job description
    print("📋 Demo 1: Job Description Analysis")
    print("-" * 40)
    
    job_description = """
    Senior Data Scientist - Tech Company
    
    We are seeking an experienced Senior Data Scientist to join our AI/ML team.
    
    Requirements:
    • Master's degree in Data Science, Statistics, or related field
    • 5+ years of experience in data science and machine learning
    • Proficiency in Python, R, SQL, and big data technologies
    • Experience with TensorFlow, PyTorch, and scikit-learn
    • Strong knowledge of statistics, A/B testing, and experimental design
    • Experience with cloud platforms (AWS, GCP, Azure)
    • Excellent communication and collaboration skills
    
    Responsibilities:
    • Build and deploy machine learning models at scale
    • Collaborate with engineering teams on model integration
    • Conduct statistical analysis and A/B tests
    • Present findings to stakeholders and leadership
    """
    
    result1 = generator.generate_keywords_from_text(job_description, "job_description")
    display_keywords_result("Job Description Keywords", result1)
    
    print("\n" + "=" * 60)
    
    # Demo 2: Industry-specific keywords
    print("🏭 Demo 2: Industry Keywords Generation")
    print("-" * 40)
    
    result2 = generator.generate_industry_keywords("technology", "data scientist")
    display_keywords_result("Technology Industry Keywords", result2)
    
    print("\n" + "=" * 60)
    
    # Demo 3: Resume analysis
    print("📄 Demo 3: Resume Analysis")
    print("-" * 40)
    
    resume_text = """
    John Smith
    Data Scientist
    
    EXPERIENCE:
    Data Scientist | ABC Corp | 2020-2024
    • Developed machine learning models using Python and TensorFlow
    • Improved prediction accuracy by 25% through feature engineering
    • Led A/B testing initiatives resulting in 15% increase in user engagement
    
    Junior Data Analyst | XYZ Inc | 2018-2020
    • Performed statistical analysis using R and SQL
    • Created dashboards and visualizations with Tableau
    
    EDUCATION:
    M.S. in Statistics | Stanford University | 2018
    
    SKILLS:
    Python, R, SQL, TensorFlow, PyTorch, scikit-learn, Pandas, NumPy,
    Tableau, Power BI, AWS, Git, Jupyter, Statistical Analysis, A/B Testing
    """
    
    result3 = generator.generate_keywords_from_text(resume_text, "resume")
    display_keywords_result("Resume Keywords", result3)
    
    print("\n" + "=" * 60)
    
    # Demo 4: Job matching analysis
    print("🎯 Demo 4: Job Matching Analysis")
    print("-" * 40)
    
    result4 = generator.generate_job_match_keywords(job_description, resume_text)
    display_matching_result(result4)
    
    print("\n" + "=" * 60)
    
    # Demo 5: ATS optimization
    print("🤖 Demo 5: ATS Optimization")
    print("-" * 40)
    
    result5 = generator.optimize_keywords_for_ats(resume_text, "Senior Data Scientist")
    display_ats_result(result5)
    
    print("\n" + "=" * 60)
    print("✅ Keyword Generation Demo Complete!")
    print("\n📝 Usage Tips:")
    print("• Use these tools to optimize your resume for specific jobs")
    print("• Generate industry-specific keywords for your field")
    print("• Analyze job descriptions to understand requirements")
    print("• Optimize your content for ATS systems")
    print("• Compare your resume against job postings")

def display_keywords_result(title: str, result: dict):
    """Display keyword extraction results in a formatted way."""
    print(f"🔍 {title}:")
    
    if "error" in result:
        print(f"   ❌ Error: {result['error']}")
        return
    
    # Show key categories
    key_categories = [
        "technical_skills", "soft_skills", "programming_languages", 
        "tools_technologies", "certifications", "job_titles"
    ]
    
    for category in key_categories:
        if category in result and result[category]:
            items = result[category][:5]  # Show first 5 items
            print(f"   📌 {category.replace('_', ' ').title()}: {', '.join(items)}")
    
    if "document_summary" in result:
        print(f"   📄 Summary: {result['document_summary']}")

def display_matching_result(result: dict):
    """Display job matching analysis results."""
    print("🎯 Job Matching Analysis:")
    
    if "error" in result:
        print(f"   ❌ Error: {result['error']}")
        return
    
    # Key matching metrics
    metrics = [
        ("match_score", "Match Score"),
        ("matching_keywords", "Matching Keywords"),
        ("missing_keywords", "Missing Keywords"),
        ("recommended_additions", "Recommended Additions"),
        ("skill_gaps", "Skill Gaps")
    ]
    
    for key, label in metrics:
        if key in result and result[key]:
            value = result[key]
            if isinstance(value, list):
                if len(value) > 0:
                    print(f"   📊 {label}: {', '.join(value[:5])}")
            else:
                print(f"   📊 {label}: {value}")

def display_ats_result(result: dict):
    """Display ATS optimization results."""
    print("🤖 ATS Optimization Analysis:")
    
    if "error" in result:
        print(f"   ❌ Error: {result['error']}")
        return
    
    # ATS metrics
    ats_metrics = [
        ("ats_score", "ATS Score"),
        ("keyword_density", "Keyword Density"),
        ("critical_keywords", "Critical Keywords"),
        ("missing_keywords", "Missing Keywords"),
        ("optimization_tips", "Optimization Tips")
    ]
    
    for key, label in ats_metrics:
        if key in result and result[key]:
            value = result[key]
            if isinstance(value, list):
                if len(value) > 0:
                    print(f"   🎯 {label}: {', '.join(value[:3])}")
            else:
                print(f"   🎯 {label}: {value}")

if __name__ == "__main__":
    demo_keyword_tools()

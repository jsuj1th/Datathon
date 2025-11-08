"""
Test Mixed Content Classification
Demonstrates how the system handles documents with multiple classification levels
"""

from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from config import Config

def test_mixed_content(filepath, description):
    """Test a document and show mixed content breakdown"""
    print("="*80)
    print(f"Testing: {description}")
    print(f"File: {filepath}")
    print("="*80)
    
    preprocessor = DocumentPreprocessor()
    classifier = DocumentClassifier()
    
    # Pre-process
    preprocess_result = preprocessor.check_file_validity(filepath)
    if not preprocess_result['valid']:
        print(f"❌ Pre-processing failed")
        return
    
    metadata = preprocess_result['metadata']
    print(f"\n📄 Pages: {metadata['page_count']}")
    print(f"🖼️  Images: {metadata['image_count']}")
    
    # Extract and classify
    content = preprocessor.extract_content_for_analysis(filepath, metadata)
    classification = classifier.classify_document(content, metadata)
    
    # Display results
    print(f"\n📋 PRIMARY CATEGORY: {classification.get('category', 'unknown').upper()}")
    print(f"📊 Confidence: {classification.get('confidence', 0):.1%}")
    print(f"🔀 Mixed Content: {'YES' if classification.get('is_mixed_content', False) else 'NO'}")
    
    # Show breakdown if mixed
    if classification.get('is_mixed_content', False):
        print(f"\n{'='*80}")
        print("CONTENT BREAKDOWN BY CATEGORY")
        print('='*80)
        
        breakdown = classification.get('category_breakdown', {})
        for cat_name, cat_data in breakdown.items():
            percentage = cat_data.get('percentage', 0)
            if percentage > 0:
                print(f"\n{cat_name.upper()}:")
                print(f"  Percentage: {percentage}%")
                print(f"  Pages: {cat_data.get('page_count', 0)}")
                print(f"  Reason: {cat_data.get('reason', 'N/A')}")
    
    # Show evidence by category
    print(f"\n{'='*80}")
    print("EVIDENCE BY CATEGORY")
    print('='*80)
    
    evidence_by_cat = {}
    for evidence in classification.get('evidence', []):
        if isinstance(evidence, dict):
            cat = evidence.get('category', 'unknown')
            if cat not in evidence_by_cat:
                evidence_by_cat[cat] = []
            evidence_by_cat[cat].append(evidence)
    
    for cat, evidences in evidence_by_cat.items():
        print(f"\n{cat.upper()} Evidence:")
        for idx, ev in enumerate(evidences, 1):
            print(f"  {idx}. {ev.get('finding', '')[:100]}...")
            if ev.get('locations'):
                print(f"     Location: {', '.join(str(loc) for loc in ev['locations'][:3])}")
    
    print(f"\n{'='*80}")
    print(f"RESULT: Primary category is {classification.get('category', 'unknown').upper()}")
    print(f"        (Most restrictive category for mixed content)")
    print('='*80)

def main():
    if not Config.OPENROUTER_API_KEY:
        print("❌ OpenRouter API key not configured!")
        return
    
    print("\n" + "╔" + "═"*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  MIXED CONTENT CLASSIFICATION TEST".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "═"*78 + "╝")
    
    # Test all documents to see which have mixed content
    test_cases = [
        ("test_documents/TC1_Sample_Public_Marketing_Document.pdf", "TC1: Public Marketing"),
        ("test_documents/TC2_Filled_In_Employement_Application.pdf", "TC2: Employment App with PII"),
        ("test_documents/TC3_Sample_Internal_Memo.pdf", "TC3: Internal Research Memo"),
    ]
    
    for filepath, description in test_cases:
        try:
            test_mixed_content(filepath, description)
            print("\n\n")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()

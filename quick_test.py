"""
Quick test to verify core system functionality
"""

import os
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from config import Config

def test_system():
    print("="*70)
    print("QUICK SYSTEM TEST")
    print("="*70)
    print()
    
    # Check API key
    print("1. Checking configuration...")
    if not Config.OPENROUTER_API_KEY or Config.OPENROUTER_API_KEY == 'your_openrouter_api_key_here':
        print("   ❌ API key not configured!")
        print("   Please set OPENROUTER_API_KEY in .env file")
        return False
    print("   ✓ API key configured")
    print()
    
    # Check test file exists
    print("2. Checking test document...")
    test_file = "test_documents/TC1_Sample_Public_Marketing_Document.pdf"
    if not os.path.exists(test_file):
        print(f"   ❌ Test file not found: {test_file}")
        return False
    print(f"   ✓ Test file found: {test_file}")
    print()
    
    # Initialize components
    print("3. Initializing components...")
    try:
        preprocessor = DocumentPreprocessor()
        classifier = DocumentClassifier()
        print("   ✓ Components initialized")
    except Exception as e:
        print(f"   ❌ Initialization failed: {e}")
        return False
    print()
    
    # Test preprocessing
    print("4. Testing preprocessing...")
    try:
        preprocess_result = preprocessor.check_file_validity(test_file)
        if not preprocess_result['valid']:
            print(f"   ❌ Preprocessing failed: {preprocess_result['errors']}")
            return False
        metadata = preprocess_result['metadata']
        print(f"   ✓ Document validated")
        print(f"     - Pages: {metadata.get('page_count', 0)}")
        print(f"     - Images: {metadata.get('image_count', 0)}")
    except Exception as e:
        print(f"   ❌ Preprocessing error: {e}")
        return False
    print()
    
    # Test content extraction
    print("5. Testing content extraction...")
    try:
        content = preprocessor.extract_content_for_analysis(test_file, metadata)
        print(f"   ✓ Content extracted")
        print(f"     - Text: {len(content.get('text', ''))} chars")
        print(f"     - Images: {len(content.get('images', []))} images")
    except Exception as e:
        print(f"   ❌ Content extraction error: {e}")
        return False
    print()
    
    # Test classification
    print("6. Testing classification...")
    try:
        classification = classifier.classify_document(content, metadata)
        print(f"   ✓ Classification complete")
        print(f"     - Category: {classification.get('category', 'unknown').upper()}")
        print(f"     - Confidence: {classification.get('confidence', 0):.0%}")
        print(f"     - Evidence items: {len(classification.get('evidence', []))}")
        print(f"     - Safety check: {'✓ Safe' if classification.get('safety_check', True) else '⚠️ Unsafe'}")
    except Exception as e:
        print(f"   ❌ Classification error: {e}")
        import traceback
        traceback.print_exc()
        return False
    print()
    
    # Test category breakdown
    print("7. Testing category breakdown...")
    breakdown = classification.get('category_breakdown', {})
    if breakdown:
        print("   ✓ Category breakdown available:")
        for cat, data in breakdown.items():
            if data.get('percentage', 0) > 0:
                print(f"     - {cat.replace('_', ' ').title()}: {data['percentage']}%")
    else:
        print("   ⚠️ No category breakdown (might be old format)")
    print()
    
    print("="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70)
    print()
    print("System is ready to use!")
    print()
    print("To start the UI:")
    print("  streamlit run demo_ui.py")
    print()
    return True

if __name__ == '__main__':
    success = test_system()
    exit(0 if success else 1)

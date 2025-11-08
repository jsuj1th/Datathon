"""
Test script for the AI Document Classification System
Run this to verify the system is working correctly
"""

import os
import sys
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from hitl_manager import HITLManager

def test_preprocessor():
    """Test document preprocessing"""
    print("\n=== Testing Preprocessor ===")
    
    preprocessor = DocumentPreprocessor()
    
    # Test with a sample file (you'll need to provide actual test files)
    test_file = "test_documents/sample.pdf"
    
    if not os.path.exists(test_file):
        print(f"⚠️  Test file not found: {test_file}")
        print("   Please add test documents to the test_documents folder")
        return False
    
    result = preprocessor.check_file_validity(test_file)
    
    print(f"✓ File validity check: {'PASS' if result['valid'] else 'FAIL'}")
    print(f"  - Page count: {result['metadata'].get('page_count', 0)}")
    print(f"  - Image count: {result['metadata'].get('image_count', 0)}")
    print(f"  - Has text: {result['metadata'].get('has_text', False)}")
    print(f"  - Is legible: {result['metadata'].get('is_legible', False)}")
    
    return result['valid']

def test_classifier():
    """Test document classification"""
    print("\n=== Testing Classifier ===")
    
    from config import Config
    
    if not Config.OPENAI_API_KEY:
        print("⚠️  OpenAI API key not configured")
        print("   Please set OPENAI_API_KEY in .env file")
        return False
    
    print("✓ OpenAI API key configured")
    
    classifier = DocumentClassifier()
    
    # Test with mock content
    mock_content = {
        'text': 'This is a public marketing brochure for our new product.',
        'images': [],
        'metadata': {
            'page_count': 1,
            'image_count': 0,
            'has_text': True
        }
    }
    
    mock_metadata = {
        'page_count': 1,
        'image_count': 0,
        'has_text': True,
        'type': 'pdf'
    }
    
    try:
        result = classifier.classify_document(mock_content, mock_metadata)
        print(f"✓ Classification successful")
        print(f"  - Category: {result.get('category', 'unknown')}")
        print(f"  - Confidence: {result.get('confidence', 0):.2f}")
        return True
    except Exception as e:
        print(f"✗ Classification failed: {str(e)}")
        return False

def test_hitl_manager():
    """Test HITL feedback system"""
    print("\n=== Testing HITL Manager ===")
    
    hitl = HITLManager()
    
    # Submit test feedback
    test_classification = {
        'category': 'public',
        'confidence': 0.85
    }
    
    test_feedback = {
        'corrected_category': 'confidential',
        'notes': 'This is actually internal documentation'
    }
    
    try:
        feedback_entry = hitl.submit_feedback(
            'test_doc_001',
            test_classification,
            test_feedback
        )
        
        print("✓ Feedback submission successful")
        print(f"  - Agreement: {feedback_entry.get('agreement', False)}")
        
        stats = hitl.get_statistics()
        print(f"✓ Statistics retrieved")
        print(f"  - Total feedback: {stats.get('total_feedback', 0)}")
        
        return True
    except Exception as e:
        print(f"✗ HITL test failed: {str(e)}")
        return False

def test_api_keys():
    """Test API key configuration"""
    print("\n=== Testing API Configuration ===")
    
    from config import Config
    
    openai_configured = bool(Config.OPENAI_API_KEY)
    anthropic_configured = bool(Config.ANTHROPIC_API_KEY)
    
    print(f"{'✓' if openai_configured else '✗'} OpenAI API Key: {'Configured' if openai_configured else 'Not configured'}")
    print(f"{'✓' if anthropic_configured else '⚠️ '} Anthropic API Key: {'Configured' if anthropic_configured else 'Not configured (optional)'}")
    
    if not openai_configured:
        print("\n⚠️  WARNING: OpenAI API key is required for classification")
        print("   Please create a .env file with your API key:")
        print("   OPENAI_API_KEY=your_key_here")
        return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("AI Document Classification System - Test Suite")
    print("=" * 60)
    
    results = {
        'API Configuration': test_api_keys(),
        'HITL Manager': test_hitl_manager(),
        'Classifier': test_classifier(),
        'Preprocessor': test_preprocessor()
    }
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✓ All tests passed! System is ready to use.")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

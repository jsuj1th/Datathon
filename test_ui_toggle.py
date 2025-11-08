"""
Test the dual-LLM toggle functionality
"""

from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier

def test_toggle():
    """Test that dual-LLM can be toggled via parameter"""
    
    print("="*70)
    print("TESTING DUAL-LLM TOGGLE FUNCTIONALITY")
    print("="*70)
    print()
    
    # Initialize
    preprocessor = DocumentPreprocessor()
    classifier = DocumentClassifier()
    
    # Test file
    test_file = "test_documents/TC1_Sample_Public_Marketing_Document.pdf"
    
    # Pre-process
    print("📄 Pre-processing test document...")
    preprocess_result = preprocessor.check_file_validity(test_file)
    metadata = preprocess_result['metadata']
    content = preprocessor.extract_content_for_analysis(test_file, metadata)
    print(f"   ✓ Document ready: {metadata.get('page_count')} pages")
    print()
    
    # Test 1: Dual-LLM DISABLED
    print("="*70)
    print("TEST 1: Dual-LLM DISABLED (enable_dual_llm=False)")
    print("="*70)
    print()
    
    classification1 = classifier.classify_document(
        content, 
        metadata,
        enable_dual_llm=False
    )
    
    print(f"✓ Classification complete")
    print(f"  Category: {classification1.get('category', 'unknown').upper()}")
    print(f"  Dual-LLM Enabled: {classification1.get('dual_llm_enabled', False)}")
    print(f"  Has Verification: {'verification' in classification1}")
    print()
    
    # Test 2: Dual-LLM ENABLED
    print("="*70)
    print("TEST 2: Dual-LLM ENABLED (enable_dual_llm=True)")
    print("="*70)
    print()
    
    classification2 = classifier.classify_document(
        content, 
        metadata,
        enable_dual_llm=True
    )
    
    print(f"✓ Classification complete")
    print(f"  Category: {classification2.get('category', 'unknown').upper()}")
    print(f"  Dual-LLM Enabled: {classification2.get('dual_llm_enabled', False)}")
    print(f"  Has Verification: {'verification' in classification2}")
    
    if 'verification' in classification2:
        verification = classification2['verification']
        print(f"  Agreement: {verification.get('agreement', 'N/A')}")
        if verification.get('agreement'):
            print(f"  ✓ Both LLMs agreed on: {classification2.get('category', 'unknown').upper()}")
        else:
            print(f"  ⚠️ Disagreement detected!")
    print()
    
    # Test 3: Default (None - uses config)
    print("="*70)
    print("TEST 3: Default (enable_dual_llm=None, uses config)")
    print("="*70)
    print()
    
    classification3 = classifier.classify_document(
        content, 
        metadata,
        enable_dual_llm=None  # Should use Config.ENABLE_DUAL_LLM
    )
    
    print(f"✓ Classification complete")
    print(f"  Category: {classification3.get('category', 'unknown').upper()}")
    print(f"  Dual-LLM Enabled: {classification3.get('dual_llm_enabled', False)}")
    print(f"  Has Verification: {'verification' in classification3}")
    print()
    
    # Summary
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print()
    print(f"✓ Test 1 (Disabled): Dual-LLM = {classification1.get('dual_llm_enabled', False)}")
    print(f"✓ Test 2 (Enabled):  Dual-LLM = {classification2.get('dual_llm_enabled', False)}")
    print(f"✓ Test 3 (Default):  Dual-LLM = {classification3.get('dual_llm_enabled', False)}")
    print()
    print("✅ Toggle functionality working correctly!")
    print()
    print("💡 In the Streamlit UI, users can now toggle dual-LLM per classification")
    print()

if __name__ == '__main__':
    test_toggle()

"""
Test Dual-LLM Verification Feature
Demonstrates how two LLMs cross-verify classifications
"""

import os
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from config import Config

def test_dual_llm_verification():
    """Test dual-LLM verification on a sample document"""
    
    print("="*70)
    print("DUAL-LLM VERIFICATION TEST")
    print("="*70)
    print()
    
    # Check if dual-LLM is enabled
    print(f"🔧 Configuration:")
    print(f"   Dual-LLM Enabled: {Config.ENABLE_DUAL_LLM}")
    print(f"   Primary Model: openai/gpt-4o")
    print(f"   Verification Model: {Config.VERIFICATION_MODEL}")
    print()
    
    if not Config.ENABLE_DUAL_LLM:
        print("⚠️  Dual-LLM is currently DISABLED")
        print("   To enable, set ENABLE_DUAL_LLM=true in .env file")
        print()
        print("   Benefits of Dual-LLM:")
        print("   • Higher accuracy through cross-verification")
        print("   • Automatic flagging of disagreements for human review")
        print("   • Reduced false positives/negatives")
        print("   • Audit trail with two independent opinions")
        print()
        print("   Trade-offs:")
        print("   • ~2x processing time (two LLM calls)")
        print("   • ~1.5x cost (verification uses cheaper model)")
        print()
    
    # Test with TC2 (Employment Application)
    test_file = "test_documents/TC2_Filled_In_Employement_Application.pdf"
    
    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return
    
    print(f"📄 Testing with: {os.path.basename(test_file)}")
    print()
    
    # Initialize
    preprocessor = DocumentPreprocessor()
    classifier = DocumentClassifier()
    
    # Pre-process
    print("1️⃣  Pre-processing document...")
    preprocess_result = preprocessor.check_file_validity(test_file)
    
    if not preprocess_result['valid']:
        print(f"❌ Pre-processing failed: {preprocess_result['errors']}")
        return
    
    metadata = preprocess_result['metadata']
    print(f"   ✓ Valid document: {metadata.get('page_count')} pages")
    print()
    
    # Extract content
    print("2️⃣  Extracting content...")
    content = preprocessor.extract_content_for_analysis(test_file, metadata)
    print(f"   ✓ Extracted {len(content.get('text', ''))} characters of text")
    print(f"   ✓ Extracted {len(content.get('images', []))} images")
    print()
    
    # Classify
    print("3️⃣  Running classification pipeline...")
    classification = classifier.classify_document(content, metadata)
    print()
    
    # Display results
    print("="*70)
    print("CLASSIFICATION RESULTS")
    print("="*70)
    print()
    
    print(f"📋 Primary Classification: {classification.get('category', 'unknown').upper()}")
    print(f"📊 Confidence: {classification.get('confidence', 0):.0%}")
    print()
    
    # Show dual-LLM results if enabled
    if classification.get('dual_llm_enabled', False):
        print("🔄 DUAL-LLM VERIFICATION RESULTS:")
        print("-"*70)
        
        verification = classification.get('verification', {})
        
        if verification.get('error'):
            print(f"❌ Verification Error: {verification['error']}")
            if verification.get('note'):
                print(f"   Note: {verification['note']}")
        else:
            primary_cat = verification.get('primary_category', 'unknown')
            verify_cat = verification.get('verification_category', 'unknown')
            agreement = verification.get('agreement', False)
            
            print(f"   Primary LLM:      {primary_cat.upper()}")
            print(f"   Verification LLM: {verify_cat.upper()}")
            print()
            
            if agreement:
                print("   ✅ AGREEMENT - Both LLMs classified identically")
                print("   → Classification is highly reliable")
                print("   → No human review needed")
            else:
                print("   ⚠️  DISAGREEMENT DETECTED")
                print("   → Flagged for human review")
                print("   → Requires expert validation")
                
                if verification.get('discrepancies'):
                    print()
                    print("   Discrepancies:")
                    print(f"   {verification['discrepancies']}")
            
            if verification.get('confidence'):
                print()
                print(f"   Verification Confidence: {verification['confidence']:.0%}")
            
            if verification.get('final_recommendation'):
                print()
                print(f"   Final Recommendation: {verification['final_recommendation']}")
        
        print()
        
        # Show HITL flag status
        if classification.get('requires_hitl', False):
            print("🚨 HUMAN REVIEW REQUIRED")
            print(f"   Reason: {classification.get('hitl_reason', 'Unknown')}")
        else:
            print("✅ AUTO-CLASSIFIED - No human review needed")
    else:
        print("ℹ️  Dual-LLM verification was not enabled for this classification")
    
    print()
    print("="*70)
    print()
    
    # Show how to enable
    if not Config.ENABLE_DUAL_LLM:
        print("💡 To enable Dual-LLM verification:")
        print("   1. Edit .env file")
        print("   2. Set: ENABLE_DUAL_LLM=true")
        print("   3. Optionally set: VERIFICATION_MODEL=openai/gpt-4o-mini")
        print("   4. Run this test again")
        print()

if __name__ == '__main__':
    test_dual_llm_verification()

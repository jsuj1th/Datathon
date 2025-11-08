"""
Test Case 1: Public Marketing Document
"""

import os
import json
from datetime import datetime
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from config import Config

def test_tc1():
    """Test TC1 - Public Marketing Document"""
    
    print("="*70)
    print("TEST CASE 1: Public Marketing Document")
    print("="*70)
    print(f"File: TC1_Sample_Public_Marketing_Document.pdf")
    print(f"Expected Category: Public")
    print(f"Expected: Page count, image count, public content citations")
    print("="*70)
    
    # Check API key
    if not Config.OPENROUTER_API_KEY or Config.OPENROUTER_API_KEY == 'your_gemini_api_key_here':
        print("\n❌ ERROR: OpenRouter API key not configured!")
        print("\nPlease edit the .env file and add your API key:")
        print("  OPENROUTER_API_KEY=your-actual-key-here")
        print("\nYou can get an API key from: https://makersuite.google.com/app/apikey")
        return
    
    filepath = "test_documents/TC1_Sample_Public_Marketing_Document.pdf"
    
    if not os.path.exists(filepath):
        print(f"\n❌ Test file not found: {filepath}")
        return
    
    print("\n[STEP 1/3] Pre-processing Document...")
    print("-"*70)
    
    preprocessor = DocumentPreprocessor()
    preprocess_result = preprocessor.check_file_validity(filepath)
    
    if not preprocess_result['valid']:
        print(f"❌ Pre-processing failed: {preprocess_result['errors']}")
        return
    
    metadata = preprocess_result['metadata']
    
    print(f"✓ Document is valid and legible")
    print(f"\nPre-processing Results:")
    print(f"  📄 Number of pages: {metadata.get('page_count', 0)}")
    print(f"  🖼️  Number of images: {metadata.get('image_count', 0)}")
    print(f"  📝 Has text content: {metadata.get('has_text', False)}")
    print(f"  ✓ Is legible: {metadata.get('is_legible', True)}")
    print(f"  📊 Text length: {len(metadata.get('text_content', ''))} characters")
    
    print("\n[STEP 2/3] Extracting Content for Analysis...")
    print("-"*70)
    
    content = preprocessor.extract_content_for_analysis(filepath, metadata)
    
    print(f"✓ Content extracted successfully")
    print(f"  📝 Text content: {len(content.get('text', ''))} characters")
    print(f"  🖼️  Images for analysis: {len(content.get('images', []))} images")
    
    print("\n[STEP 3/3] Classifying Document with AI...")
    print("-"*70)
    print("⏳ This may take 10-20 seconds...")
    
    try:
        classifier = DocumentClassifier()
        classification = classifier.classify_document(content, metadata)
        
        print("✓ Classification complete!")
        
        # Display Results
        print("\n" + "="*70)
        print("CLASSIFICATION RESULTS")
        print("="*70)
        
        category = classification.get('category', 'unknown').upper()
        confidence = classification.get('confidence', 0)
        
        print(f"\n📋 Category: {category}")
        print(f"📊 Confidence: {confidence:.1%}")
        print(f"✓ Safety Check: {'SAFE for children' if classification.get('safety_check', True) else '⚠️ UNSAFE'}")
        
        # Check if matches expected
        expected = 'public'
        actual = classification.get('category', '').lower().replace(' ', '_')
        match = actual == expected
        
        print(f"\n{'='*70}")
        print(f"Expected: PUBLIC")
        print(f"Actual: {category}")
        print(f"Result: {'✅ PASS' if match else '❌ FAIL'}")
        print(f"{'='*70}")
        
        # Evidence & Citations
        print(f"\n📑 EVIDENCE & CITATIONS")
        print("-"*70)
        
        evidence_list = classification.get('evidence', [])
        if evidence_list:
            for idx, evidence in enumerate(evidence_list, 1):
                # Handle both dict and string evidence
                if isinstance(evidence, dict):
                    print(f"\n{idx}. {evidence.get('type', 'Evidence').upper()}")
                    
                    if 'location' in evidence:
                        print(f"   📍 Location: {evidence['location']}")
                    
                    if 'details' in evidence:
                        details = evidence['details']
                        if isinstance(details, list):
                            for detail in details[:5]:
                                if isinstance(detail, dict):
                                    print(f"   • {detail}")
                                else:
                                    print(f"   • {detail}")
                        else:
                            print(f"   {details}")
                    
                    if 'page_citations' in evidence:
                        print(f"   📄 Pages: {evidence['page_citations']}")
                else:
                    # If evidence is a string, just print it
                    print(f"\n{idx}. {evidence}")
        else:
            print("⚠️  No specific evidence citations provided")
        
        # Reasoning
        print(f"\n💭 REASONING")
        print("-"*70)
        reasoning = classification.get('reasoning', 'No reasoning provided')
        print(reasoning)
        
        # Classification Stages
        if 'stages' in classification:
            print(f"\n🔍 CLASSIFICATION STAGES")
            print("-"*70)
            for stage_name, stage_result in classification['stages'].items():
                status = "✓" if 'error' not in stage_result else "❌"
                print(f"{status} {stage_name.replace('_', ' ').title()}")
                if 'error' in stage_result:
                    print(f"   Error: {stage_result['error']}")
        
        # Summary for TC1
        print(f"\n{'='*70}")
        print("TC1 EVALUATION SUMMARY")
        print("="*70)
        print(f"✓ Pre-processing: PASS")
        print(f"  - Pages detected: {metadata.get('page_count', 0)}")
        print(f"  - Images detected: {metadata.get('image_count', 0)}")
        print(f"✓ Classification: {'PASS' if match else 'FAIL'}")
        print(f"  - Category: {category} (Expected: PUBLIC)")
        print(f"  - Confidence: {confidence:.1%}")
        print(f"✓ Evidence: {'PASS' if evidence_list else 'NEEDS IMPROVEMENT'}")
        print(f"  - Citations provided: {len(evidence_list)}")
        print(f"✓ Safety: {'PASS' if classification.get('safety_check', True) else 'FAIL'}")
        print(f"  - Content safe for kids: {classification.get('safety_check', True)}")
        
        # Save detailed report
        report = {
            'test_case': 'TC1',
            'timestamp': datetime.now().isoformat(),
            'file': 'TC1_Sample_Public_Marketing_Document.pdf',
            'expected_category': 'Public',
            'results': {
                'preprocessing': {
                    'page_count': metadata.get('page_count', 0),
                    'image_count': metadata.get('image_count', 0),
                    'has_text': metadata.get('has_text', False),
                    'is_legible': metadata.get('is_legible', True)
                },
                'classification': classification,
                'match': match
            }
        }
        
        report_file = f"tc1_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        if match:
            print("\n🎉 TEST CASE 1: PASSED!")
        else:
            print("\n⚠️  TEST CASE 1: FAILED - Review classification logic")
        
    except Exception as e:
        print(f"\n❌ Classification failed with error:")
        print(f"   {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == '__main__':
    test_tc1()

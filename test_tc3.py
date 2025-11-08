"""
Test Case 3: Internal Memo (No PII)
"""

import os
import json
from datetime import datetime
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from config import Config

def test_tc3():
    """Test TC3 - Internal Memo without PII"""
    
    print("="*70)
    print("TEST CASE 3: Internal Memo (No PII)")
    print("="*70)
    print(f"File: TC3_Sample_Internal_Memo.pdf")
    print(f"Expected Category: Confidential")
    print(f"Expected: Internal content detection, NO PII, clear reasoning")
    print("="*70)
    
    # Check API key
    if not Config.OPENROUTER_API_KEY or Config.OPENROUTER_API_KEY == 'your_gemini_api_key_here':
        print("\n❌ ERROR: OpenRouter API key not configured!")
        return
    
    filepath = "test_documents/TC3_Sample_Internal_Memo.pdf"
    
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
        expected = 'confidential'
        actual = classification.get('category', '').lower().replace(' ', '_')
        match = actual == expected
        
        print(f"\n{'='*70}")
        print(f"Expected: CONFIDENTIAL")
        print(f"Actual: {category}")
        print(f"Result: {'✅ PASS' if match else '❌ FAIL'}")
        print(f"{'='*70}")
        
        # Evidence & Citations
        print(f"\n📑 EVIDENCE & CITATIONS (Internal Content)")
        print("-"*70)
        
        evidence_list = classification.get('evidence', [])
        internal_found = False
        pii_found = False
        
        if evidence_list:
            for idx, evidence in enumerate(evidence_list, 1):
                if isinstance(evidence, dict):
                    if 'finding' in evidence:
                        print(f"\n{idx}. INTERNAL CONTENT DETECTED")
                        print(f"   📍 {evidence['finding']}")
                        if 'locations' in evidence:
                            print(f"   📄 Location: {', '.join(evidence['locations'])}")
                        if 'internal' in evidence['finding'].lower() or 'research' in evidence['finding'].lower():
                            internal_found = True
                        if 'pii' in evidence['finding'].lower() or 'personal' in evidence['finding'].lower():
                            pii_found = True
                    else:
                        evidence_type = evidence.get('type', 'Evidence')
                        print(f"\n{idx}. {evidence_type.upper()}")
                        
                        if 'location' in evidence:
                            print(f"   📍 Location: {evidence['location']}")
                        
                        if 'details' in evidence:
                            details = evidence['details']
                            if isinstance(details, str):
                                print(f"   {details}")
                                if 'internal' in details.lower():
                                    internal_found = True
                        
                        if 'page_citations' in evidence:
                            print(f"   📄 Pages: {evidence['page_citations']}")
                else:
                    print(f"\n{idx}. {evidence}")
                    if 'internal' in str(evidence).lower():
                        internal_found = True
        else:
            print("⚠️  No specific evidence citations provided")
        
        # Reasoning
        print(f"\n💭 REASONING")
        print("-"*70)
        reasoning = classification.get('reasoning', 'No reasoning provided')
        print(reasoning)
        
        # Check for PII false positives
        print(f"\n🔍 PII VERIFICATION")
        print("-"*70)
        if pii_found:
            print("⚠️  WARNING: PII detected in internal memo (should be none)")
        else:
            print("✓ No PII detected (correct for internal memo)")
        
        # Classification Stages
        if 'stages' in classification:
            print(f"\n🔍 CLASSIFICATION STAGES")
            print("-"*70)
            for stage_name, stage_result in classification['stages'].items():
                status = "✓" if 'error' not in stage_result else "❌"
                print(f"{status} {stage_name.replace('_', ' ').title()}")
                if 'error' in stage_result:
                    print(f"   Error: {stage_result['error']}")
                
                # Show PII detection results
                if stage_name == 'pii_detection' and 'error' not in stage_result:
                    if stage_result.get('pii_found'):
                        print(f"   ⚠️  PII Detected (unexpected for internal memo)")
                    else:
                        print(f"   ✓ No PII found (correct)")
        
        # Summary for TC3
        print(f"\n{'='*70}")
        print("TC3 EVALUATION SUMMARY")
        print("="*70)
        print(f"✓ Pre-processing: PASS")
        print(f"  - Pages detected: {metadata.get('page_count', 0)}")
        print(f"  - Images detected: {metadata.get('image_count', 0)}")
        print(f"{'✓' if match else '✗'} Classification: {'PASS' if match else 'FAIL'}")
        print(f"  - Category: {category} (Expected: CONFIDENTIAL)")
        print(f"  - Confidence: {confidence:.1%}")
        print(f"{'✓' if internal_found else '✗'} Internal Content Detection: {'PASS' if internal_found else 'FAIL'}")
        print(f"  - Internal markers found: {internal_found}")
        print(f"{'✓' if not pii_found else '✗'} No PII False Positives: {'PASS' if not pii_found else 'FAIL'}")
        print(f"  - PII incorrectly detected: {pii_found}")
        print(f"✓ Evidence: {'PASS' if evidence_list else 'NEEDS IMPROVEMENT'}")
        print(f"  - Citations provided: {len(evidence_list)}")
        print(f"✓ Safety: {'PASS' if classification.get('safety_check', True) else 'FAIL'}")
        print(f"  - Content safe for kids: {classification.get('safety_check', True)}")
        
        # Save detailed report
        report = {
            'test_case': 'TC3',
            'timestamp': datetime.now().isoformat(),
            'file': 'TC3_Sample_Internal_Memo.pdf',
            'expected_category': 'Confidential',
            'results': {
                'preprocessing': {
                    'page_count': metadata.get('page_count', 0),
                    'image_count': metadata.get('image_count', 0),
                    'has_text': metadata.get('has_text', False),
                    'is_legible': metadata.get('is_legible', True)
                },
                'classification': classification,
                'match': match,
                'internal_content_detected': internal_found,
                'pii_false_positive': pii_found
            }
        }
        
        report_file = f"tc3_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        if match and internal_found and not pii_found:
            print("\n🎉 TEST CASE 3: PASSED!")
        elif match:
            print("\n⚠️  TEST CASE 3: PARTIAL PASS - Category correct but evidence needs improvement")
        else:
            print("\n❌ TEST CASE 3: FAILED - Review classification logic")
        
    except Exception as e:
        print(f"\n❌ Classification failed with error:")
        print(f"   {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == '__main__':
    test_tc3()

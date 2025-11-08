"""
Test Case 2: Employment Application with PII
"""

import os
import json
from datetime import datetime
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from config import Config

def test_tc2():
    """Test TC2 - Employment Application with PII"""
    
    print("="*70)
    print("TEST CASE 2: Employment Application with PII")
    print("="*70)
    print(f"File: TC2_Filled_In_Employement_Application.pdf")
    print(f"Expected Category: Highly Sensitive")
    print(f"Expected: PII detection (SSN, name, address, phone)")
    print("="*70)
    
    # Check API key
    if not Config.OPENROUTER_API_KEY or Config.OPENROUTER_API_KEY == 'your_gemini_api_key_here':
        print("\n❌ ERROR: OpenRouter API key not configured!")
        print("\nPlease edit the .env file and add your API key:")
        print("  OPENROUTER_API_KEY=your-actual-key-here")
        return
    
    filepath = "test_documents/TC2_Filled_In_Employement_Application.pdf"
    
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
        expected = 'highly_sensitive'
        actual = classification.get('category', '').lower().replace(' ', '_')
        match = actual == expected
        
        print(f"\n{'='*70}")
        print(f"Expected: HIGHLY SENSITIVE")
        print(f"Actual: {category}")
        print(f"Result: {'✅ PASS' if match else '❌ FAIL'}")
        print(f"{'='*70}")
        
        # Evidence & Citations
        print(f"\n📑 EVIDENCE & CITATIONS (PII Detection)")
        print("-"*70)
        
        evidence_list = classification.get('evidence', [])
        pii_found = False
        
        if evidence_list:
            for idx, evidence in enumerate(evidence_list, 1):
                # Handle both dict and string evidence
                if isinstance(evidence, dict):
                    # Check for different evidence formats
                    if 'finding' in evidence:
                        # OpenRouter format with finding
                        print(f"\n{idx}. PII DETECTED")
                        print(f"   📍 {evidence['finding']}")
                        if 'locations' in evidence:
                            print(f"   📄 Location: {', '.join(evidence['locations'])}")
                        pii_found = True
                    else:
                        evidence_type = evidence.get('type', 'Evidence')
                        print(f"\n{idx}. {evidence_type.upper()}")
                        
                        if 'location' in evidence:
                            print(f"   📍 Location: {evidence['location']}")
                        
                        if 'details' in evidence:
                            details = evidence['details']
                            if isinstance(details, list):
                                for detail in details:
                                    if isinstance(detail, dict):
                                        # PII detail
                                        pii_type = detail.get('pii_type', detail.get('type', 'PII'))
                                        location = detail.get('location', 'Unknown')
                                        severity = detail.get('severity', 'unknown')
                                        print(f"   • {pii_type}: {location} (Severity: {severity})")
                                        pii_found = True
                                    else:
                                        print(f"   • {detail}")
                            else:
                                print(f"   {details}")
                        
                        if 'page_citations' in evidence:
                            print(f"   📄 Pages: {evidence['page_citations']}")
                else:
                    # If evidence is a string, just print it
                    print(f"\n{idx}. {evidence}")
                    if 'SSN' in str(evidence) or 'social security' in str(evidence).lower():
                        pii_found = True
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
                
                # Show PII detection details
                if stage_name == 'pii_detection' and 'error' not in stage_result:
                    if stage_result.get('pii_found'):
                        print(f"   ✓ PII Detected!")
                        if 'pii_elements' in stage_result:
                            for pii in stage_result['pii_elements'][:5]:
                                if isinstance(pii, dict):
                                    print(f"     - {pii.get('type', 'PII')}: {pii.get('location', 'Unknown')}")
        
        # Summary for TC2
        print(f"\n{'='*70}")
        print("TC2 EVALUATION SUMMARY")
        print("="*70)
        print(f"✓ Pre-processing: PASS")
        print(f"  - Pages detected: {metadata.get('page_count', 0)}")
        print(f"  - Images detected: {metadata.get('image_count', 0)}")
        print(f"{'✓' if match else '✗'} Classification: {'PASS' if match else 'FAIL'}")
        print(f"  - Category: {category} (Expected: HIGHLY SENSITIVE)")
        print(f"  - Confidence: {confidence:.1%}")
        print(f"{'✓' if pii_found else '✗'} PII Detection: {'PASS' if pii_found else 'FAIL'}")
        print(f"  - PII elements found: {len(evidence_list)}")
        print(f"  - SSN/sensitive data detected: {pii_found}")
        print(f"✓ Evidence: {'PASS' if evidence_list else 'NEEDS IMPROVEMENT'}")
        print(f"  - Citations provided: {len(evidence_list)}")
        print(f"✓ Safety: {'PASS' if classification.get('safety_check', True) else 'FAIL'}")
        print(f"  - Content safe for kids: {classification.get('safety_check', True)}")
        
        # Save detailed report
        report = {
            'test_case': 'TC2',
            'timestamp': datetime.now().isoformat(),
            'file': 'TC2_Filled_In_Employement_Application.pdf',
            'expected_category': 'Highly Sensitive',
            'results': {
                'preprocessing': {
                    'page_count': metadata.get('page_count', 0),
                    'image_count': metadata.get('image_count', 0),
                    'has_text': metadata.get('has_text', False),
                    'is_legible': metadata.get('is_legible', True)
                },
                'classification': classification,
                'match': match,
                'pii_detected': pii_found
            }
        }
        
        report_file = f"tc2_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        if match and pii_found:
            print("\n🎉 TEST CASE 2: PASSED!")
        elif match:
            print("\n⚠️  TEST CASE 2: PARTIAL PASS - Category correct but PII detection needs improvement")
        else:
            print("\n❌ TEST CASE 2: FAILED - Review classification logic")
        
    except Exception as e:
        print(f"\n❌ Classification failed with error:")
        print(f"   {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == '__main__':
    test_tc2()

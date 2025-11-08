"""
Run all 5 test cases and generate a comprehensive report
"""

import os
import json
from datetime import datetime
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from config import Config

def run_test_case(tc_number, filepath, expected_category):
    """Run a single test case"""
    print(f"\n{'='*70}")
    print(f"TEST CASE {tc_number}")
    print(f"File: {os.path.basename(filepath)}")
    print(f"Expected Category: {expected_category}")
    print('='*70)
    
    preprocessor = DocumentPreprocessor()
    classifier = DocumentClassifier()
    
    # Pre-process
    print("\n[1/3] Pre-processing...")
    preprocess_result = preprocessor.check_file_validity(filepath)
    
    if not preprocess_result['valid']:
        print(f"❌ Pre-processing failed: {preprocess_result['errors']}")
        return None
    
    metadata = preprocess_result['metadata']
    print(f"✓ Valid document")
    print(f"  - Pages: {metadata.get('page_count', 0)}")
    print(f"  - Images: {metadata.get('image_count', 0)}")
    print(f"  - Has text: {metadata.get('has_text', False)}")
    print(f"  - Legible: {metadata.get('is_legible', True)}")
    
    # Extract content
    print("\n[2/3] Extracting content...")
    content = preprocessor.extract_content_for_analysis(filepath, metadata)
    print(f"✓ Content extracted")
    print(f"  - Text length: {len(content.get('text', ''))} chars")
    print(f"  - Images for analysis: {len(content.get('images', []))}")
    
    # Classify
    print("\n[3/3] Classifying...")
    classification = classifier.classify_document(content, metadata)
    
    # Display results
    print(f"\n{'─'*70}")
    print("RESULTS")
    print('─'*70)
    print(f"Category: {classification.get('category', 'unknown').upper()}")
    print(f"Confidence: {classification.get('confidence', 0):.2%}")
    print(f"Safety Check: {'✓ Safe' if classification.get('safety_check', True) else '⚠️ Unsafe'}")
    
    # Match with expected
    actual_category = classification.get('category', '').lower().replace(' ', '_')
    expected_normalized = expected_category.lower().replace(' ', '_')
    match = actual_category == expected_normalized
    
    print(f"\nExpected: {expected_category}")
    print(f"Actual: {classification.get('category', 'unknown')}")
    print(f"Match: {'✓ PASS' if match else '✗ FAIL'}")
    
    # Evidence
    print(f"\n{'─'*70}")
    print("EVIDENCE & CITATIONS")
    print('─'*70)
    
    if classification.get('evidence'):
        for idx, evidence in enumerate(classification['evidence'], 1):
            print(f"\n{idx}. {evidence.get('type', 'Evidence').upper()}")
            if 'location' in evidence:
                print(f"   Location: {evidence['location']}")
            if 'details' in evidence:
                details = evidence['details']
                if isinstance(details, list):
                    for detail in details[:3]:  # Show first 3
                        print(f"   - {detail}")
                else:
                    print(f"   {details}")
    else:
        print("No specific evidence citations provided")
    
    # Reasoning
    print(f"\n{'─'*70}")
    print("REASONING")
    print('─'*70)
    print(classification.get('reasoning', 'No reasoning provided'))
    
    # Stages
    if 'stages' in classification:
        print(f"\n{'─'*70}")
        print("CLASSIFICATION STAGES")
        print('─'*70)
        for stage_name, stage_result in classification['stages'].items():
            print(f"\n{stage_name.upper()}:")
            if 'error' in stage_result:
                print(f"  Error: {stage_result['error']}")
            else:
                print(f"  ✓ Completed")
    
    return {
        'test_case': tc_number,
        'file': os.path.basename(filepath),
        'expected': expected_category,
        'actual': classification.get('category', 'unknown'),
        'match': match,
        'confidence': classification.get('confidence', 0),
        'page_count': metadata.get('page_count', 0),
        'image_count': metadata.get('image_count', 0),
        'safety_check': classification.get('safety_check', True),
        'evidence_count': len(classification.get('evidence', [])),
        'classification': classification
    }

def main():
    """Run all test cases"""
    
    # Check API key
    if not Config.OPENAI_API_KEY:
        print("❌ ERROR: OPENAI_API_KEY not configured")
        print("Please set your API key in the .env file")
        return
    
    print("="*70)
    print("AI DOCUMENT CLASSIFICATION SYSTEM - TEST SUITE")
    print("="*70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Dual-LLM Enabled: {Config.ENABLE_DUAL_LLM}")
    
    # Define test cases
    test_cases = [
        {
            'number': 'TC1',
            'file': 'test_documents/TC1_Sample_Public_Marketing_Document.pdf',
            'expected': 'Public',
            'description': 'Public Marketing Document'
        },
        {
            'number': 'TC2',
            'file': 'test_documents/TC2_Filled_In_Employement_Application.pdf',
            'expected': 'Highly Sensitive',
            'description': 'Employment Application with PII'
        },
        {
            'number': 'TC3',
            'file': 'test_documents/TC3_Sample_Internal_Memo.pdf',
            'expected': 'Confidential',
            'description': 'Internal Memo'
        },
        {
            'number': 'TC4',
            'file': 'test_documents/TC4_ Stealth_Fighter_With_Part_Names.pdf',
            'expected': 'Confidential',
            'description': 'Stealth Fighter with Part Names'
        },
        {
            'number': 'TC5',
            'file': 'test_documents/TC5_Testing_Multiple_Non_Compliance_Categorization.pdf',
            'expected': 'Unsafe',  # or Confidential + Unsafe
            'description': 'Multiple Non-Compliance Categories'
        }
    ]
    
    results = []
    
    for tc in test_cases:
        if not os.path.exists(tc['file']):
            print(f"\n❌ Test file not found: {tc['file']}")
            continue
        
        result = run_test_case(tc['number'], tc['file'], tc['expected'])
        if result:
            results.append(result)
    
    # Summary
    print(f"\n\n{'='*70}")
    print("TEST SUMMARY")
    print('='*70)
    
    passed = sum(1 for r in results if r['match'])
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total} ({passed/total*100:.1f}%)")
    print(f"\nDetailed Results:")
    print(f"{'TC':<6} {'Expected':<20} {'Actual':<20} {'Confidence':<12} {'Status'}")
    print('-'*70)
    
    for r in results:
        status = '✓ PASS' if r['match'] else '✗ FAIL'
        print(f"{r['test_case']:<6} {r['expected']:<20} {r['actual']:<20} {r['confidence']:.1%}{'':>8} {status}")
    
    # Save detailed report
    report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': total,
                'passed': passed,
                'failed': total - passed,
                'pass_rate': passed/total if total > 0 else 0
            },
            'results': results
        }, f, indent=2)
    
    print(f"\n✓ Detailed report saved to: {report_file}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Review the results above.")

if __name__ == '__main__':
    main()

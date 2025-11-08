"""
Test Case 5: Multiple Non-Compliance Categorizations
"""

import os
import json
from datetime import datetime
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from config import Config

def test_tc5():
    """Test TC5 - Document with multiple violations (Confidential + Unsafe)"""
    
    print("="*70)
    print("TEST CASE 5: Multiple Non-Compliance Categorizations")
    print("="*70)
    print(f"File: TC5_Testing_Multiple_Non_Compliance_Categorization.pdf")
    print(f"Expected Category: Unsafe (highest priority) + Confidential")
    print(f"Expected: Multiple violation types detected with citations")
    print("="*70)
    
    # Check API key
    if not Config.OPENROUTER_API_KEY or Config.OPENROUTER_API_KEY == 'your_gemini_api_key_here':
        print("\n❌ ERROR: OpenRouter API key not configured!")
        return
    
    filepath = "test_documents/TC5_Testing_Multiple_Non_Compliance_Categorization.pdf"
    
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
    print("⏳ This may take 15-30 seconds (analyzing for multiple violations)...")
    
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
        safety_check = classification.get('safety_check', True)
        
        print(f"\n📋 Primary Category: {category}")
        print(f"📊 Confidence: {confidence:.1%}")
        print(f"⚠️  Safety Check: {'SAFE for children' if safety_check else '⚠️ UNSAFE - FLAGGED'}")
        
        # Check if matches expected (Unsafe should be primary, but should also detect confidential content)
        expected_primary = 'unsafe'
        actual = classification.get('category', '').lower().replace(' ', '_')
        primary_match = actual == expected_primary
        
        print(f"\n{'='*70}")
        print(f"Expected Primary: UNSAFE (with Confidential content also detected)")
        print(f"Actual Primary: {category}")
        print(f"Primary Category: {'✅ PASS' if primary_match else '❌ FAIL'}")
        print(f"Safety Flag: {'✅ PASS' if not safety_check else '❌ FAIL (should be unsafe)'}")
        print(f"{'='*70}")
        
        # Evidence & Citations - Look for MULTIPLE violation types
        print(f"\n📑 EVIDENCE & CITATIONS (Multiple Violations)")
        print("-"*70)
        
        evidence_list = classification.get('evidence', [])
        unsafe_found = False
        confidential_found = False
        technical_found = False
        violation_types = set()
        
        if evidence_list:
            for idx, evidence in enumerate(evidence_list, 1):
                if isinstance(evidence, dict):
                    if 'finding' in evidence:
                        finding_lower = evidence['finding'].lower()
                        
                        # Determine violation type
                        violation_type = "UNKNOWN"
                        if any(word in finding_lower for word in ['unsafe', 'hate', 'violent', 'criminal', 'exploitative', 'threat']):
                            violation_type = "⚠️ UNSAFE CONTENT"
                            unsafe_found = True
                            violation_types.add('unsafe')
                        elif any(word in finding_lower for word in ['technical', 'aviation', 'flight', 'manual', 'specification']):
                            violation_type = "🔒 CONFIDENTIAL CONTENT"
                            confidential_found = True
                            technical_found = True
                            violation_types.add('confidential')
                        elif any(word in finding_lower for word in ['proprietary', 'internal', 'sensitive']):
                            violation_type = "🔒 CONFIDENTIAL CONTENT"
                            confidential_found = True
                            violation_types.add('confidential')
                        
                        print(f"\n{idx}. {violation_type}")
                        print(f"   📍 {evidence['finding']}")
                        if 'locations' in evidence:
                            print(f"   📄 Location: {', '.join(evidence['locations'])}")
                    else:
                        evidence_type = evidence.get('type', 'Evidence')
                        print(f"\n{idx}. {evidence_type.upper()}")
                        
                        if 'location' in evidence:
                            print(f"   📍 Location: {evidence['location']}")
                        
                        if 'details' in evidence:
                            details = evidence['details']
                            if isinstance(details, str):
                                print(f"   {details}")
                                if 'unsafe' in details.lower():
                                    unsafe_found = True
                                    violation_types.add('unsafe')
                                if 'confidential' in details.lower() or 'technical' in details.lower():
                                    confidential_found = True
                                    violation_types.add('confidential')
                else:
                    print(f"\n{idx}. {evidence}")
                    evidence_str = str(evidence).lower()
                    if 'unsafe' in evidence_str:
                        unsafe_found = True
                        violation_types.add('unsafe')
                    if 'confidential' in evidence_str or 'technical' in evidence_str:
                        confidential_found = True
                        violation_types.add('confidential')
        else:
            print("⚠️  No specific evidence citations provided")
        
        # Reasoning
        print(f"\n💭 REASONING & POLICY EXPLANATION")
        print("-"*70)
        reasoning = classification.get('reasoning', 'No reasoning provided')
        print(reasoning)
        
        # Multiple Violations Check
        print(f"\n🔍 MULTIPLE VIOLATIONS DETECTED")
        print("-"*70)
        print(f"Violation types found: {len(violation_types)}")
        for vtype in violation_types:
            print(f"  • {vtype.upper()}")
        
        if len(violation_types) >= 2:
            print("✓ Multiple violation types detected (as expected)")
        else:
            print("⚠️  Only one violation type detected (expected multiple)")
        
        # Classification Stages
        if 'stages' in classification:
            print(f"\n🔍 CLASSIFICATION STAGES")
            print("-"*70)
            for stage_name, stage_result in classification['stages'].items():
                status = "✓" if 'error' not in stage_result else "❌"
                print(f"{status} {stage_name.replace('_', ' ').title()}")
                if 'error' in stage_result:
                    print(f"   Error: {stage_result['error']}")
        
        # Summary for TC5
        print(f"\n{'='*70}")
        print("TC5 EVALUATION SUMMARY")
        print("="*70)
        print(f"✓ Pre-processing: PASS")
        print(f"  - Pages detected: {metadata.get('page_count', 0)}")
        print(f"  - Images detected: {metadata.get('image_count', 0)}")
        print(f"{'✓' if primary_match else '✗'} Primary Classification: {'PASS' if primary_match else 'FAIL'}")
        print(f"  - Category: {category} (Expected: UNSAFE)")
        print(f"  - Confidence: {confidence:.1%}")
        print(f"{'✓' if not safety_check else '✗'} Safety Flag: {'PASS' if not safety_check else 'FAIL'}")
        print(f"  - Content flagged as unsafe: {not safety_check}")
        print(f"{'✓' if len(violation_types) >= 2 else '✗'} Multiple Violations: {'PASS' if len(violation_types) >= 2 else 'FAIL'}")
        print(f"  - Violation types detected: {len(violation_types)}")
        print(f"  - Unsafe content: {unsafe_found}")
        print(f"  - Confidential content: {confidential_found}")
        print(f"✓ Evidence: {'PASS' if evidence_list else 'NEEDS IMPROVEMENT'}")
        print(f"  - Citations provided: {len(evidence_list)}")
        
        # Save detailed report
        report = {
            'test_case': 'TC5',
            'timestamp': datetime.now().isoformat(),
            'file': 'TC5_Testing_Multiple_Non_Compliance_Categorization.pdf',
            'expected_category': 'Unsafe (with Confidential)',
            'results': {
                'preprocessing': {
                    'page_count': metadata.get('page_count', 0),
                    'image_count': metadata.get('image_count', 0),
                    'has_text': metadata.get('has_text', False),
                    'is_legible': metadata.get('is_legible', True)
                },
                'classification': classification,
                'primary_match': primary_match,
                'safety_flagged': not safety_check,
                'violation_types': list(violation_types),
                'multiple_violations_detected': len(violation_types) >= 2
            }
        }
        
        report_file = f"tc5_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        # Overall pass criteria
        overall_pass = primary_match and not safety_check and len(violation_types) >= 2
        
        if overall_pass:
            print("\n🎉 TEST CASE 5: PASSED!")
            print("   ✓ Unsafe content detected as primary category")
            print("   ✓ Safety check correctly flagged")
            print("   ✓ Multiple violation types identified")
        elif primary_match and not safety_check:
            print("\n⚠️  TEST CASE 5: PARTIAL PASS")
            print("   ✓ Unsafe category correct")
            print("   ✓ Safety flagged")
            print("   ⚠️  Multiple violations detection needs improvement")
        else:
            print("\n❌ TEST CASE 5: FAILED")
            if not primary_match:
                print("   ✗ Primary category should be UNSAFE")
            if safety_check:
                print("   ✗ Safety check should flag content as unsafe")
        
    except Exception as e:
        print(f"\n❌ Classification failed with error:")
        print(f"   {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == '__main__':
    test_tc5()

"""
Test Case 4: Stealth Fighter with Part Names
"""

import os
import json
from datetime import datetime
from preprocessor import DocumentPreprocessor
from classifier import DocumentClassifier
from config import Config

def test_tc4():
    """Test TC4 - Stealth Fighter with Part Names"""
    
    print("="*70)
    print("TEST CASE 4: Stealth Fighter with Part Names")
    print("="*70)
    print(f"File: TC4_ Stealth_Fighter_With_Part_Names.pdf")
    print(f"Expected Category: Confidential")
    print(f"Expected: Image analysis, technical content, policy explanation")
    print("="*70)
    
    # Check API key
    if not Config.OPENROUTER_API_KEY or Config.OPENROUTER_API_KEY == 'your_gemini_api_key_here':
        print("\n❌ ERROR: OpenRouter API key not configured!")
        return
    
    filepath = "test_documents/TC4_ Stealth_Fighter_With_Part_Names.pdf"
    
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
    print("⏳ This may take 15-30 seconds (analyzing images)...")
    
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
        
        # Check if matches expected (Confidential or Highly Sensitive both acceptable)
        expected_options = ['confidential', 'highly_sensitive']
        actual = classification.get('category', '').lower().replace(' ', '_')
        match = actual in expected_options
        
        print(f"\n{'='*70}")
        print(f"Expected: CONFIDENTIAL (or HIGHLY SENSITIVE)")
        print(f"Actual: {category}")
        print(f"Result: {'✅ PASS' if match else '❌ FAIL'}")
        print(f"{'='*70}")
        
        # Evidence & Citations
        print(f"\n📑 EVIDENCE & CITATIONS (Technical/Military Content)")
        print("-"*70)
        
        evidence_list = classification.get('evidence', [])
        technical_found = False
        military_found = False
        image_analysis = False
        
        if evidence_list:
            for idx, evidence in enumerate(evidence_list, 1):
                if isinstance(evidence, dict):
                    if 'finding' in evidence:
                        print(f"\n{idx}. TECHNICAL CONTENT DETECTED")
                        print(f"   📍 {evidence['finding']}")
                        if 'locations' in evidence:
                            print(f"   📄 Location: {', '.join(evidence['locations'])}")
                        
                        finding_lower = evidence['finding'].lower()
                        if any(word in finding_lower for word in ['technical', 'specification', 'aviation', 'aircraft', 'flight', 'manual']):
                            technical_found = True
                        if any(word in finding_lower for word in ['military', 'fighter', 'defense', 'stealth']):
                            military_found = True
                        if any(word in finding_lower for word in ['image', 'diagram', 'figure', 'illustration']):
                            image_analysis = True
                    else:
                        evidence_type = evidence.get('type', 'Evidence')
                        print(f"\n{idx}. {evidence_type.upper()}")
                        
                        if 'location' in evidence:
                            print(f"   📍 Location: {evidence['location']}")
                        
                        if 'details' in evidence:
                            details = evidence['details']
                            if isinstance(details, str):
                                print(f"   {details}")
                                if 'technical' in details.lower() or 'aviation' in details.lower():
                                    technical_found = True
                        
                        if 'page_citations' in evidence:
                            print(f"   📄 Pages: {evidence['page_citations']}")
                else:
                    print(f"\n{idx}. {evidence}")
                    if 'technical' in str(evidence).lower() or 'aviation' in str(evidence).lower():
                        technical_found = True
        else:
            print("⚠️  No specific evidence citations provided")
        
        # Reasoning
        print(f"\n💭 REASONING & POLICY EXPLANATION")
        print("-"*70)
        reasoning = classification.get('reasoning', 'No reasoning provided')
        print(reasoning)
        
        # Check for image analysis
        print(f"\n🖼️  IMAGE ANALYSIS")
        print("-"*70)
        if len(content.get('images', [])) > 0:
            print(f"✓ {len(content.get('images', []))} image(s) processed for analysis")
            if image_analysis:
                print("✓ Image content referenced in evidence")
            else:
                print("⚠️  Image content not explicitly mentioned in evidence")
        else:
            print("⚠️  No images extracted for analysis")
        
        # Classification Stages
        if 'stages' in classification:
            print(f"\n🔍 CLASSIFICATION STAGES")
            print("-"*70)
            for stage_name, stage_result in classification['stages'].items():
                status = "✓" if 'error' not in stage_result else "❌"
                print(f"{status} {stage_name.replace('_', ' ').title()}")
                if 'error' in stage_result:
                    print(f"   Error: {stage_result['error']}")
                
                # Show proprietary detection results
                if stage_name == 'proprietary_detection' and 'error' not in stage_result:
                    if stage_result.get('proprietary_found'):
                        print(f"   ✓ Proprietary/Technical content detected")
        
        # Summary for TC4
        print(f"\n{'='*70}")
        print("TC4 EVALUATION SUMMARY")
        print("="*70)
        print(f"✓ Pre-processing: PASS")
        print(f"  - Pages detected: {metadata.get('page_count', 0)}")
        print(f"  - Images detected: {metadata.get('image_count', 0)}")
        print(f"{'✓' if match else '✗'} Classification: {'PASS' if match else 'FAIL'}")
        print(f"  - Category: {category} (Expected: CONFIDENTIAL)")
        print(f"  - Confidence: {confidence:.1%}")
        print(f"{'✓' if technical_found else '✗'} Technical Content Detection: {'PASS' if technical_found else 'FAIL'}")
        print(f"  - Technical/aviation content found: {technical_found}")
        print(f"{'✓' if len(content.get('images', [])) > 0 else '✗'} Image Processing: {'PASS' if len(content.get('images', [])) > 0 else 'FAIL'}")
        print(f"  - Images analyzed: {len(content.get('images', []))}")
        print(f"✓ Evidence: {'PASS' if evidence_list else 'NEEDS IMPROVEMENT'}")
        print(f"  - Citations provided: {len(evidence_list)}")
        print(f"✓ Safety: {'PASS' if classification.get('safety_check', True) else 'FAIL'}")
        print(f"  - Content safe for kids: {classification.get('safety_check', True)}")
        
        # Save detailed report
        report = {
            'test_case': 'TC4',
            'timestamp': datetime.now().isoformat(),
            'file': 'TC4_ Stealth_Fighter_With_Part_Names.pdf',
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
                'technical_content_detected': technical_found,
                'military_content_detected': military_found,
                'images_analyzed': len(content.get('images', []))
            }
        }
        
        report_file = f"tc4_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        if match and technical_found:
            print("\n🎉 TEST CASE 4: PASSED!")
        elif match:
            print("\n⚠️  TEST CASE 4: PARTIAL PASS - Category correct but evidence needs improvement")
        else:
            print("\n❌ TEST CASE 4: FAILED - Review classification logic")
        
    except Exception as e:
        print(f"\n❌ Classification failed with error:")
        print(f"   {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == '__main__':
    test_tc4()

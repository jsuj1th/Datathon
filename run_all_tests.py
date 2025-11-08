"""
Run all test cases and generate summary report
"""

import subprocess
import sys

def run_test(test_file, test_name):
    """Run a single test and capture results"""
    print(f"\n{'='*70}")
    print(f"Running {test_name}...")
    print('='*70)
    
    result = subprocess.run(
        [sys.executable, test_file],
        capture_output=True,
        text=True
    )
    
    # Extract key metrics from output
    output = result.stdout
    
    # Look for PASS/FAIL
    if "PASSED!" in output:
        status = "✅ PASS"
    elif "PARTIAL PASS" in output:
        status = "⚠️  PARTIAL"
    else:
        status = "❌ FAIL"
    
    # Extract category and confidence
    category = "Unknown"
    confidence = "0%"
    pages = "?"
    images = "?"
    
    for line in output.split('\n'):
        if "Actual:" in line and "Category" not in line:
            category = line.split("Actual:")[1].strip()
        elif "Confidence:" in line and "📊" in line:
            confidence = line.split("Confidence:")[1].strip()
        elif "Pages detected:" in line:
            pages = line.split(":")[-1].strip()
        elif "Images detected:" in line:
            images = line.split(":")[-1].strip()
    
    return {
        'status': status,
        'category': category,
        'confidence': confidence,
        'pages': pages,
        'images': images
    }

def main():
    """Run all tests"""
    print("="*70)
    print("AI DOCUMENT CLASSIFICATION SYSTEM - FULL TEST SUITE")
    print("="*70)
    
    tests = [
        ('test_tc1.py', 'TC1: Public Marketing Document'),
        ('test_tc2.py', 'TC2: Employment Application (PII)'),
        ('test_tc3.py', 'TC3: Internal Memo'),
        ('test_tc4.py', 'TC4: Flight Operations Manual'),
    ]
    
    results = []
    
    for test_file, test_name in tests:
        result = run_test(test_file, test_name)
        results.append((test_name, result))
    
    # Print summary
    print(f"\n\n{'='*70}")
    print("TEST SUMMARY")
    print('='*70)
    print(f"\n{'Test Case':<40} {'Status':<12} {'Category':<20} {'Confidence':<12}")
    print('-'*70)
    
    for test_name, result in results:
        print(f"{test_name:<40} {result['status']:<12} {result['category']:<20} {result['confidence']:<12}")
    
    print(f"\n{'='*70}")
    print("DETAILED METRICS")
    print('='*70)
    print(f"\n{'Test Case':<40} {'Pages':<8} {'Images':<8}")
    print('-'*70)
    
    for test_name, result in results:
        print(f"{test_name:<40} {result['pages']:<8} {result['images']:<8}")
    
    # Count passes
    passed = sum(1 for _, r in results if '✅' in r['status'])
    total = len(results)
    
    print(f"\n{'='*70}")
    print(f"OVERALL RESULT: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print('='*70)
    
    if passed == total:
        print("\n🎉 All tests PASSED! System is ready for evaluation.")
    else:
        print(f"\n⚠️  {total - passed} test(s) need attention.")

if __name__ == '__main__':
    main()

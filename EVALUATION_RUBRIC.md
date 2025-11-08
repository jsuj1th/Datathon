# Evaluation Rubric

## Scoring Criteria

This document outlines how the AI Document Classification System will be evaluated against the 5 test cases.

---

## Test Case 1: Public Marketing Document

### Input
- **File**: TC1_Sample_Public_Marketing_Document.pdf
- **Content**: Hitachi EverFlex brochure (8 pages)
- **Expected Category**: Public

### Evaluation Points (20 points)

| Criteria | Points | Requirements |
|----------|--------|--------------|
| Correct Classification | 8 | Category = "Public" |
| Pre-processing Accuracy | 3 | Correct page count (8), image count |
| Evidence Quality | 5 | Cites specific pages with marketing content |
| Safety Check | 2 | Content safe for kids = true |
| Reasoning Clarity | 2 | Clear explanation why it's public |

### Expected Output

```json
{
  "category": "public",
  "confidence": 0.85-0.95,
  "page_count": 8,
  "image_count": 10-15,
  "safety_check": true,
  "evidence": [
    {
      "type": "public_content",
      "location": "Pages 1-8",
      "details": "Marketing materials for Hitachi EverFlex services"
    }
  ],
  "reasoning": "Document contains only public marketing materials..."
}
```

### Pass Criteria
- ✓ Category = Public
- ✓ Page count = 8
- ✓ Evidence cites specific pages
- ✓ No PII detected
- ✓ Safety check passes

---

## Test Case 2: Employment Application with PII

### Input
- **File**: TC2_Filled_In_Employement_Application.pdf
- **Content**: Completed employment application (4 pages)
- **Expected Category**: Highly Sensitive

### Evaluation Points (20 points)

| Criteria | Points | Requirements |
|----------|--------|--------------|
| Correct Classification | 8 | Category = "Highly Sensitive" |
| PII Detection | 6 | Identifies SSN field, name, address, phone |
| Pre-processing Accuracy | 2 | Correct page count (4) |
| Evidence Citations | 3 | Specific field locations cited |
| Safety Check | 1 | Content safe for kids = true |

### Expected Output

```json
{
  "category": "highly_sensitive",
  "confidence": 0.90-0.98,
  "page_count": 4,
  "image_count": 0,
  "safety_check": true,
  "evidence": [
    {
      "type": "pii_detected",
      "details": [
        {
          "pii_type": "SSN",
          "location": "Page 1, Section 2",
          "severity": "high"
        },
        {
          "pii_type": "full_name_with_address",
          "location": "Page 1, Personal Information",
          "severity": "high"
        },
        {
          "pii_type": "phone_number",
          "location": "Page 1",
          "severity": "medium"
        }
      ]
    }
  ],
  "reasoning": "Document contains multiple PII elements including SSN field..."
}
```

### Pass Criteria
- ✓ Category = Highly Sensitive
- ✓ PII detected (SSN, name, address, phone)
- ✓ Page count = 4
- ✓ Specific field citations provided
- ✓ High confidence score (>0.85)

---

## Test Case 3: Internal Memo

### Input
- **File**: TC3_Sample_Internal_Memo.pdf
- **Content**: Research proposal/internal memo (3 pages)
- **Expected Category**: Confidential

### Evaluation Points (20 points)

| Criteria | Points | Requirements |
|----------|--------|--------------|
| Correct Classification | 8 | Category = "Confidential" |
| Internal Content Detection | 5 | Identifies internal/non-public nature |
| Pre-processing Accuracy | 2 | Correct page count (3) |
| Evidence Quality | 3 | Cites internal operational details |
| No PII False Positives | 2 | Correctly identifies no PII present |

### Expected Output

```json
{
  "category": "confidential",
  "confidence": 0.80-0.90,
  "page_count": 3,
  "image_count": 0-1,
  "safety_check": true,
  "evidence": [
    {
      "type": "internal_content",
      "location": "Pages 1-3",
      "details": "Research proposal with internal project details"
    }
  ],
  "reasoning": "Document contains internal research/project information..."
}
```

### Pass Criteria
- ✓ Category = Confidential
- ✓ Page count = 3
- ✓ No PII detected
- ✓ Internal content identified
- ✓ Clear policy reasoning

---

## Test Case 4: Stealth Fighter with Part Names

### Input
- **File**: TC4_ Stealth_Fighter_With_Part_Names.pdf
- **Content**: Flight operations manual (18 pages)
- **Expected Category**: Confidential

### Evaluation Points (20 points)

| Criteria | Points | Requirements |
|----------|--------|--------------|
| Correct Classification | 7 | Category = "Confidential" or "Highly Sensitive" |
| Image Analysis | 6 | Analyzes images/technical content |
| Pre-processing Accuracy | 2 | Correct page count (18) |
| Evidence Citations | 3 | Cites specific pages/regions |
| Policy Explanation | 2 | Explains why technical specs are confidential |

### Expected Output

```json
{
  "category": "confidential",
  "confidence": 0.85-0.95,
  "page_count": 18,
  "image_count": 5-10,
  "safety_check": true,
  "evidence": [
    {
      "type": "proprietary_content",
      "location": "Pages 1-18, Multiple images",
      "details": "Flight operations manual with technical specifications",
      "sensitivity_level": "high"
    }
  ],
  "reasoning": "Document contains technical aviation specifications..."
}
```

### Pass Criteria
- ✓ Category = Confidential (or Highly Sensitive)
- ✓ Page count = 18
- ✓ Technical content identified
- ✓ Image analysis performed
- ✓ Specific page citations

---

## Test Case 5: Multiple Non-Compliance Categories

### Input
- **File**: TC5_Testing_Multiple_Non_Compliance_Categorization.pdf
- **Content**: Mixed content with multiple violations (1 page)
- **Expected Category**: Unsafe (highest priority) + Confidential

### Evaluation Points (20 points)

| Criteria | Points | Requirements |
|----------|--------|--------------|
| Correct Primary Classification | 7 | Category = "Unsafe" (highest priority) |
| Multiple Violation Detection | 6 | Identifies both unsafe and confidential content |
| Pre-processing Accuracy | 1 | Correct page count (1) |
| Evidence for Each Violation | 4 | Separate citations for each issue |
| Safety Check | 2 | Content safe for kids = false |

### Expected Output

```json
{
  "category": "unsafe",
  "confidence": 0.90-0.98,
  "page_count": 1,
  "image_count": 1-2,
  "safety_check": false,
  "evidence": [
    {
      "type": "proprietary_content",
      "location": "Page 1, Image region",
      "details": "Technical specifications or military content"
    },
    {
      "type": "safety_violation",
      "location": "Page 1",
      "details": [
        {
          "violation_type": "hate_speech/violent_content/etc",
          "severity": "high"
        }
      ]
    }
  ],
  "reasoning": "Document contains both confidential content and unsafe material. Unsafe classification takes priority..."
}
```

### Pass Criteria
- ✓ Primary category = Unsafe
- ✓ Multiple violations detected
- ✓ Safety check = false
- ✓ Evidence for each violation type
- ✓ Clear explanation of priority

---

## Overall Scoring Summary

### Total Points: 100

| Test Case | Points | Focus Area |
|-----------|--------|------------|
| TC1 - Public | 20 | Basic classification, no false positives |
| TC2 - PII | 20 | PII detection accuracy |
| TC3 - Internal | 20 | Confidential content identification |
| TC4 - Technical | 20 | Image analysis, technical content |
| TC5 - Mixed | 20 | Priority handling, multiple violations |

### Grading Scale

- **90-100**: Excellent - Production ready
- **80-89**: Good - Minor improvements needed
- **70-79**: Satisfactory - Some issues to address
- **60-69**: Needs Work - Significant improvements required
- **<60**: Insufficient - Major rework needed

---

## Key Performance Indicators

### Classification Accuracy
- **Target**: >90% correct classifications
- **Measurement**: Matches expected category

### Evidence Quality
- **Target**: Specific page/field citations for all findings
- **Measurement**: Evidence includes exact locations

### Pre-processing Accuracy
- **Target**: 100% accurate page/image counts
- **Measurement**: Counts match actual document

### PII Detection Rate
- **Target**: >95% detection of PII elements
- **Measurement**: All PII types identified

### Safety Check Accuracy
- **Target**: 100% correct safety assessments
- **Measurement**: Unsafe content properly flagged

### Confidence Calibration
- **Target**: High confidence (>0.8) for clear cases
- **Measurement**: Confidence scores align with accuracy

---

## Bonus Points (Optional)

### Advanced Features (+10 points)

| Feature | Points | Description |
|---------|--------|-------------|
| Dual-LLM Verification | 3 | Two LLMs cross-verify classifications |
| HITL Auto-flagging | 2 | Correctly flags low-confidence cases |
| Detailed Audit Trail | 2 | Complete classification history |
| Performance Optimization | 2 | Fast processing (<15s per document) |
| UI/UX Excellence | 1 | Intuitive, business-friendly interface |

---

## Failure Modes to Avoid

### Critical Failures (Automatic Fail)
- ❌ Classifying PII document as Public
- ❌ Missing SSN in employment application
- ❌ Not flagging unsafe content
- ❌ System crashes or errors on valid input

### Major Issues (-10 points each)
- ⚠️ Incorrect page/image counts
- ⚠️ No evidence citations provided
- ⚠️ Wrong primary category on multiple tests
- ⚠️ False positives on PII detection

### Minor Issues (-5 points each)
- ⚠️ Low confidence on clear cases
- ⚠️ Vague reasoning without specifics
- ⚠️ Missing some PII elements
- ⚠️ Slow processing (>30s per document)

---

## Testing Procedure

### 1. Setup Verification
- [ ] All dependencies installed
- [ ] API keys configured
- [ ] Test documents loaded
- [ ] System starts without errors

### 2. Run Test Suite
```bash
python run_test_cases.py
```

### 3. Evaluate Each Test Case
- Check classification category
- Verify page/image counts
- Review evidence citations
- Assess reasoning quality
- Confirm safety checks

### 4. Calculate Score
- Sum points from all test cases
- Add bonus points if applicable
- Subtract points for issues
- Calculate final percentage

### 5. Generate Report
- Document all results
- Include screenshots
- Note any issues
- Provide recommendations

---

## Success Criteria

### Minimum Requirements
- ✓ All 5 test cases run successfully
- ✓ At least 4/5 correct classifications
- ✓ PII detected in TC2
- ✓ Unsafe content flagged in TC5
- ✓ Evidence citations provided

### Excellent Performance
- ✓ 5/5 correct classifications
- ✓ All PII elements detected
- ✓ Specific page/field citations
- ✓ High confidence scores (>0.85)
- ✓ Clear, detailed reasoning
- ✓ Fast processing (<15s)
- ✓ Intuitive UI

---

## Judging Focus Areas

### 1. Accuracy (40%)
- Correct category assignment
- PII detection completeness
- Safety violation identification

### 2. Evidence Quality (30%)
- Specific page citations
- Field-level references
- Clear, detailed descriptions

### 3. System Robustness (20%)
- Pre-processing reliability
- Error handling
- Performance consistency

### 4. User Experience (10%)
- UI clarity
- Result presentation
- Feedback mechanism

---

## Final Checklist

Before submission, verify:

- [ ] All test cases pass
- [ ] Evidence includes page numbers
- [ ] PII detection works correctly
- [ ] Safety checks are accurate
- [ ] UI is functional and clear
- [ ] Documentation is complete
- [ ] Code is well-organized
- [ ] System is production-ready

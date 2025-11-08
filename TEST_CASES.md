# Test Cases Documentation

## Overview

This document describes the 5 test cases for evaluating the AI Document Classification System.

## Test Case 1: Public Marketing Document

### Input
- **Type**: Multi-page PDF brochure or program viewbook
- **Content**: Public marketing materials, product information
- **Expected Category**: Public

### Expected Output
```json
{
  "category": "public",
  "confidence": 0.85-0.95,
  "page_count": 8,
  "image_count": 12,
  "safety_check": true,
  "evidence": [
    {
      "type": "public_content",
      "location": "Pages 1-8",
      "details": "Marketing statements, product features, public contact information"
    }
  ],
  "reasoning": "Document contains only public marketing materials with no PII or confidential information"
}
```

### Validation Points
- ✓ Correct classification as Public
- ✓ Accurate page and image counts
- ✓ No PII detected
- ✓ Content safe for children
- ✓ Evidence cites specific pages

---

## Test Case 2: Employment Application with PII

### Input
- **Type**: PDF form with filled information
- **Content**: Name, address, SSN, employment history
- **Expected Category**: Highly Sensitive

### Expected Output
```json
{
  "category": "highly_sensitive",
  "confidence": 0.90-0.98,
  "page_count": 3,
  "image_count": 0,
  "safety_check": true,
  "evidence": [
    {
      "type": "pii_detected",
      "details": [
        {
          "pii_type": "SSN",
          "location": "Page 1, Section 2",
          "value_pattern": "XXX-XX-XXXX"
        },
        {
          "pii_type": "full_name_with_address",
          "location": "Page 1, Section 1",
          "context": "Personal information section"
        }
      ]
    }
  ],
  "reasoning": "Document contains multiple PII elements including SSN, requiring highest sensitivity classification"
}
```

### Validation Points
- ✓ Correct classification as Highly Sensitive
- ✓ PII detection (SSN, address, name)
- ✓ Specific field citations
- ✓ Redaction suggestions (optional)
- ✓ Content safe for children

---

## Test Case 3: Internal Memo (No PII)

### Input
- **Type**: PDF document
- **Content**: Internal project milestones, risks, team discussions
- **Expected Category**: Confidential

### Expected Output
```json
{
  "category": "confidential",
  "confidence": 0.80-0.90,
  "page_count": 2,
  "image_count": 1,
  "safety_check": true,
  "evidence": [
    {
      "type": "internal_content",
      "location": "Pages 1-2",
      "details": "Internal project milestones, risk assessments, non-public operational details"
    }
  ],
  "reasoning": "Document contains internal business information not intended for public distribution, but no PII"
}
```

### Validation Points
- ✓ Correct classification as Confidential
- ✓ No PII detected
- ✓ Internal content identified
- ✓ Clear policy reasoning
- ✓ Content safe for children

---

## Test Case 4: Stealth Fighter Image

### Input
- **Type**: High-resolution image (PNG/JPG)
- **Content**: Military stealth fighter with part names/serial numbers
- **Expected Category**: Confidential or Highly Sensitive

### Expected Output
```json
{
  "category": "confidential",
  "confidence": 0.85-0.95,
  "page_count": 1,
  "image_count": 1,
  "safety_check": true,
  "evidence": [
    {
      "type": "proprietary_content",
      "location": "Image 1, Region: center-right",
      "details": "Military equipment with identifiable serial numbers and technical specifications",
      "sensitivity_level": "high"
    }
  ],
  "reasoning": "Image contains identifiable military equipment with technical details requiring confidential classification"
}
```

### Validation Points
- ✓ Correct classification as Confidential
- ✓ Image analysis performed
- ✓ Region-specific citations
- ✓ Policy explanation for military equipment
- ✓ Content safe for children

---

## Test Case 5: Mixed Content (Multiple Violations)

### Input
- **Type**: PDF document
- **Content**: Stealth fighter image + unsafe content (hate speech, violence, etc.)
- **Expected Category**: Multiple (Confidential + Unsafe)

### Expected Output
```json
{
  "category": "unsafe",
  "confidence": 0.90-0.98,
  "page_count": 3,
  "image_count": 2,
  "safety_check": false,
  "evidence": [
    {
      "type": "proprietary_content",
      "location": "Page 1, Image 1",
      "details": "Military equipment with technical specifications"
    },
    {
      "type": "safety_violation",
      "location": "Page 2",
      "details": [
        {
          "violation_type": "hate_speech",
          "severity": "high",
          "context": "Discriminatory language targeting protected groups"
        }
      ]
    }
  ],
  "reasoning": "Document contains both confidential military content and unsafe content violating child safety policies. Unsafe classification takes priority."
}
```

### Validation Points
- ✓ Unsafe classification (highest priority)
- ✓ Multiple evidence types detected
- ✓ Specific citations for each violation
- ✓ Clear policy explanations
- ✓ Flagged for human review
- ✓ Content NOT safe for children

---

## Testing Procedure

### 1. Prepare Test Documents

Place your 5 test PDFs in the `test_documents/` folder:
- `tc1_public_brochure.pdf`
- `tc2_employment_application.pdf`
- `tc3_internal_memo.pdf`
- `tc4_stealth_fighter.png`
- `tc5_mixed_content.pdf`

### 2. Run Interactive Tests

1. Start the application: `python app.py`
2. Open browser: http://localhost:5000
3. Upload each test document
4. Verify classification results
5. Check evidence citations
6. Submit feedback if corrections needed

### 3. Run Batch Tests

1. Navigate to "Batch Processing" tab
2. Upload all 5 test documents
3. Monitor real-time progress
4. Review aggregated results
5. Export results for analysis

### 4. Validate Results

For each test case, verify:
- ✓ Correct category classification
- ✓ Accurate page/image counts
- ✓ Specific evidence citations
- ✓ Clear reasoning provided
- ✓ Safety check results
- ✓ HITL flagging when appropriate

### 5. Test HITL Feedback

1. Submit corrected classifications
2. Add detailed notes
3. Check statistics dashboard
4. Verify feedback storage
5. Review agreement rates

---

## Evaluation Criteria

### Classification Accuracy (40%)
- Correct category assignment
- Appropriate confidence scores
- Proper priority handling (Unsafe > Highly Sensitive > Confidential > Public)

### Evidence Quality (30%)
- Specific page/image citations
- Detailed evidence descriptions
- Accurate location references
- Clear policy mappings

### Pre-processing (15%)
- Accurate page counts
- Correct image counts
- Legibility assessment
- Text extraction quality

### Safety & HITL (15%)
- Proper safety checks
- Appropriate HITL flagging
- Feedback mechanism functionality
- Statistics tracking

---

## Expected Performance

### Response Times
- Single document (interactive): 5-15 seconds
- Batch processing: 10-20 seconds per document
- Pre-processing checks: < 2 seconds

### Accuracy Targets
- Overall classification accuracy: > 90%
- PII detection rate: > 95%
- Safety violation detection: > 98%
- False positive rate: < 5%

### HITL Metrics
- Agreement rate with human reviewers: > 85%
- Appropriate flagging rate: 10-20% of documents
- Feedback incorporation: Real-time statistics updates

# Mixed Content Classification Guide

## Overview

The system now supports **mixed-content documents** that contain multiple classification levels within a single document. This reflects real-world scenarios where documents may have:
- Public marketing content + confidential technical specs
- General information + PII sections
- Safe content + unsafe material
- Internal memos + public announcements

## How It Works

### 1. **Full Document Analysis**

The system analyzes the ENTIRE document and identifies ALL content types:
- **Public**: Marketing, general information, public-facing content
- **Confidential**: Internal docs, technical specs, non-public content
- **Highly Sensitive**: PII, proprietary designs, sensitive data
- **Unsafe**: Hate speech, violence, child safety violations

### 2. **Weighted Classification**

Each category is assigned:
- **Percentage**: Proportion of document containing this type (0-100%)
- **Page Count**: Number of pages with this content
- **Reason**: Brief explanation of what was found

### 3. **Primary Category Selection**

The system uses **most restrictive** category as primary:

```
Priority (Highest to Lowest):
1. Unsafe (even 1% → Unsafe)
2. Highly Sensitive (>5% → Highly Sensitive)
3. Confidential (>50% → Confidential)
4. Public (>80% with no sensitive → Public)
```

## Example Scenarios

### Scenario 1: Marketing Brochure with Customer Testimonials

**Content Mix**:
- 90% Public (product info, marketing)
- 10% Confidential (customer names + companies)

**Result**:
- Primary: **Confidential** (contains identifiable customer info)
- Breakdown: 90% Public, 10% Confidential
- Reasoning: Customer testimonials with company names = confidential

### Scenario 2: Technical Manual with Public Introduction

**Content Mix**:
- 20% Public (introduction, overview)
- 80% Confidential (technical specifications)

**Result**:
- Primary: **Confidential** (majority is technical)
- Breakdown: 20% Public, 80% Confidential
- Reasoning: Technical specifications dominate

### Scenario 3: Internal Report with PII Section

**Content Mix**:
- 70% Confidential (internal analysis)
- 30% Highly Sensitive (employee PII)

**Result**:
- Primary: **Highly Sensitive** (PII present)
- Breakdown: 70% Confidential, 30% Highly Sensitive
- Reasoning: Any PII triggers highly sensitive

### Scenario 4: Document with Unsafe Content

**Content Mix**:
- 95% Public (general content)
- 5% Unsafe (hate speech on one page)

**Result**:
- Primary: **Unsafe** (any unsafe content)
- Breakdown: 95% Public, 5% Unsafe
- Reasoning: Even small amount of unsafe content requires unsafe classification

## Output Format

```json
{
  "primary_category": "confidential",
  "overall_classification": "confidential",
  "is_mixed_content": true,
  "category_breakdown": {
    "public": {
      "percentage": 40,
      "page_count": 4,
      "reason": "Marketing materials and product descriptions"
    },
    "confidential": {
      "percentage": 60,
      "page_count": 6,
      "reason": "Technical specifications and internal procedures"
    }
  },
  "confidence": 0.92,
  "evidence": [
    {
      "category": "public",
      "finding": "Pages 1-4 contain marketing materials...",
      "locations": ["Pages 1-4"],
      "policy_explanation": "Marketing materials = public"
    },
    {
      "category": "confidential",
      "finding": "Pages 5-10 contain technical specifications...",
      "locations": ["Pages 5-10, Technical Section"],
      "policy_explanation": "Technical specifications = confidential"
    }
  ],
  "reasoning": "Document contains 40% public marketing content and 60% confidential technical specifications. Using confidential as primary category (most restrictive for mixed content)."
}
```

## UI Display

When mixed content is detected, the UI shows:

1. **Warning Banner**: "⚠️ Mixed Content Detected"
2. **Breakdown Chart**: Visual representation of category percentages
3. **Per-Category Metrics**: Percentage and page count for each
4. **Primary Classification**: Highlighted with explanation
5. **Evidence by Category**: Grouped by classification level

## Benefits

### For Users:
- ✅ **Transparency**: See exactly what content types are in the document
- ✅ **Granular Understanding**: Know which pages contain what
- ✅ **Better Decisions**: Understand why a document got its classification

### For Compliance:
- ✅ **Audit Trail**: Clear breakdown of content types
- ✅ **Risk Assessment**: Identify sensitive sections
- ✅ **Selective Redaction**: Know which pages need protection

### For HITL:
- ✅ **Targeted Review**: Focus on sensitive sections
- ✅ **Context**: Understand the mix of content
- ✅ **Validation**: Verify percentage assessments

## Use Cases

### 1. **Corporate Documents**
- Annual reports (public financials + confidential strategy)
- Product documentation (public features + internal architecture)
- Marketing materials (public content + customer testimonials)

### 2. **Legal Documents**
- Contracts (public terms + confidential clauses)
- Court filings (public records + sealed information)
- Compliance reports (public summary + sensitive findings)

### 3. **Research Papers**
- Academic papers (public research + confidential data)
- Clinical trials (public results + patient PII)
- Technical reports (public findings + proprietary methods)

### 4. **Government Documents**
- Public notices (public announcements + internal notes)
- FOIA responses (public info + redacted sections)
- Policy documents (public policy + classified details)

## Configuration

The weightage thresholds can be adjusted in `prompt_library.py`:

```python
CLASSIFICATION LOGIC FOR MIXED CONTENT:
1. If ANY unsafe content exists (even 1%) → Primary = "unsafe"
2. If ANY highly sensitive content exists (>5%) → Primary = "highly_sensitive"
3. If confidential content is majority (>50%) → Primary = "confidential"
4. If public content is majority (>80%) and no sensitive content → Primary = "public"
```

## Testing

Run the mixed content test:
```bash
python test_mixed_content.py
```

Or use the Streamlit UI:
```bash
streamlit run demo_ui.py
```

Upload any document and the system will automatically detect and display mixed content if present.

## Summary

The mixed-content feature makes the system **production-ready for real-world scenarios** where documents rarely fit into a single category. It provides:
- **Accurate classification** based on content proportions
- **Transparent breakdown** of what's in the document
- **Flexible handling** of complex documents
- **Compliance-friendly** audit trails

This enhancement ensures the system works for **any general scenario** where users upload PDFs with varying content types.

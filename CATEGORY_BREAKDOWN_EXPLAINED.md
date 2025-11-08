# Category Breakdown - How It Works

## Overview

The category breakdown feature analyzes documents to determine what percentage of content falls into each classification level (Public, Confidential, Highly Sensitive, Unsafe). This provides transparency into mixed-content documents and helps users understand the composition of their documents.

## The Process

### Step 1: Document Analysis Request

When a document is classified, the LLM receives a prompt that explicitly asks for category breakdown:

```
IMPORTANT: Documents can contain MIXED CONTENT with multiple classification levels.

Analyze the ENTIRE document and identify ALL content types present:
- Public content (marketing, general info)
- Confidential content (internal docs, technical specs)
- Highly Sensitive content (PII, proprietary designs)
- Unsafe content (hate speech, violence, etc.)

Return JSON with:
{
  "category_breakdown": {
    "highly_sensitive": {
      "percentage": 0-100,
      "page_count": X,
      "reason": "brief explanation"
    },
    "confidential": {...},
    "public": {...},
    "unsafe": {...}
  }
}
```

### Step 2: LLM Analysis

The LLM (GPT-4o) analyzes the document and:

1. **Reads all text content** - Scans every page for classification markers
2. **Analyzes all images** - Examines diagrams, forms, photos for sensitive content
3. **Identifies content types** - Categorizes each section/page
4. **Calculates proportions** - Determines percentage of each category
5. **Provides reasoning** - Explains why content falls into each category

### Step 3: Response Format

The LLM returns a structured response:

```json
{
  "primary_category": "highly_sensitive",
  "category_breakdown": {
    "highly_sensitive": {
      "percentage": 75,
      "page_count": 3,
      "reason": "Pages 1-3 contain PII: full name, SSN field, address, phone numbers, employment history"
    },
    "confidential": {
      "percentage": 0,
      "page_count": 0,
      "reason": ""
    },
    "public": {
      "percentage": 25,
      "page_count": 1,
      "reason": "Page 4 contains general employment policy information available publicly"
    },
    "unsafe": {
      "percentage": 0,
      "page_count": 0,
      "reason": ""
    }
  },
  "overall_classification": "highly_sensitive",
  "is_mixed_content": true
}
```

### Step 4: Result Processing

The classifier processes this response:

```python
# In classifier.py - _aggregate_results()

# Extract breakdown from LLM response
aggregated['category_breakdown'] = base.get('category_breakdown', {})

# Ensure all categories are present (fill missing with 0%)
all_categories = ['public', 'confidential', 'highly_sensitive', 'unsafe']
for cat in all_categories:
    if cat not in aggregated['category_breakdown']:
        aggregated['category_breakdown'][cat] = {
            'percentage': 0,
            'page_count': 0,
            'reason': ''
        }
```

### Step 5: UI Display

The Streamlit UI displays the breakdown:

```python
# In demo_ui.py

breakdown = classification.get('category_breakdown', {})

# Show only categories with content
categories_with_content = {
    k: v for k, v in breakdown.items() 
    if v.get('percentage', 0) > 0
}

# Display in columns
for cat_name, cat_data in categories_with_content.items():
    st.metric(
        f"{cat_name.replace('_', ' ').title()}",
        f"{cat_data['percentage']}%",
        f"{cat_data['page_count']} pages"
    )
    st.caption(cat_data['reason'])
```

## How the LLM Determines Percentages

### Method 1: Page-Based Calculation (Most Common)

The LLM counts pages with each content type:

```
Example: 4-page employment application

Page 1: Personal info (name, address, SSN) → Highly Sensitive
Page 2: Employment history with references → Highly Sensitive  
Page 3: Education and skills → Highly Sensitive
Page 4: General employment policies → Public

Calculation:
- Highly Sensitive: 3/4 pages = 75%
- Public: 1/4 pages = 25%
```

### Method 2: Content Volume (For Mixed Pages)

If a single page has mixed content, the LLM estimates by content volume:

```
Example: 1-page document with mixed content

Top 80%: Technical specifications (confidential)
Bottom 20%: Public disclaimer

Calculation:
- Confidential: 80%
- Public: 20%
```

### Method 3: Severity Weighting

For documents with multiple classification levels, the LLM may weight by severity:

```
Example: Research document

- 10% contains participant PII → Highly Sensitive
- 60% contains proprietary research → Confidential
- 30% contains published background → Public

Even though PII is only 10%, it might trigger the entire 
document to be classified as Highly Sensitive (most restrictive)
```

## Classification Priority Logic

The system uses **most restrictive category** as primary:

```python
# Priority order (highest to lowest)
category_priority = {
    'unsafe': 4,        # Highest priority
    'highly_sensitive': 3,
    'confidential': 2,
    'public': 1         # Lowest priority
}
```

### Priority Rules:

1. **If ANY unsafe content exists (even 1%)** → Primary = "unsafe"
2. **If ANY highly sensitive content exists (>5%)** → Primary = "highly_sensitive"
3. **If confidential content is majority (>50%)** → Primary = "confidential"
4. **If public content is majority (>80%) and no sensitive content** → Primary = "public"

## Real-World Examples

### Example 1: Pure Document (Single Category)

**Document**: Marketing brochure (TC1)

```json
{
  "primary_category": "public",
  "category_breakdown": {
    "public": {
      "percentage": 100,
      "page_count": 8,
      "reason": "All pages contain public marketing materials"
    },
    "confidential": {"percentage": 0, "page_count": 0},
    "highly_sensitive": {"percentage": 0, "page_count": 0},
    "unsafe": {"percentage": 0, "page_count": 0}
  },
  "is_mixed_content": false
}
```

**Display**:
```
📊 Content Breakdown by Category
┌─────────────────┐
│ Public: 100%    │
│ 8 pages         │
└─────────────────┘
```

### Example 2: Mixed Document (Multiple Categories)

**Document**: Employment application with PII (TC2)

```json
{
  "primary_category": "highly_sensitive",
  "category_breakdown": {
    "highly_sensitive": {
      "percentage": 75,
      "page_count": 3,
      "reason": "Contains PII: SSN field, full name, address, phone, references"
    },
    "public": {
      "percentage": 25,
      "page_count": 1,
      "reason": "General employment policy information"
    },
    "confidential": {"percentage": 0, "page_count": 0},
    "unsafe": {"percentage": 0, "page_count": 0}
  },
  "is_mixed_content": true
}
```

**Display**:
```
⚠️ Mixed Content Detected

📊 Content Breakdown by Category
┌──────────────────┬──────────────────┐
│ Highly Sensitive │ Public           │
│ 75%              │ 25%              │
│ 3 pages          │ 1 page           │
│ Contains PII     │ General policies │
└──────────────────┴──────────────────┘

Primary Classification: HIGHLY_SENSITIVE
(Using most restrictive category for mixed content)
```

### Example 3: Complex Mixed Document

**Document**: Technical manual with multiple sections

```json
{
  "primary_category": "confidential",
  "category_breakdown": {
    "confidential": {
      "percentage": 60,
      "page_count": 12,
      "reason": "Technical specifications, serial numbers, operational procedures"
    },
    "highly_sensitive": {
      "percentage": 10,
      "page_count": 2,
      "reason": "Maintenance logs with technician names and IDs"
    },
    "public": {
      "percentage": 30,
      "page_count": 6,
      "reason": "General safety warnings and public disclaimers"
    },
    "unsafe": {"percentage": 0, "page_count": 0}
  },
  "is_mixed_content": true
}
```

**Display**:
```
⚠️ Mixed Content Detected

📊 Content Breakdown by Category
┌──────────────────┬──────────────────┬──────────────────┐
│ Highly Sensitive │ Confidential     │ Public           │
│ 10%              │ 60%              │ 30%              │
│ 2 pages          │ 12 pages         │ 6 pages          │
│ Technician IDs   │ Tech specs       │ Safety warnings  │
└──────────────────┴──────────────────┴──────────────────┘

Primary Classification: CONFIDENTIAL
(Highly Sensitive content present but confidential is majority)
```

## How It Handles Edge Cases

### Edge Case 1: Borderline Content

**Scenario**: Content that could be classified multiple ways

```
Example: Research proposal (could be public sample or confidential)

LLM Analysis:
- Checks for "SAMPLE" or "TEMPLATE" markers
- Looks for actual proprietary research data
- Considers document context and metadata

Decision:
- If marked as sample but contains real research → Confidential
- If generic template with no real data → Public
```

### Edge Case 2: Redacted Content

**Scenario**: Document with redacted sections

```
Example: Employment application with [REDACTED] SSN

LLM Analysis:
- Recognizes redaction markers
- Identifies that PII fields exist (even if redacted)
- Classifies based on document purpose

Decision:
- Presence of PII fields → Highly Sensitive
- Reason: "Contains PII collection fields (SSN, address)"
```

### Edge Case 3: Minimal Sensitive Content

**Scenario**: Mostly public document with tiny sensitive section

```
Example: 100-page manual with 1 page of serial numbers

LLM Analysis:
- 99 pages: Public technical information
- 1 page: Serial numbers (confidential)

Breakdown:
- Public: 99%
- Confidential: 1%

Decision:
- Primary: Confidential (most restrictive rule)
- Reason: "Even 1% confidential content requires protection"
```

## Technical Implementation

### Prompt Engineering

The prompt explicitly instructs the LLM to analyze content distribution:

```python
# From prompt_library.py

"""
Analyze the ENTIRE document and identify ALL content types present:
- Public content (marketing, general info)
- Confidential content (internal docs, technical specs)
- Highly Sensitive content (PII, proprietary designs)
- Unsafe content (hate speech, violence, etc.)

Return JSON with these exact fields:
{
  "category_breakdown": {
    "highly_sensitive": {
      "percentage": 0-100,
      "page_count": X,
      "reason": "brief explanation"
    },
    ...
  }
}

CLASSIFICATION LOGIC FOR MIXED CONTENT:
1. If ANY unsafe content exists (even 1%) → Primary = "unsafe"
2. If ANY highly sensitive content exists (>5%) → Primary = "highly_sensitive"
3. If confidential content is majority (>50%) → Primary = "confidential"
4. If public content is majority (>80%) and no sensitive content → Primary = "public"
5. Always use the MOST RESTRICTIVE category as primary for mixed documents
"""
```

### Aggregation Logic

```python
# From classifier.py

def _aggregate_results(self, stages, metadata):
    # Extract breakdown from base classification
    aggregated['category_breakdown'] = base.get('category_breakdown', {})
    
    # Ensure all categories present
    all_categories = ['public', 'confidential', 'highly_sensitive', 'unsafe']
    for cat in all_categories:
        if cat not in aggregated['category_breakdown']:
            aggregated['category_breakdown'][cat] = {
                'percentage': 0,
                'page_count': 0,
                'reason': ''
            }
    
    # Apply priority logic
    if safety_check shows unsafe:
        aggregated['category'] = 'unsafe'
    elif pii_detection shows PII:
        aggregated['category'] = 'highly_sensitive'
    elif proprietary_detection shows proprietary:
        aggregated['category'] = 'confidential'
    else:
        # Use LLM's primary classification
        aggregated['category'] = base.get('overall_classification')
```

### Fallback Handling

If the LLM doesn't provide breakdown (old format or error):

```python
# Create a simple breakdown showing 100% of detected category
if not aggregated['category_breakdown']:
    category = base.get('category', 'public')
    aggregated['category_breakdown'] = {
        'public': {'percentage': 0, 'page_count': 0, 'reason': ''},
        'confidential': {'percentage': 0, 'page_count': 0, 'reason': ''},
        'highly_sensitive': {'percentage': 0, 'page_count': 0, 'reason': ''},
        'unsafe': {'percentage': 0, 'page_count': 0, 'reason': ''}
    }
    aggregated['category_breakdown'][category] = {
        'percentage': 100,
        'page_count': metadata.get('page_count', 0),
        'reason': f'Entire document classified as {category}'
    }
```

## Benefits of Category Breakdown

### 1. Transparency
Users see exactly what content triggered each classification level

### 2. Audit Trail
Clear documentation of why a document was classified a certain way

### 3. Compliance
Helps meet regulatory requirements for data classification

### 4. Risk Assessment
Quantifies the amount of sensitive content in a document

### 5. Redaction Guidance
Shows which pages/sections need protection or redaction

### 6. Training Data
Provides detailed feedback for improving classification accuracy

## Validation & Quality Control

### Consistency Checks

The system validates that percentages add up:

```python
# Validation (not currently implemented but recommended)
total_percentage = sum(
    cat_data.get('percentage', 0) 
    for cat_data in breakdown.values()
)

if total_percentage != 100:
    # Log warning or adjust proportionally
    logger.warning(f"Percentages don't sum to 100: {total_percentage}")
```

### Dual-LLM Verification

When dual-LLM is enabled, both models provide breakdowns:

```python
Primary LLM Breakdown:
- Highly Sensitive: 75%
- Public: 25%

Verification LLM Breakdown:
- Highly Sensitive: 80%
- Public: 20%

Agreement Check:
- Both agree on primary category: Highly Sensitive ✓
- Slight difference in percentages (acceptable)
```

## Future Enhancements

### Planned Improvements

1. **Page-Level Breakdown**
   - Show classification for each individual page
   - Visual heatmap of sensitive content

2. **Section-Level Analysis**
   - Break down by document sections
   - Identify specific paragraphs with sensitive content

3. **Confidence Scoring per Category**
   - Show confidence for each category percentage
   - Highlight uncertain classifications

4. **Historical Tracking**
   - Track breakdown changes over document versions
   - Show trends in content classification

5. **Custom Weighting**
   - Allow users to define custom priority rules
   - Adjust sensitivity thresholds

---

## Summary

The category breakdown feature works by:

1. **Prompting the LLM** to analyze all content types in the document
2. **Calculating percentages** based on page count or content volume
3. **Applying priority logic** to determine the primary classification
4. **Providing transparency** with reasons for each category
5. **Displaying visually** in the UI with metrics and explanations

This gives users complete visibility into document composition and helps them understand why documents are classified the way they are, especially for mixed-content documents that contain multiple classification levels.

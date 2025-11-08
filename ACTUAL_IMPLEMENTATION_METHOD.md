# Actual Implementation Method - Category Breakdown

## TL;DR

**Method Used: LLM-Based Analysis with Prompt Instructions**

The codebase uses **Method 1: LLM Self-Analysis** where the GPT-4o model itself calculates the percentages based on explicit prompt instructions. The system does NOT manually count pages or calculate percentages in Python code.

## How It Actually Works

### Step 1: Prompt Instructions

The system sends this prompt to GPT-4o:

```python
# From prompt_library.py - get_base_classification_prompt()

"""
IMPORTANT: Documents can contain MIXED CONTENT with multiple classification levels.

Analyze the ENTIRE document and identify ALL content types present:
- Public content (marketing, general info)
- Confidential content (internal docs, technical specs)
- Highly Sensitive content (PII, proprietary designs)
- Unsafe content (hate speech, violence, etc.)

Return JSON with these exact fields:
{
  "category_breakdown": {
    "highly_sensitive": {"percentage": 0-100, "page_count": X, "reason": "brief explanation"},
    "confidential": {"percentage": 0-100, "page_count": X, "reason": "brief explanation"},
    "public": {"percentage": 0-100, "page_count": X, "reason": "brief explanation"},
    "unsafe": {"percentage": 0-100, "page_count": X, "reason": "brief explanation"}
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

### Step 2: LLM Calculates Percentages

**The LLM (GPT-4o) does all the work:**

1. Reads the entire document (text + images)
2. Identifies which pages/sections contain which content types
3. Calculates percentages (likely using page-based counting)
4. Determines page counts for each category
5. Provides reasoning for each category

**Example LLM Response:**
```json
{
  "primary_category": "highly_sensitive",
  "category_breakdown": {
    "highly_sensitive": {
      "percentage": 75,
      "page_count": 3,
      "reason": "Pages 1-3 contain PII: full name, SSN field, address, phone numbers"
    },
    "confidential": {
      "percentage": 0,
      "page_count": 0,
      "reason": ""
    },
    "public": {
      "percentage": 25,
      "page_count": 1,
      "reason": "Page 4 contains general employment policy information"
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

### Step 3: Python Code Extracts the Response

The classifier simply extracts what the LLM calculated:

```python
# From classifier.py - _aggregate_results()

# Extract the breakdown directly from LLM response
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

### Step 4: Fallback for Old Format

If the LLM doesn't provide breakdown (backward compatibility):

```python
# Old format - create simple 100% breakdown
aggregated['category_breakdown'] = {
    'public': {'percentage': 0, 'page_count': 0, 'reason': ''},
    'confidential': {'percentage': 0, 'page_count': 0, 'reason': ''},
    'highly_sensitive': {'percentage': 0, 'page_count': 0, 'reason': ''},
    'unsafe': {'percentage': 0, 'page_count': 0, 'reason': ''}
}

# Set detected category to 100%
aggregated['category_breakdown'][category] = {
    'percentage': 100,
    'page_count': metadata.get('page_count', 0),
    'reason': f'Entire document classified as {category.replace("_", " ")}'
}
```

## What the Python Code Does vs What the LLM Does

### Python Code Responsibilities:
1. ✅ Send prompt with instructions to LLM
2. ✅ Receive JSON response from LLM
3. ✅ Extract `category_breakdown` from response
4. ✅ Fill in missing categories with 0%
5. ✅ Apply priority logic for final classification
6. ✅ Handle errors and fallbacks

### LLM (GPT-4o) Responsibilities:
1. ✅ Read and analyze entire document
2. ✅ Identify content types on each page
3. ✅ **Calculate percentages** (page-based or content-based)
4. ✅ **Count pages** for each category
5. ✅ **Provide reasoning** for each category
6. ✅ Determine if content is mixed
7. ✅ Return structured JSON response

## The Actual Calculation Method

Based on the prompt and LLM behavior, **GPT-4o likely uses Page-Based Calculation**:

```
Example: 4-page employment application

LLM Analysis:
- Page 1: Personal info section → Highly Sensitive
- Page 2: Employment history → Highly Sensitive  
- Page 3: References with contact info → Highly Sensitive
- Page 4: General employment policies → Public

LLM Calculation:
- Highly Sensitive: 3 pages / 4 total = 75%
- Public: 1 page / 4 total = 25%

LLM Response:
{
  "category_breakdown": {
    "highly_sensitive": {
      "percentage": 75,
      "page_count": 3,
      "reason": "Pages 1-3 contain PII"
    },
    "public": {
      "percentage": 25,
      "page_count": 1,
      "reason": "Page 4 contains general policies"
    }
  }
}
```

## Why This Approach?

### Advantages:

1. **Leverages LLM Intelligence**
   - GPT-4o understands context and nuance
   - Can handle complex mixed content
   - Adapts to different document types

2. **No Manual Page Counting**
   - No need to parse PDF structure in Python
   - No need to track which page has what content
   - Simpler codebase

3. **Flexible and Adaptive**
   - LLM can use different methods (page-based, content-based, severity-based)
   - Adjusts to document characteristics
   - Handles edge cases intelligently

4. **Reasoning Included**
   - LLM explains why each percentage was assigned
   - Provides transparency
   - Helps with auditing

### Disadvantages:

1. **Less Deterministic**
   - Same document might get slightly different percentages on different runs
   - Depends on LLM's interpretation

2. **No Direct Control**
   - Can't force specific calculation method
   - Relies on prompt engineering

3. **Validation Challenges**
   - Hard to verify if percentages are "correct"
   - Percentages might not always sum to exactly 100%

## Evidence from Test Runs

Looking at actual test results, we can see the LLM provides breakdowns like:

```python
# TC2 - Employment Application (from test runs)
{
  "category_breakdown": {
    "highly_sensitive": {
      "percentage": 95,  # LLM calculated this
      "page_count": 4,   # LLM counted pages
      "reason": "Contains extensive PII throughout"
    },
    "public": {
      "percentage": 5,
      "page_count": 0,
      "reason": "Minor public disclaimers"
    }
  }
}
```

The percentages and page counts come directly from the LLM's analysis, not from Python calculations.

## Code Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  1. Python: Build prompt with instructions                  │
│     - Include category breakdown requirements               │
│     - Specify JSON format                                   │
│     - Provide classification rules                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. Python: Send to OpenRouter API (GPT-4o)                 │
│     - Document text                                         │
│     - Image descriptions                                    │
│     - Metadata                                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. GPT-4o: Analyze document                                │
│     ✓ Read all pages                                        │
│     ✓ Identify content types                                │
│     ✓ Calculate percentages (page-based)                    │
│     ✓ Count pages per category                             │
│     ✓ Generate reasoning                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. GPT-4o: Return JSON response                            │
│     {                                                        │
│       "category_breakdown": {                               │
│         "highly_sensitive": {                               │
│           "percentage": 75,  ← LLM calculated               │
│           "page_count": 3,   ← LLM counted                  │
│           "reason": "..."    ← LLM explained                │
│         }                                                    │
│       }                                                      │
│     }                                                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  5. Python: Extract breakdown from response                 │
│     breakdown = base.get('category_breakdown', {})          │
│     # No calculation, just extraction!                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  6. Python: Fill missing categories with 0%                 │
│     for cat in all_categories:                              │
│       if cat not in breakdown:                              │
│         breakdown[cat] = {'percentage': 0, ...}             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  7. Python: Apply priority logic for final classification   │
│     if unsafe > 0: primary = "unsafe"                       │
│     elif highly_sensitive > 5: primary = "highly_sensitive" │
│     # etc.                                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  8. UI: Display breakdown to user                           │
│     - Show percentages (from LLM)                           │
│     - Show page counts (from LLM)                           │
│     - Show reasons (from LLM)                               │
└─────────────────────────────────────────────────────────────┘
```

## Summary

**The actual implementation uses: LLM-Based Self-Analysis**

- ✅ GPT-4o calculates all percentages
- ✅ GPT-4o counts pages per category
- ✅ GPT-4o provides reasoning
- ✅ Python code just extracts and displays
- ✅ No manual page counting in Python
- ✅ No percentage calculations in Python

This is a **prompt engineering approach** where the intelligence is in the LLM, and the Python code is just orchestration and data handling.

The method is essentially: **"Ask the LLM to do it, trust the LLM's analysis, display the results."**

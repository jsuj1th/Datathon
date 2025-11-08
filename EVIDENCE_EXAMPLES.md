# Evidence Examples with Policy Mapping

## System Enhancement: Policy Explanations in Evidence

The system now provides **policy mapping** for each classification decision, explaining which rules apply and why.

---

## TC1: Public Marketing Document

### Evidence with Policy Explanation:

**Finding**: Document is a "Brochure" for Hitachi EverFlex Infrastructure as a Service Portfolio

**Location**: Pages 1-8, Title and throughout

**Policy Mapping in Reasoning**:
> "This directly aligns with the classification rules stating that 'Marketing materials, brochures, public website content, publicly available templates = public' and 'Marketing/promotional materials = public'"

**Why This Matters**: Clear reference to the specific classification rule that applies

---

## TC2: Employment Application with PII

### Evidence 1 with Policy Explanation:

**Finding**: Employment application containing:
- Full name: Susan J. Simmons
- Multiple addresses (street and mailing)
- Email, telephone, cell phone
- Employment history with employer details
- Virginia Driver's License
- Three personal references with contact info

**Location**: 
- Page 1, Items 3-12 (Personal info)
- Page 2, Item 20 (Employment history)
- Page 3, Items 24, 26, 28 (License and references)

**POLICY EXPLANATION**: 
> "Employment applications with personal information = highly_sensitive"

### Evidence 2 with Policy Explanation:

**Finding**: Full name + multiple contact details + references and employer contacts

**Location**: Page 1 Items 3-12, Page 2 Item 20, Page 3 Item 28

**POLICY EXPLANATION**:
> "Documents with names AND contact details = highly_sensitive"

### Reasoning with Policy Mapping:

> "This document is classified as 'highly_sensitive' because it is an employment application filled with a significant amount of personal information, directly matching the classification rule 'Employment applications with personal information = highly_sensitive'. Furthermore, the document contains the applicant's full name and multiple contact details (addresses, email, phone numbers), along with names and contact information for references and past employers, which aligns with the classification rule 'Documents with names AND contact details = highly_sensitive'."

**Why This Matters**: 
- References TWO specific classification rules
- Explains how each rule applies to the content
- Provides specific examples of the PII found

---

## TC3: Internal Memo

### Evidence with Policy Explanation:

**Finding**: "A Sample Research Proposal with Comments" - academic research document with internal processes

**Location**: Pages 1-3

**Policy Mapping in Reasoning**:
> "The document is a sample research proposal, which falls under the category of 'research' and 'non-public operational content' within an academic or institutional context... making it an internal academic document."

**Why This Matters**: Explains why research proposals are confidential (internal, non-public operational content)

---

## TC4: Flight Operations Manual

### Evidence with Policy Explanation:

**Finding**: "NBAA Light Business Airplane Flight Operations Manual Template" with technical procedures

**Location**: Pages 1-2

**POLICY EXPLANATION**:
> "The classification rules explicitly state: 'Technical manuals and flight operations procedures = confidential (even if templates)'"

### Reasoning with Policy Mapping:

> "The document is a template for a 'Flight Operations Manual', which falls under the classification rule for 'Technical manuals and flight operations procedures'. The rules explicitly state that such documents are 'confidential', even if they are templates. Although the document mentions it's available in PDF and Word formats and provides a public URL, the nature of its content (aviation procedures, safety management, operational guidance) overrides the 'publicly available templates without sensitive specs' rule due to the specific instruction for flight operations manuals."

**Why This Matters**:
- Directly quotes the classification rule
- Explains why this rule takes precedence over the "public template" exception
- Shows understanding of rule priority

---

## Key Improvements

### Before:
```json
{
  "finding": "Document contains PII",
  "location": "Page 1"
}
```

### After:
```json
{
  "finding": "Employment application containing full name (Susan J. Simmons), addresses, phone numbers, email, employment history, driver's license, and references. POLICY EXPLANATION: Employment applications with personal information = highly_sensitive",
  "locations": ["Page 1, Items 3-12", "Page 2, Item 20", "Page 3, Items 24, 26, 28"],
  "page_numbers": [1, 2, 3]
}
```

### What Changed:
1. ✅ **Specific content details** (not just "contains PII")
2. ✅ **Exact locations** (page AND item numbers)
3. ✅ **Policy explanation** (which rule applies)
4. ✅ **Reasoning section** references multiple rules and explains priority

---

## Policy Mapping Format

The system now provides policy explanations in two ways:

### 1. In Evidence Items:
Each piece of evidence includes "POLICY EXPLANATION:" followed by the specific rule that applies

### 2. In Reasoning Section:
The overall reasoning references classification rules and explains:
- Which rules apply
- Why they apply to this specific content
- How rules are prioritized when multiple apply
- Why certain exceptions don't apply

---

## Example: Complete Evidence Chain

**Document**: Employment Application

**Evidence Chain**:
1. **Finding**: Lists specific PII elements
2. **Location**: Exact page and field numbers
3. **Policy Rule**: "Employment applications with personal information = highly_sensitive"
4. **Reasoning**: Explains why this rule applies and references supporting rule about "names AND contact details"

**Result**: Clear, auditable classification with full policy traceability

---

## Benefits

### For Compliance:
- ✅ Audit trail shows which policies were applied
- ✅ Decisions are explainable and defensible
- ✅ Easy to verify correct policy application

### For Users:
- ✅ Understand why document was classified
- ✅ Learn which policies apply to their content
- ✅ Can challenge or confirm based on policy references

### For HITL:
- ✅ Reviewers can verify policy application
- ✅ Easier to identify misclassifications
- ✅ Feedback can reference specific policy rules

---

## Summary

The system now provides **complete policy traceability** for every classification decision:

1. **What was found**: Specific content details
2. **Where it was found**: Exact page/field locations
3. **Which policy applies**: Direct rule references
4. **Why it applies**: Explanation of policy logic
5. **How rules interact**: Priority and exception handling

This meets the requirement: "Cite the region with the serial; explain policy mapping for identifiable equipment and where and why content is unsafe."

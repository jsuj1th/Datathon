"""
Configurable prompt library for dynamic prompt tree generation
"""

class PromptLibrary:
    
    @staticmethod
    def get_base_classification_prompt():
        return """You are a document classification expert. Analyze the document type and content to classify it.

Categories:
1. highly_sensitive - Contains personal data like names+addresses, ID numbers, financial info, or proprietary designs
2. confidential - Internal business documents, research proposals, academic research, internal memos, non-public operational content, technical manuals with specifications, flight operations manuals, aviation procedures
3. public - Marketing materials, brochures, public website content, publicly available templates
4. unsafe - Violates child safety, hate speech, violent/criminal content

Classification Rules (PRIORITY ORDER):
- Employment applications with personal information = highly_sensitive
- Documents with names AND contact details = highly_sensitive  
- Research proposals (even if samples/templates) = confidential
- Academic research documents = confidential
- Internal memos/research = confidential
- Documents with "proposal", "research", "thesis" in title = confidential
- Technical manuals and flight operations procedures = confidential (even if templates)
- Aviation/aircraft technical specifications = confidential
- Marketing/promotional materials = public
- Publicly available templates without sensitive specs = public
- Unsafe content = unsafe (highest priority)

IMPORTANT: Research proposals, academic documents, and internal planning documents are ALWAYS confidential, even if they are samples or templates. The content is non-public operational/academic content.

IMPORTANT: Documents can contain MIXED CONTENT with multiple classification levels.

Analyze the ENTIRE document and identify ALL content types present:
- Public content (marketing, general info)
- Confidential content (internal docs, technical specs)
- Highly Sensitive content (PII, proprietary designs)
- Unsafe content (hate speech, violence, etc.)

Return JSON with these exact fields:
{
  "primary_category": "The dominant category based on most sensitive/prevalent content",
  "category_breakdown": {
    "highly_sensitive": {"percentage": 0-100, "page_count": X, "reason": "brief explanation"},
    "confidential": {"percentage": 0-100, "page_count": X, "reason": "brief explanation"},
    "public": {"percentage": 0-100, "page_count": X, "reason": "brief explanation"},
    "unsafe": {"percentage": 0-100, "page_count": X, "reason": "brief explanation"}
  },
  "overall_classification": "Primary category (use most restrictive if mixed)",
  "confidence": 0.95,
  "is_mixed_content": true/false,
  "evidence": [
    {
      "category": "which category this evidence supports",
      "finding": "Detailed description (3-4 sentences) with specific content details",
      "locations": ["Page X, Section Y, Line Z or Image Region"],
      "page_numbers": [X],
      "policy_explanation": "Which rule applies and WHY"
    }
  ],
  "reasoning": "Explain the mix of content types, their proportions, and why the primary category was chosen. If mixed, explain the weightage.",
  "safety_check": true/false,
  "page_citations": [1, 2, 3]
}

CLASSIFICATION LOGIC FOR MIXED CONTENT:
1. If ANY unsafe content exists (even 1%) → Primary = "unsafe"
2. If ANY highly sensitive content exists (>5%) → Primary = "highly_sensitive"
3. If confidential content is majority (>50%) → Primary = "confidential"
4. If public content is majority (>80%) and no sensitive content → Primary = "public"
5. Always use the MOST RESTRICTIVE category as primary for mixed documents
"""

    @staticmethod
    def get_pii_detection_prompt():
        return """Analyze this document specifically for Personally Identifiable Information (PII):

Look for:
- Social Security Numbers (SSN) - format XXX-XX-XXXX or variations
- Credit card numbers (16 digits)
- Bank account numbers
- Driver's license numbers
- Passport numbers
- Date of birth combined with name
- Email addresses (in sensitive contexts like applications)
- Phone numbers (in sensitive contexts like applications)
- Full names combined with addresses
- Medical record numbers
- Biometric data
- Employment history with personal details
- Emergency contact information
- References with contact details

CRITICAL: For employment applications, even if SSN field is blank or shows "XXX-XX-XXXX", the PRESENCE of an SSN field indicates this is a form designed to collect PII and should be flagged.

For each PII element found, provide:
- type: Type of PII
- location: Exact page number and section/field name
- context: Surrounding text/context (e.g., "Employment Application Section 2")
- severity: high (SSN, account numbers), medium (phone, email), low (generic address)
- is_filled: Boolean indicating if the field contains actual data or is just a form field
- pii_found: Boolean - true if ANY PII or PII collection fields exist

Return JSON with:
{
  "pii_found": true/false,
  "pii_elements": [
    {
      "type": "SSN/Driver License/etc",
      "location": "Page X, Field Y",
      "severity": "high/medium/low",
      "policy_mapping": "Contains PII - triggers Highly Sensitive classification per rule: 'Documents with names AND contact details = highly_sensitive'"
    }
  ],
  "locations": [list of page numbers],
  "highest_severity": "high/medium/low"
}
"""

    @staticmethod
    def get_safety_check_prompt():
        return """Perform a comprehensive safety check on this content:

Evaluate for:
1. Child safety violations
2. Hate speech or discriminatory content
3. Violent or graphic content
4. Criminal activity or instructions
5. Exploitative material
6. Cyber-threat or hacking instructions
7. Political misinformation or propaganda

Return:
{
  "is_safe": false,
  "violations": [
    {
      "type": "hate_speech/violent_content/etc",
      "location": "Page X, paragraph Y or Image region",
      "severity": "critical/high/medium/low",
      "policy_mapping": "Violates child safety policy - triggers Unsafe classification per rule: 'Unsafe content = unsafe (highest priority)'"
    }
  ],
  "severity": "critical/high/medium/low",
  "recommended_action": "flag/review/block"
}
"""

    @staticmethod
    def get_proprietary_detection_prompt():
        return """Analyze this document for proprietary or confidential business information:

Look for:
- Technical schematics or blueprints
- Product designs or prototypes
- Military or defense equipment
- Trade secrets or formulas
- Strategic business plans
- Financial projections (non-public)
- Source code or algorithms
- Patent-pending designs

For each finding:
{
  "type": "Type of proprietary content",
  "location": "Page X, Image region Y, or specific section",
  "sensitivity_level": "high/medium/low",
  "business_impact": "Description of potential impact if leaked",
  "policy_mapping": "Technical specifications/military equipment - triggers Confidential classification per rule: 'Technical manuals and flight operations procedures = confidential'"
}
"""

    @staticmethod
    def get_verification_prompt(initial_classification):
        return f"""You are a second-opinion classifier. Review this document independently.

The first classifier determined: {initial_classification}

Categories (use EXACTLY these names):
1. highly_sensitive - Contains personal data like names+addresses, ID numbers, financial info, or proprietary designs
2. confidential - Internal business documents, research proposals, academic research, internal memos, technical manuals
3. public - Marketing materials, brochures, public website content, publicly available templates
4. unsafe - Violates child safety, hate speech, violent/criminal content

Provide your own independent classification without bias. If you disagree, explain why.

Return JSON with these fields:
- category: highly_sensitive, confidential, public, or unsafe (use exact category name)
- confidence: 0.0 to 1.0
- agreement: true or false
- discrepancies: Explain any differences in your analysis
- final_recommendation: Your recommendation for handling this document
"""

    @staticmethod
    def build_dynamic_prompt_tree(document_metadata):
        """
        Build a dynamic prompt tree based on document characteristics
        """
        prompts = []
        
        # Always start with base classification
        prompts.append({
            'stage': 'base_classification',
            'prompt': PromptLibrary.get_base_classification_prompt(),
            'priority': 1
        })
        
        # Add safety check for all documents
        prompts.append({
            'stage': 'safety_check',
            'prompt': PromptLibrary.get_safety_check_prompt(),
            'priority': 1
        })
        
        # If document has text content, check for PII
        if document_metadata.get('has_text', False):
            prompts.append({
                'stage': 'pii_detection',
                'prompt': PromptLibrary.get_pii_detection_prompt(),
                'priority': 2
            })
        
        # If document has images, check for proprietary content
        if document_metadata.get('image_count', 0) > 0:
            prompts.append({
                'stage': 'proprietary_detection',
                'prompt': PromptLibrary.get_proprietary_detection_prompt(),
                'priority': 2
            })
        
        return sorted(prompts, key=lambda x: x['priority'])

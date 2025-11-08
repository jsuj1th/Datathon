import json
import base64
from openai import OpenAI
from config import Config
from prompt_library import PromptLibrary
from PIL import Image
import io

class DocumentClassifier:
    
    def __init__(self):
        if Config.OPENROUTER_API_KEY:
            # OpenRouter uses OpenAI-compatible API
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=Config.OPENROUTER_API_KEY,
            )
            # Use GPT-4o for multi-modal support
            self.model_name = "openai/gpt-4o"
        else:
            self.client = None
            self.model_name = None
    
    def classify_document(self, content, metadata, enable_dual_llm=None):
        """
        Main classification method using dynamic prompt tree
        
        Args:
            content: Document content (text, images)
            metadata: Document metadata
            enable_dual_llm: Override for dual-LLM setting (None = use config default)
        """
        # Use parameter if provided, otherwise fall back to config
        if enable_dual_llm is None:
            enable_dual_llm = Config.ENABLE_DUAL_LLM
        
        if not self.client:
            return {
                'error': 'OpenRouter API not configured',
                'category': 'unknown',
                'confidence': 0.0,
                'evidence': [],
                'reasoning': 'API key not configured',
                'safety_check': True,
                'page_count': metadata.get('page_count', 0),
                'image_count': metadata.get('image_count', 0),
                'stages': {}
            }
        
        # Build dynamic prompt tree based on document characteristics
        prompt_tree = PromptLibrary.build_dynamic_prompt_tree(metadata)
        
        results = {
            'category': None,
            'confidence': 0.0,
            'evidence': [],
            'reasoning': '',
            'safety_check': True,
            'page_count': metadata.get('page_count', 0),
            'image_count': metadata.get('image_count', 0),
            'stages': {}
        }
        
        # Execute each stage in the prompt tree
        for prompt_stage in prompt_tree:
            stage_name = prompt_stage['stage']
            stage_result = self._execute_stage(
                prompt_stage['prompt'],
                content,
                metadata
            )
            results['stages'][stage_name] = stage_result
        
        # Aggregate results from all stages
        final_classification = self._aggregate_results(results['stages'], metadata)
        results.update(final_classification)
        
        # Add dual-LLM flag
        results['dual_llm_enabled'] = enable_dual_llm
        
        # Dual-LLM verification if enabled
        if enable_dual_llm:
            print("  🔄 Running dual-LLM verification...")
            verification_result = self._verify_classification(
                results, 
                content, 
                metadata
            )
            results['verification'] = verification_result
            
            # Check for disagreement
            if verification_result.get('agreement') == False:
                results['requires_hitl'] = True
                results['hitl_reason'] = 'Dual-LLM disagreement detected'
                print(f"  ⚠️ Disagreement: Primary={results['category']}, Verification={verification_result.get('category')}")
            else:
                print(f"  ✓ Agreement: Both LLMs classified as {results['category']}")
        
        return results
    
    def _analyze_images(self, images):
        """Analyze images separately and return descriptions"""
        if not self.client or not images:
            return []
        
        image_descriptions = []
        
        for idx, img_data in enumerate(images[:5], 1):  # Analyze up to 5 images
            try:
                # Convert bytes to base64 for OpenAI API
                base64_image = base64.b64encode(img_data['data']).decode('utf-8')
                
                # Ask GPT-4o to describe the image
                prompt = """Analyze this image and describe:
1. What type of content is shown (diagram, photo, text, chart, etc.)
2. Any identifiable equipment, serial numbers, or technical specifications
3. Any text visible in the image
4. Whether it contains sensitive, proprietary, or confidential information
5. Any safety concerns (violence, hate symbols, etc.)

Be specific about locations and details. Keep response concise (2-3 sentences)."""
                
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=500,
                    temperature=0.3
                )
                
                description = response.choices[0].message.content
                image_descriptions.append({
                    'page': img_data.get('page', idx),
                    'description': description
                })
            except Exception as e:
                print(f"Warning: Could not analyze image {idx}: {e}")
        
        return image_descriptions
    
    def _execute_stage(self, prompt, content, metadata):
        """Execute a single classification stage using OpenRouter"""
        if not self.client:
            return {'error': 'OpenRouter API not configured'}
        
        try:
            # First, analyze images separately if present
            image_descriptions = []
            if content.get('images') and len(content['images']) > 0:
                print(f"  Analyzing {len(content['images'])} image(s)...")
                image_descriptions = self._analyze_images(content['images'])
                if image_descriptions:
                    print(f"  ✓ Generated descriptions for {len(image_descriptions)} image(s)")
            
            # Prepare the prompt with content (including image descriptions)
            full_prompt = f"{prompt}\n\n{self._prepare_content_for_llm(content, metadata, image_descriptions)}\n\nProvide your response in valid JSON format."
            
            # Call OpenRouter API (OpenAI-compatible)
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a document classification expert. Always respond with valid JSON."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.3,
                max_tokens=2048,
                response_format={"type": "json_object"}
            )
            
            # Parse JSON response
            response_text = response.choices[0].message.content
            
            # Try to extract JSON from response
            try:
                # Sometimes Gemini wraps JSON in markdown code blocks
                if '```json' in response_text:
                    json_start = response_text.find('```json') + 7
                    json_end = response_text.find('```', json_start)
                    response_text = response_text[json_start:json_end].strip()
                elif '```' in response_text:
                    json_start = response_text.find('```') + 3
                    json_end = response_text.find('```', json_start)
                    response_text = response_text[json_start:json_end].strip()
                
                # Try to fix common JSON issues
                # Remove trailing commas before closing braces/brackets
                import re
                response_text = re.sub(r',(\s*[}\]])', r'\1', response_text)
                
                result = json.loads(response_text)
                return result
            except json.JSONDecodeError as e:
                # Try to extract key information even if JSON parsing fails
                print(f"DEBUG: JSON parse error: {e}")
                print(f"DEBUG: Attempting to fix truncated JSON...")
                
                # Try to fix truncated strings and close the JSON
                try:
                    # Find the last complete field
                    lines = response_text.split('\n')
                    fixed_lines = []
                    for line in lines:
                        if line.strip() and not line.strip().endswith(('"', ',', '{', '[', '}', ']')):
                            # Truncated line - try to close it
                            if '"' in line and line.count('"') % 2 == 1:
                                line = line + '",'
                        fixed_lines.append(line)
                    
                    # Close any open structures
                    fixed_text = '\n'.join(fixed_lines)
                    open_braces = fixed_text.count('{') - fixed_text.count('}')
                    open_brackets = fixed_text.count('[') - fixed_text.count(']')
                    
                    for _ in range(open_brackets):
                        fixed_text += '\n]'
                    for _ in range(open_braces):
                        fixed_text += '\n}'
                    
                    result = json.loads(fixed_text)
                    print("DEBUG: Successfully fixed JSON!")
                    return result
                except:
                    pass
                
                # If JSON parsing fails, return a structured error
                return {
                    'error': 'Failed to parse JSON response',
                    'raw_response': response_text[:1000],
                    'parse_error': str(e)
                }
            
        except Exception as e:
            return {'error': str(e)}
    
    def _prepare_content_for_llm(self, content, metadata, image_descriptions=None):
        """Prepare content string for LLM"""
        parts = []
        
        parts.append(f"Document Metadata:")
        parts.append(f"- Type: {metadata.get('type', 'unknown')}")
        parts.append(f"- Pages: {metadata.get('page_count', 0)}")
        parts.append(f"- Images: {metadata.get('image_count', 0)}")
        parts.append(f"- Has Text: {metadata.get('has_text', False)}")
        parts.append("")
        
        if content.get('text'):
            parts.append("Text Content:")
            parts.append(content['text'][:10000])  # Limit text length
            parts.append("")
        
        if image_descriptions:
            parts.append(f"Image Analysis Results ({len(image_descriptions)} images analyzed):")
            for img_desc in image_descriptions:
                parts.append(f"\nPage {img_desc['page']}:")
                parts.append(f"  {img_desc['description']}")
            parts.append("")
        elif content.get('images'):
            parts.append(f"Document contains {len(content['images'])} image(s).")
        
        return '\n'.join(parts)
    


    
    def _aggregate_results(self, stages, metadata):
        """Aggregate results from all classification stages"""
        aggregated = {
            'category': 'public',
            'confidence': 0.0,
            'evidence': [],
            'reasoning': '',
            'safety_check': True,
            'is_mixed_content': False,
            'category_breakdown': {}
        }
        
        # Priority order for categories
        category_priority = {
            'unsafe': 4,
            'highly_sensitive': 3,
            'confidential': 2,
            'public': 1
        }
        
        highest_priority = 0
        
        # Process base classification
        if 'base_classification' in stages:
            base = stages['base_classification']
            
            # Handle new mixed-content format
            if 'primary_category' in base or 'overall_classification' in base:
                # New format with category breakdown
                category = base.get('overall_classification', base.get('primary_category', 'public')).lower().replace(' ', '_')
                aggregated['category'] = category
                aggregated['confidence'] = base.get('confidence', 0.0)
                aggregated['reasoning'] = base.get('reasoning', '')
                aggregated['is_mixed_content'] = base.get('is_mixed_content', False)
                aggregated['category_breakdown'] = base.get('category_breakdown', {})
                highest_priority = category_priority.get(category, 0)
                
                # Ensure category_breakdown has all categories (fill in missing ones with 0%)
                all_categories = ['public', 'confidential', 'highly_sensitive', 'unsafe']
                for cat in all_categories:
                    if cat not in aggregated['category_breakdown']:
                        aggregated['category_breakdown'][cat] = {
                            'percentage': 0,
                            'page_count': 0,
                            'reason': ''
                        }
            else:
                # Old format (backward compatible) - create breakdown for single category
                category = base.get('category', 'public').lower().replace(' ', '_')
                aggregated['category'] = category
                aggregated['confidence'] = base.get('confidence', 0.0)
                aggregated['reasoning'] = base.get('reasoning', '')
                highest_priority = category_priority.get(category, 0)
                
                # Create a simple breakdown showing 100% of the detected category
                aggregated['category_breakdown'] = {
                    'public': {'percentage': 0, 'page_count': 0, 'reason': ''},
                    'confidential': {'percentage': 0, 'page_count': 0, 'reason': ''},
                    'highly_sensitive': {'percentage': 0, 'page_count': 0, 'reason': ''},
                    'unsafe': {'percentage': 0, 'page_count': 0, 'reason': ''}
                }
                aggregated['category_breakdown'][category] = {
                    'percentage': 100,
                    'page_count': metadata.get('page_count', 0),
                    'reason': f'Entire document classified as {category.replace("_", " ")}'
                }
            
            if base.get('evidence'):
                aggregated['evidence'].extend(base['evidence'])
        
        # Process safety check
        if 'safety_check' in stages:
            safety = stages['safety_check']
            aggregated['safety_check'] = safety.get('is_safe', True)
            
            if not safety.get('is_safe', True):
                aggregated['category'] = 'unsafe'
                highest_priority = 4
                aggregated['evidence'].append({
                    'type': 'safety_violation',
                    'details': safety.get('violations', []),
                    'severity': safety.get('severity', 'high')
                })
        
        # Process PII detection
        if 'pii_detection' in stages:
            pii = stages['pii_detection']
            if pii.get('pii_found'):
                # PII means highly sensitive
                if category_priority.get('highly_sensitive', 0) > highest_priority:
                    aggregated['category'] = 'highly_sensitive'
                    highest_priority = 3
                
                aggregated['evidence'].append({
                    'type': 'pii_detected',
                    'details': pii.get('pii_elements', []),
                    'locations': pii.get('locations', [])
                })
        
        # Process proprietary detection
        if 'proprietary_detection' in stages:
            prop = stages['proprietary_detection']
            if prop.get('proprietary_found'):
                # Proprietary content is at least confidential
                if category_priority.get('confidential', 0) > highest_priority:
                    aggregated['category'] = 'confidential'
                
                aggregated['evidence'].append({
                    'type': 'proprietary_content',
                    'details': prop.get('findings', []),
                    'sensitivity': prop.get('sensitivity_level', 'medium')
                })
        
        return aggregated

    def _verify_classification(self, primary_result, content, metadata):
        """
        Second-opinion classification using a different model or independent prompt
        """
        if not self.client:
            return {'error': 'OpenRouter API not configured'}
        
        try:
            # Get verification prompt with primary classification
            verification_prompt = PromptLibrary.get_verification_prompt(
                primary_result.get('category', 'unknown')
            )
            
            # Prepare content (reuse existing method but without images to save cost)
            full_prompt = f"{verification_prompt}\n\n{self._prepare_content_for_llm(content, metadata, image_descriptions=None)}\n\nProvide your response in valid JSON format."
            
            # Use verification model (can be different/cheaper model)
            verification_model = Config.VERIFICATION_MODEL if hasattr(Config, 'VERIFICATION_MODEL') else self.model_name
            
            # Call verification LLM
            response = self.client.chat.completions.create(
                model=verification_model,
                messages=[
                    {"role": "system", "content": "You are an independent document classification expert providing a second opinion. Always respond with valid JSON."},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.3,
                max_tokens=1024,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            response_text = response.choices[0].message.content
            
            # Clean JSON if needed
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                response_text = response_text[json_start:json_end].strip()
            elif '```' in response_text:
                json_start = response_text.find('```') + 3
                json_end = response_text.find('```', json_start)
                response_text = response_text[json_start:json_end].strip()
            
            import re
            response_text = re.sub(r',(\s*[}\]])', r'\1', response_text)
            
            result = json.loads(response_text)
            
            # Normalize category names for comparison
            primary_category = primary_result.get('category', '').lower().replace(' ', '_')
            verification_category = result.get('category', '').lower().replace(' ', '_')
            
            # Check agreement
            result['agreement'] = (primary_category == verification_category)
            result['primary_category'] = primary_category
            result['verification_category'] = verification_category
            
            return result
            
        except Exception as e:
            return {
                'error': str(e),
                'agreement': True,  # Default to agreement on error to avoid false flags
                'note': 'Verification failed, defaulting to primary classification'
            }

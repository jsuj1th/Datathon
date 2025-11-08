# Dual-LLM Verification Guide

## Overview

Dual-LLM verification adds a second layer of AI validation to improve classification accuracy and reliability. When enabled, the system uses two different LLMs to independently classify each document and flags any disagreements for human review.

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                    Document Input                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Primary Classification (GPT-4o)                 │
│  • Full multi-stage analysis                                │
│  • Image analysis                                           │
│  • PII detection                                            │
│  • Safety check                                             │
│  • Evidence generation                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│         Verification Classification (GPT-4o-mini)            │
│  • Independent second opinion                               │
│  • Text-only analysis (faster)                              │
│  • Same classification rules                                │
│  • Discrepancy detection                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  Agreement Check                             │
│                                                              │
│  ✅ AGREEMENT          ⚠️ DISAGREEMENT                       │
│  → Auto-classify       → Flag for HITL                       │
│  → High confidence     → Requires review                     │
│  → No review needed    → Show both opinions                  │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

### Enable Dual-LLM

Edit your `.env` file:

```bash
# Enable dual-LLM verification
ENABLE_DUAL_LLM=true

# Verification model (optional - defaults to gpt-4o-mini)
VERIFICATION_MODEL=openai/gpt-4o-mini
```

### Model Options

**Primary Model**: `openai/gpt-4o`
- Full-featured analysis
- Multi-modal (text + images)
- Higher accuracy
- More expensive

**Verification Model Options**:
1. `openai/gpt-4o-mini` (Recommended)
   - Fast and cost-effective
   - Good accuracy
   - ~70% cheaper than GPT-4o
   
2. `openai/gpt-4o` (Maximum accuracy)
   - Same model as primary
   - Highest reliability
   - 2x cost

3. `anthropic/claude-3-sonnet` (Alternative provider)
   - Different AI architecture
   - Reduces model bias
   - Similar cost to GPT-4o-mini

## Benefits

### 1. Higher Accuracy
- Two independent opinions reduce errors
- Cross-validation catches edge cases
- Reduces both false positives and false negatives

### 2. Automatic Quality Control
- Disagreements automatically flagged
- No manual review needed for agreements
- Built-in confidence scoring

### 3. Audit Trail
- Two independent classifications recorded
- Discrepancy explanations provided
- Clear reasoning from both models

### 4. Reduced Human Review
- Only review disagreements (~5-10% of cases)
- High-confidence agreements auto-approved
- Focus human expertise where needed

## Trade-offs

### Performance Impact
- **Processing Time**: ~2x slower (two LLM calls)
- **Cost**: ~1.5x more expensive (verification uses cheaper model)
- **API Calls**: 2x API requests

### When to Enable

✅ **Enable When**:
- High accuracy is critical
- Dealing with sensitive documents
- Compliance requirements are strict
- Cost is not a primary concern
- Processing time is acceptable

❌ **Disable When**:
- Processing speed is critical
- Cost optimization is priority
- Documents are low-risk
- High volume batch processing
- Single-LLM accuracy is sufficient

## Testing

### Test Dual-LLM Feature

```bash
# Run the test script
python test_dual_llm.py
```

This will:
1. Show current configuration
2. Process a test document (TC2)
3. Display both LLM opinions
4. Show agreement/disagreement status
5. Explain HITL flagging logic

### Expected Results

**Agreement Example**:
```
🔄 DUAL-LLM VERIFICATION RESULTS:
   Primary LLM:      HIGHLY_SENSITIVE
   Verification LLM: HIGHLY_SENSITIVE
   
   ✅ AGREEMENT - Both LLMs classified identically
   → Classification is highly reliable
   → No human review needed
```

**Disagreement Example**:
```
🔄 DUAL-LLM VERIFICATION RESULTS:
   Primary LLM:      CONFIDENTIAL
   Verification LLM: HIGHLY_SENSITIVE
   
   ⚠️ DISAGREEMENT DETECTED
   → Flagged for human review
   → Requires expert validation
   
   Discrepancies:
   The verification model detected PII that the primary 
   model may have missed, warranting a higher classification.
```

## Integration with UI

### Streamlit UI (demo_ui.py)

When dual-LLM is enabled, the UI automatically shows:
- Verification status badge
- Agreement/disagreement indicator
- Both LLM classifications (if different)
- Discrepancy explanations
- HITL flag status

### Batch Processing (batch_processor.py)

Dual-LLM works seamlessly with batch processing:
- Each document gets dual verification
- Disagreements tracked in results
- HITL queue populated automatically
- Processing time scales linearly

## Metrics & Monitoring

### Agreement Rate
Track how often the two LLMs agree:
```python
from metrics_tracker import MetricsTracker

tracker = MetricsTracker()
report = tracker.generate_report()

# Check dual-LLM statistics
if 'dual_llm_stats' in report:
    print(f"Agreement Rate: {report['dual_llm_stats']['agreement_rate']:.1%}")
```

### Cost Analysis
Monitor the cost impact:
- Primary model: ~$0.005 per 1K tokens
- Verification model: ~$0.0015 per 1K tokens
- Total increase: ~50% more cost

### Performance Metrics
- Average processing time with dual-LLM: ~15-20 seconds
- Average processing time without: ~8-10 seconds
- Disagreement rate: Typically 5-10%

## Best Practices

### 1. Start with Dual-LLM Disabled
- Test with single LLM first
- Measure baseline accuracy
- Enable dual-LLM for comparison

### 2. Monitor Disagreement Patterns
- Track which document types cause disagreements
- Refine prompts based on patterns
- Update classification rules

### 3. Use for High-Stakes Documents
- Enable for sensitive classifications
- Disable for routine/low-risk documents
- Toggle based on document type

### 4. Review Disagreements
- Use HITL feedback to improve prompts
- Document resolution decisions
- Update training data

## Troubleshooting

### Verification Always Fails
**Problem**: Verification returns errors
**Solution**: Check API key and model availability

### High Disagreement Rate (>20%)
**Problem**: Models disagree too often
**Solution**: 
- Review prompt clarity
- Check if categories are well-defined
- Consider using same model for both

### Slow Performance
**Problem**: Processing takes too long
**Solution**:
- Use faster verification model (gpt-4o-mini)
- Disable image analysis for verification
- Process in batches during off-hours

## API Reference

### Configuration
```python
from config import Config

# Check if enabled
if Config.ENABLE_DUAL_LLM:
    print("Dual-LLM is enabled")

# Get verification model
model = Config.VERIFICATION_MODEL
```

### Classification Result
```python
classification = classifier.classify_document(content, metadata)

# Check dual-LLM status
if classification['dual_llm_enabled']:
    verification = classification['verification']
    
    if verification['agreement']:
        print("LLMs agree")
    else:
        print(f"Disagreement: {verification['discrepancies']}")
```

### HITL Integration
```python
from hitl_manager import HITLManager

hitl = HITLManager()

# Check if needs review
needs_review, reason = hitl.should_flag_for_review(classification)

if needs_review:
    print(f"Flagged: {reason}")
```

## FAQ

**Q: Does dual-LLM work with all document types?**
A: Yes, it works with PDFs, images, and text documents.

**Q: Can I use different models for verification?**
A: Yes, set VERIFICATION_MODEL in .env to any OpenRouter-supported model.

**Q: What happens if verification fails?**
A: The system defaults to the primary classification and logs the error.

**Q: Does it work with batch processing?**
A: Yes, dual-LLM works seamlessly with batch_processor.py.

**Q: How much does it cost?**
A: Approximately 50% more than single-LLM (using gpt-4o-mini for verification).

**Q: Can I disable it for specific documents?**
A: Currently it's a global setting. You can toggle it in .env between runs.

---

## Summary

Dual-LLM verification provides an extra layer of confidence in your document classifications. While it adds some cost and processing time, the improved accuracy and automatic quality control make it valuable for high-stakes applications.

**Quick Start**:
1. Set `ENABLE_DUAL_LLM=true` in .env
2. Run `python test_dual_llm.py`
3. Check results in UI or batch processor
4. Monitor agreement rates and adjust as needed

# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install system dependencies (macOS)
brew install poppler tesseract

# Or on Ubuntu/Debian
sudo apt-get install poppler-utils tesseract-ocr
```

### Step 2: Configure API Keys

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Run Test Cases

Test the system with the provided test documents:

```bash
python run_test_cases.py
```

This will:
- Process all 5 test case documents
- Show detailed classification results
- Display evidence citations
- Generate a test report

### Step 4: Start the Web Application

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

---

## 📋 Test Cases Overview

| Test Case | Document Type | Expected Category | Key Features |
|-----------|--------------|-------------------|--------------|
| TC1 | Marketing Brochure | Public | 8 pages, Hitachi product info |
| TC2 | Employment Application | Highly Sensitive | PII fields (SSN, address, phone) |
| TC3 | Research Memo | Confidential | Internal project documentation |
| TC4 | Flight Manual | Confidential | 18 pages, technical specifications |
| TC5 | Mixed Content | Unsafe | Multiple violation types |

---

## 🎯 Using the Web Interface

### Interactive Mode

1. Click "Interactive Mode" tab
2. Drag and drop a document or click to upload
3. Click "Classify Document"
4. Review results with evidence citations
5. Provide feedback if needed

### Batch Processing

1. Click "Batch Processing" tab
2. Select multiple documents
3. Click "Process Batch"
4. Monitor real-time progress
5. Review aggregated results

### Statistics Dashboard

1. Click "Statistics" tab
2. View HITL feedback metrics
3. See agreement rates
4. Track system performance

---

## 📊 Understanding Results

### Classification Categories

- **Public**: Marketing materials, public-facing content
- **Confidential**: Internal documents, business communications
- **Highly Sensitive**: PII, proprietary designs, defense materials
- **Unsafe**: Child safety violations, hate speech, violent content

### Confidence Scores

- **80-100%**: High confidence (green badge)
- **60-79%**: Medium confidence (yellow badge)
- **0-59%**: Low confidence (red badge) - flagged for human review

### Evidence Citations

Each classification includes:
- Specific page numbers
- Location references
- Type of evidence found
- Context and details

---

## 🔄 HITL Feedback Loop

### When to Provide Feedback

The system automatically flags documents for human review when:
- Confidence score < 70%
- Dual-LLM disagreement (if enabled)
- Unsafe content detected
- Multiple sensitive elements found

### How to Submit Feedback

1. Review the classification result
2. Select correct category if different
3. Add notes explaining the correction
4. Click "Submit Feedback"

Your feedback helps improve the system over time!

---

## 🛠️ Troubleshooting

### "OpenAI API key not configured"

**Solution**: Make sure `.env` file exists with valid `OPENAI_API_KEY`

### "Pre-processing failed"

**Possible causes**:
- File format not supported (use PDF, PNG, JPG)
- File corrupted or unreadable
- File size exceeds 50MB limit

**Solution**: Check file format and size

### "Classification timeout"

**Possible causes**:
- Large document (many pages)
- API rate limits
- Network issues

**Solution**: 
- Try batch processing for multiple files
- Check your OpenAI API quota
- Retry after a few moments

### OCR not working

**Solution**: Install tesseract
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr
```

---

## 📈 Expected Performance

### Response Times

- **Single document**: 5-15 seconds
- **Batch processing**: 10-20 seconds per document
- **Pre-processing**: < 2 seconds

### Accuracy Targets

- **Overall accuracy**: > 90%
- **PII detection**: > 95%
- **Safety violations**: > 98%
- **False positives**: < 5%

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** to version control
2. **Rotate API keys** regularly
3. **Clean up uploads** folder periodically
4. **Review HITL feedback** for sensitive data
5. **Use HTTPS** in production

---

## 📚 Next Steps

### For Development

- Review `IMPLEMENTATION_GUIDE.md` for detailed architecture
- Check `PROJECT_STRUCTURE.md` for code organization
- Read `TEST_CASES.md` for evaluation criteria

### For Production

- Follow `DEPLOYMENT.md` for production setup
- Configure monitoring and logging
- Set up automated backups
- Implement authentication

### For Customization

- Modify `prompt_library.py` for custom prompts
- Update `config.py` for new categories
- Adjust `hitl_manager.py` for review thresholds

---

## 💡 Tips

1. **Start with test cases** to verify setup
2. **Use batch mode** for multiple documents
3. **Review evidence citations** for accuracy
4. **Provide feedback** to improve the system
5. **Monitor statistics** to track performance

---

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review error messages in the console
3. Run `python test_system.py` to diagnose
4. Check API key configuration
5. Verify all dependencies are installed

---

## ✅ Checklist

Before running the system, ensure:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] System dependencies installed (poppler, tesseract)
- [ ] `.env` file created with API key
- [ ] Test documents in `test_documents/` folder
- [ ] `uploads/` folder exists (created automatically)

Ready to go? Run:

```bash
python run_test_cases.py
```

Then start the web app:

```bash
python app.py
```

🎉 **You're all set!**

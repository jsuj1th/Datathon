# User Guide - AI Document Classification System

## 🚀 Getting Started

Access the application at: **http://localhost:8501**

## 📤 How to Upload and Classify Documents

### Option 1: Upload Your Own PDF

1. **Select Upload Mode**
   - In the sidebar, choose "📤 Upload Your Own PDF"

2. **Upload File**
   - Click "Browse files" or drag & drop your PDF
   - File will be automatically saved to `test_documents/` folder
   - You'll see a confirmation with the saved filename

3. **Classify**
   - Click "🔍 Classify Document" button
   - Wait 10-20 seconds for analysis

4. **View Results**
   - Primary classification category
   - Confidence score
   - Mixed content breakdown (if applicable)
   - Detailed evidence with page citations
   - Policy explanations

### Option 2: Use Test Cases

1. **Select Test Case Mode**
   - In the sidebar, choose "📋 Use Test Cases"

2. **Choose Test Case**
   - Select from TC1-TC5 dropdown
   - Each demonstrates different classification scenarios

3. **Classify**
   - Click "🔍 Classify Document"
   - View results

## 📊 Understanding Results

### Primary Classification

Your document will be classified as:
- **🔴 Highly Sensitive**: Contains PII, proprietary designs
- **🟠 Confidential**: Internal docs, technical specs
- **🟢 Public**: Marketing materials, public content
- **⚠️ Unsafe**: Violates safety policies

### Mixed Content

If your document contains multiple types:
- **Warning banner** appears
- **Breakdown chart** shows percentages
- **Primary category** uses most restrictive classification

Example:
```
⚠️ Mixed Content Detected

Public: 40% (4 pages) - Marketing materials
Confidential: 60% (6 pages) - Technical specifications

Primary Classification: CONFIDENTIAL
```

### Evidence

For each classification, you'll see:
- **Finding**: What was detected (3-4 sentences)
- **Location**: Exact pages, sections, fields
- **Policy Mapping**: Which rule applies and why

### Performance Metrics

After classifying documents:
- **Processing Time**: How long it took
- **Accuracy**: If using test cases
- **Review Needed**: Whether HITL review is required

## 🗂️ Managing Uploaded Files

### View Uploaded Files
- Sidebar shows count of uploaded files
- Files are stored in `test_documents/` folder
- Filenames include timestamp: `uploaded_20251108_123456_document.pdf`

### Clear Uploads
- Click "🗑️ Clear All Uploads" in sidebar
- Removes all uploaded files
- Test case files are preserved

## 📈 Viewing Metrics

### Session Metrics (Sidebar)
- **Tests Run**: Number of documents classified
- **Accuracy**: Overall classification accuracy
- **Avg Confidence**: Average confidence score
- **Avg Time**: Average processing time

### Full Metrics Report
1. Click "📈 View Full Metrics Report"
2. See comprehensive metrics:
   - Model information
   - Precision & Recall by category
   - Throughput statistics
   - HITL review metrics
   - Safety validation results

## 🎯 Use Cases

### 1. Classify Business Documents
- Upload contracts, reports, memos
- Get instant classification
- See which sections are sensitive

### 2. Compliance Checking
- Upload documents for review
- Identify PII or confidential content
- Get audit trail with citations

### 3. Content Moderation
- Check for unsafe content
- Validate child safety
- Flag policy violations

### 4. Document Triage
- Batch classify documents
- Route to appropriate teams
- Prioritize sensitive content

## 🔐 What Gets Classified

### Highly Sensitive
- Social Security Numbers
- Credit card numbers
- Driver's licenses
- Medical records
- Proprietary designs
- Defense schematics

### Confidential
- Internal memos
- Research proposals
- Technical manuals
- Business strategies
- Customer lists
- Financial projections

### Public
- Marketing brochures
- Product catalogs
- Press releases
- Public announcements
- Website content

### Unsafe
- Hate speech
- Violent content
- Child safety violations
- Criminal instructions
- Exploitative material

## ⚡ Tips for Best Results

### 1. File Quality
- Use clear, legible PDFs
- Avoid heavily encrypted files
- Ensure text is extractable

### 2. File Size
- Keep under 50MB
- Large files take longer to process
- Consider splitting very large documents

### 3. Mixed Content
- System automatically detects mixed content
- Primary category is most restrictive
- Review breakdown for details

### 4. Review Flagging
- Low confidence (<70%) flagged for review
- Unsafe content always flagged
- Multiple sensitive elements flagged

## 🛠️ Troubleshooting

### Upload Not Working
- Check file is PDF format
- Ensure file size < 50MB
- Try renaming file (remove special characters)

### Classification Taking Long
- Large files take 20-30 seconds
- Multiple images increase processing time
- Check internet connection (API calls)

### Unexpected Classification
- Review evidence and policy explanations
- Check mixed content breakdown
- Consider providing feedback

### Can't See Uploaded Files
- Check `test_documents/` folder
- Files prefixed with `uploaded_`
- Use "Clear All Uploads" to reset

## 📞 Support

For issues or questions:
1. Check this guide
2. Review `MIXED_CONTENT_GUIDE.md` for mixed content
3. See `TC5_EXPLANATION.md` for test case details
4. Check `ARCHITECTURE.md` for technical details

## 🎉 Quick Start Example

1. Go to http://localhost:8501
2. Select "📤 Upload Your Own PDF"
3. Upload any PDF document
4. Click "🔍 Classify Document"
5. View results with evidence and policy explanations
6. Check if mixed content detected
7. Review metrics in sidebar

That's it! The system handles the rest automatically.

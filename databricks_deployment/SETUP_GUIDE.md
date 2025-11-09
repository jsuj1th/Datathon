# Complete Databricks Setup Guide - Step by Step

## Prerequisites

Before you start, you need:
- [ ] A Databricks account (free trial available)
- [ ] Your OpenRouter API key
- [ ] Python installed on your computer
- [ ] Terminal/Command Prompt access

---

## Part 1: Get a Databricks Workspace (15 minutes)

### Option A: Free Trial (Recommended for Testing)

1. **Go to Databricks Website**
   - Visit: https://databricks.com/try-databricks
   - Click "Start Free Trial"

2. **Choose Cloud Provider**
   - Select: **AWS**, **Azure**, or **GCP**
   - For beginners: Choose **AWS** (easiest)

3. **Sign Up**
   - Enter your email
   - Create password
   - Verify email

4. **Create Workspace**
   - Follow the setup wizard
   - Choose region (pick one close to you)
   - Wait 5-10 minutes for workspace creation

5. **Save Your Workspace URL**
   - It will look like: `https://dbc-12345678-abcd.cloud.databricks.com`
   - **Write this down!** You'll need it later

### Option B: Use Existing Databricks Account

If you already have access:
1. Log in to your Databricks workspace
2. Note your workspace URL
3. Skip to Part 2

---

## Part 2: Get Databricks Access Token (5 minutes)

1. **Log in to Databricks**
   - Go to your workspace URL
   - Sign in

2. **Generate Access Token**
   - Click your **username** (top right corner)
   - Select **User Settings**
   - Click **Developer** tab (or **Access Tokens**)
   - Click **Generate New Token**

3. **Configure Token**
   - Comment: `Document Classifier CLI`
   - Lifetime: `90 days` (or as needed)
   - Click **Generate**

4. **Copy and Save Token**
   - **IMPORTANT**: Copy the token immediately
   - Save it somewhere safe (you can't see it again!)
   - It looks like: `dapi1234567890abcdef...`

---

## Part 3: Install Databricks CLI (5 minutes)

Open your terminal/command prompt:

### On Mac/Linux:

```bash
# Install Databricks CLI
pip install databricks-cli

# Verify installation
databricks --version
```

### On Windows:

```bash
# Install Databricks CLI
pip install databricks-cli

# Verify installation
databricks --version
```

### If pip is not found:

```bash
# Install pip first
python -m ensurepip --upgrade

# Then install Databricks CLI
python -m pip install databricks-cli
```

---

## Part 4: Configure Databricks CLI (2 minutes)

```bash
# Run configuration
databricks configure --token
```

You'll be prompted for:

**1. Databricks Host:**
```
Enter: https://dbc-12345678-abcd.cloud.databricks.com
(Use YOUR workspace URL from Part 1)
```

**2. Token:**
```
Enter: dapi1234567890abcdef...
(Paste YOUR token from Part 2)
```

**Test Configuration:**
```bash
# This should list your workspace
databricks workspace ls /
```

If you see output, you're configured! ✅

---

## Part 5: Upload Files to Databricks (5 minutes)

### Navigate to Project Directory

```bash
# Go to your project folder
cd /path/to/new_hitachi

# Go to databricks deployment folder
cd databricks_deployment
```

### Run Upload Script

```bash
# Make script executable (Mac/Linux only)
chmod +x upload_to_databricks.sh

# Run upload script
./upload_to_databricks.sh
```

**On Windows:**
```bash
# Run with bash
bash upload_to_databricks.sh
```

**What this does:**
- Creates folders in Databricks
- Uploads all Python files
- Uploads test documents
- Uploads job scripts

You should see:
```
✓ Directories created
✓ Python files uploaded
✓ Test documents uploaded
✓ Databricks scripts uploaded
Upload Complete!
```

---

## Part 6: Set Up Secrets (3 minutes)

### Create Secrets Scope

```bash
# Create scope for storing secrets
databricks secrets create-scope --scope document-classifier
```

### Add Your OpenRouter API Key

```bash
# Add API key as secret
databricks secrets put --scope document-classifier --key openrouter-api-key
```

This will open a text editor. Paste your OpenRouter API key and save.

**On Mac/Linux:**
- Paste key
- Press `Ctrl+X`, then `Y`, then `Enter`

**On Windows:**
- Paste key
- Press `Ctrl+X`, then `Y`, then `Enter`

### Verify Secret

```bash
# List secrets (won't show values, just names)
databricks secrets list --scope document-classifier
```

You should see:
```
Key name: openrouter-api-key
```

---

## Part 7: Import Notebooks (5 minutes)

### Option A: Via Databricks UI (Easier)

1. **Go to Databricks Workspace**
   - Open your workspace URL in browser
   - Log in

2. **Navigate to Workspace**
   - Click **Workspace** in left sidebar
   - Click **Users**
   - Click your email/username

3. **Import Interactive Notebook**
   - Click the **⋮** (three dots) next to your name
   - Select **Import**
   - Click **File**
   - Browse to: `databricks_deployment/databricks_interactive_notebook.py`
   - Click **Import**

4. **Import Batch Job Notebook**
   - Repeat above steps
   - Import: `databricks_deployment/databricks_batch_job.py`

### Option B: Via CLI

```bash
# Import interactive notebook
databricks workspace import databricks_interactive_notebook.py \
  /Users/your-email@example.com/databricks_interactive_notebook \
  --language PYTHON --format SOURCE

# Import batch job notebook
databricks workspace import databricks_batch_job.py \
  /Users/your-email@example.com/databricks_batch_job \
  --language PYTHON --format SOURCE
```

---

## Part 8: Create a Cluster (5 minutes)

1. **Go to Compute**
   - Click **Compute** in left sidebar
   - Click **Create Cluster**

2. **Configure Cluster**
   - **Cluster name**: `document-classifier-cluster`
   - **Cluster mode**: `Single Node` (for testing)
   - **Databricks runtime**: `13.3 LTS` or later
   - **Node type**: `Standard_DS3_v2` (or smallest available)
   - **Terminate after**: `30 minutes` of inactivity

3. **Advanced Options** (expand)
   - **Spark Config**: Leave default
   - **Environment Variables**: Leave default

4. **Create Cluster**
   - Click **Create Cluster**
   - Wait 3-5 minutes for cluster to start

---

## Part 9: Test the System (10 minutes)

### Test 1: Interactive Notebook

1. **Open Interactive Notebook**
   - Go to **Workspace** → **Users** → **Your Name**
   - Click `databricks_interactive_notebook`

2. **Attach Cluster**
   - Click **Connect** dropdown (top)
   - Select your cluster

3. **Run Cells**
   - Click **Run All** (or run cells one by one)
   - Watch for output

4. **Verify Success**
   - You should see: `✓ Modules imported successfully`
   - Then: `✓ API key loaded from secrets`
   - Finally: Classification results

### Test 2: Upload a Document

1. **Go to Data**
   - Click **Data** in left sidebar
   - Click **DBFS**

2. **Navigate to Input Folder**
   - Browse to: `/FileStore/documents/input/`

3. **Upload a PDF**
   - Click **Upload**
   - Select a PDF file
   - Click **Upload**

4. **Run Classification**
   - Go back to interactive notebook
   - Update document path in Cell 6
   - Run the cell
   - View results

---

## Part 10: Create Batch Job (Optional - 10 minutes)

1. **Go to Workflows**
   - Click **Workflows** in left sidebar
   - Click **Create Job**

2. **Configure Job**
   - **Name**: `Document Classification Batch`
   - **Task name**: `classify_documents`
   - **Type**: `Notebook`
   - **Notebook path**: `/Users/your-email/databricks_batch_job`
   - **Cluster**: Select your cluster

3. **Add Parameters**
   - Click **Add** under Parameters
   - Add:
     - `input_path`: `/FileStore/documents/input/`
     - `output_path`: `/FileStore/documents/output/`
     - `enable_dual_llm`: `false`

4. **Save and Run**
   - Click **Create**
   - Click **Run Now**
   - Monitor progress

---

## Verification Checklist

After setup, verify everything works:

- [ ] Databricks CLI installed and configured
- [ ] Files uploaded to DBFS
- [ ] Secrets configured
- [ ] Notebooks imported
- [ ] Cluster created and running
- [ ] Interactive notebook runs successfully
- [ ] Can classify a test document
- [ ] Batch job created (optional)

---

## Troubleshooting

### "databricks: command not found"

```bash
# Install Databricks CLI
pip install databricks-cli

# Or with python -m
python -m pip install databricks-cli
```

### "Authentication failed"

```bash
# Reconfigure with correct credentials
databricks configure --token

# Make sure to use:
# - Correct workspace URL (with https://)
# - Valid access token
```

### "Module not found" in notebook

```python
# Add this at the top of your notebook
import sys
sys.path.append('/dbfs/FileStore/document_classifier/')
```

### "API key not configured"

```bash
# Verify secret exists
databricks secrets list --scope document-classifier

# If not, add it again
databricks secrets put --scope document-classifier --key openrouter-api-key
```

### "File not found" errors

```bash
# Re-run upload script
cd databricks_deployment
./upload_to_databricks.sh
```

### Cluster won't start

- Check if you have quota/credits
- Try smaller instance type
- Check Databricks status page

---

## Cost Considerations

### Free Trial
- Usually includes $200-400 credits
- Enough for testing and development
- Lasts 14-30 days

### After Trial
- **Compute**: ~$0.15-0.40 per DBU-hour
- **Storage**: ~$0.023 per GB-month
- **API Calls**: OpenRouter charges separately

### Cost Optimization
1. Use **Single Node** clusters for testing
2. Set **auto-termination** to 30 minutes
3. Use **Spot instances** for batch jobs
4. Disable **Dual-LLM** unless needed
5. Delete unused clusters

---

## Next Steps

After successful setup:

1. **Test with Your Documents**
   - Upload your PDFs to `/FileStore/documents/input/`
   - Run classifications
   - Review results

2. **Set Up Batch Processing**
   - Create scheduled job
   - Process documents automatically
   - Export results to Delta Lake

3. **Monitor Usage**
   - Check cluster metrics
   - Monitor API costs
   - Review classification accuracy

4. **Scale Up**
   - Increase cluster size for more documents
   - Enable auto-scaling
   - Set up production workflows

---

## Quick Reference

### Important URLs
- **Workspace**: `https://your-workspace.cloud.databricks.com`
- **Databricks Docs**: https://docs.databricks.com
- **OpenRouter**: https://openrouter.ai

### Important Paths
- **Python Files**: `/FileStore/document_classifier/`
- **Input Documents**: `/FileStore/documents/input/`
- **Output Results**: `/FileStore/documents/output/`
- **Test Documents**: `/FileStore/documents/test_documents/`

### Key Commands
```bash
# Upload file
databricks fs cp local.pdf dbfs:/FileStore/documents/input/

# List files
databricks fs ls dbfs:/FileStore/documents/input/

# Download results
databricks fs cp dbfs:/FileStore/documents/output/results.json ./

# Check secrets
databricks secrets list --scope document-classifier
```

---

## Support

If you get stuck:
1. Check the troubleshooting section above
2. Review `README_DATABRICKS.md` for details
3. Check Databricks documentation
4. Review notebook error messages

---

## Summary

You should now have:
- ✅ Databricks workspace set up
- ✅ CLI configured
- ✅ Files uploaded
- ✅ Secrets configured
- ✅ Notebooks imported
- ✅ Cluster running
- ✅ System tested and working

**Congratulations! Your AI Document Classification System is now running on Databricks!** 🎉

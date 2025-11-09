# 🌐 MCP Web Inspector - Complete Guide

## Quick Start

### Launch Web Inspector (One Command)

```bash
./launch_mcp_inspector.sh
```

**OR manually:**

```bash
npx @modelcontectprotocol/inspector mcp-server-config.json
```

This will:
1. Start the MCP Inspector server
2. Launch your Job Matcher MCP server
3. Open web browser at `http://localhost:5173`

---

## 🖥️ Web Interface Overview

### What You'll See

```
┌─────────────────────────────────────────────────────────────┐
│  MCP Inspector                                    [Connect] │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🔌 Connected Servers                                       │
│  ├─ job-matcher ✅ Connected                               │
│  │                                                          │
│  📋 Tabs:                                                   │
│  ├─ Tools (4 available)                                    │
│  ├─ Resources                                              │
│  ├─ Prompts                                                │
│  └─ Logs                                                   │
│                                                              │
│  🔧 TOOLS TAB (Active)                                      │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 1. get_job_statistics                              │    │
│  │    Get statistics about collected jobs             │    │
│  │    [View Details] [Test]                           │    │
│  │                                                     │    │
│  │ 2. collect_jobs                                    │    │
│  │    Collect jobs from all sources                   │    │
│  │    [View Details] [Test]                           │    │
│  │                                                     │    │
│  │ 3. extract_resume                                  │    │
│  │    Extract text from resume PDF                    │    │
│  │    [View Details] [Test]                           │    │
│  │                                                     │    │
│  │ 4. match_jobs                                      │    │
│  │    AI-powered job matching with scores             │    │
│  │    [View Details] [Test]                           │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 4 Available Tools

### 1. `get_job_statistics`

**What it does**: Shows you stats about collected jobs

**Parameters**: None (click and run!)

**Example Output**:
```json
{
  "total_jobs": 521,
  "sources": {
    "LinkedIn": 98,
    "GitHub": 423
  },
  "sample_jobs": [...]
}
```

**Use in Inspector**:
1. Click "Tools" tab
2. Click `get_job_statistics`
3. Click "Execute" button
4. See results instantly!

---

### 2. `collect_jobs`

**What it does**: Collects jobs from specified sources

**Parameters**:
- `sources` (array): Choose from `["linkedin", "github", "data"]`

**Example in Web UI**:
```
Parameter: sources
Value: ["linkedin", "github"]

[Execute]
```

**Output**:
```
✅ Collected 521 jobs from 2 sources
```

---

### 3. `extract_resume`

**What it does**: Parses resume PDF and extracts text

**Parameters**:
- `resume_path` (string): Path to PDF file

**Example in Web UI**:
```
Parameter: resume_path
Value: MCP_Servers/pdfDocs/Resume_NEW_ML_Pathakota_Pranavi_2.pdf

[Execute]
```

**Output**:
```
📄 Resume Extracted:

Length: 5750 characters

Preview:
Pranavi Pathakota
Software Engineer | ML Enthusiast
...
```

---

### 4. `match_jobs` ⭐ (Most Powerful)

**What it does**: Uses AI to match jobs with resume and rank them

**Parameters**:
- `top_n` (number): Number of matches to return (default: 10)

**Example in Web UI**:
```
Parameter: top_n
Value: 10

[Execute]
```

**Output**:
```
🎯 Top 10 Job Matches:

1. Machine Learning Engineer at Google
   Score: 95/100
   Reason: Strong alignment with Python, TensorFlow, and ML coursework...
   Link: https://...

2. AI Research Engineer at OpenAI
   Score: 92/100
   Reason: Perfect match for research background and NLP experience...
   Link: https://...

[... 8 more matches ...]
```

---

## 📊 Step-by-Step Tutorial

### Tutorial 1: View Job Statistics

1. **Launch Inspector**:
   ```bash
   ./launch_mcp_inspector.sh
   ```

2. **Wait for browser** to open at `http://localhost:5173`

3. **Check connection**:
   - Top right should show: ✅ "job-matcher Connected"

4. **Click "Tools" tab**

5. **Find "get_job_statistics"** in the list

6. **Click "Test" or "Execute"**

7. **View results** - should show:
   ```
   Total: 521 jobs
   Sources: LinkedIn (98), GitHub (423)
   ```

**Expected Time**: 5 seconds

---

### Tutorial 2: Test AI Job Matching

1. **In Inspector, click "Tools" tab**

2. **Select `match_jobs`**

3. **Set parameter**:
   - `top_n`: `5` (for fast demo)

4. **Click "Execute"**

5. **Wait ~10-15 seconds** (AI is analyzing jobs!)

6. **View results**:
   - Top 5 job matches
   - Match scores (0-100)
   - AI reasoning for each match
   - Apply links

**Expected Time**: 15 seconds

---

### Tutorial 3: Extract and View Resume

1. **Select `extract_resume` tool**

2. **Enter path**:
   ```
   MCP_Servers/pdfDocs/Resume_NEW_ML_Pathakota_Pranavi_2.pdf
   ```

3. **Click "Execute"**

4. **See extracted text**:
   - Full resume content
   - Character count
   - Preview of first 500 chars

**Expected Time**: 2 seconds

---

## 🎬 Demo Workflow (for Challenge Presentation)

### 5-Minute Live Demo

**Minute 1: Introduction**
```
"I built an MCP server that uses AI to match jobs with resumes.
Let me show you the tools available via the MCP Inspector."
```

**Minute 2: Show Tools**
```
[Open web inspector]
"Here are 4 MCP tools exposed by my server:
1. Statistics - shows 521 collected jobs
2. Collection - gathers from multiple sources
3. Resume parsing - extracts context
4. AI Matching - the magic happens here"
```

**Minute 3: Execute Statistics**
```
[Click get_job_statistics]
[Execute]
"As you can see, we've collected 521 jobs from LinkedIn and GitHub."
```

**Minute 4: AI Matching Demo**
```
[Click match_jobs]
[Set top_n = 5]
[Execute]
[Wait for results]
"The AI analyzes each job against the resume and provides:
- Match score (95/100)
- Reasoning (why it matches)
- Direct apply link"
```

**Minute 5: Impact**
```
"This solves the problem of spending 20+ hours/week job searching.
Instead: 5 minutes, AI-powered, personalized recommendations."
```

---

## 🔍 Troubleshooting

### Port Already in Use

**Error**: "Port 5173 is already in use"

**Solution**:
```bash
# Kill existing inspector
pkill -f "mcp.*inspector"

# Or use different port
npx @modelcontextprotocol/inspector --port 5174 mcp-server-config.json
```

---

### Server Won't Connect

**Error**: "job-matcher" shows ❌ Disconnected

**Solutions**:

1. **Check Python path**:
   ```bash
   which python3
   # Update mcp-server-config.json if needed
   ```

2. **Test server manually**:
   ```bash
   python3 job_matcher_mcp_stdio.py
   # Should show: "Job Matcher MCP Server started"
   # Press Ctrl+C to exit
   ```

3. **Check GEMINI_API_KEY**:
   ```bash
   echo $GEMINI_API_KEY
   # Or check .env file
   ```

---

### Tool Execution Fails

**Error**: Tool returns error message

**Solutions**:

1. **Check file paths** (for extract_resume):
   ```bash
   # Use absolute path
   /Users/pranavi/Documents/Courses/Programming_LLMs/Project/MCP_Servers/pdfDocs/Resume_NEW_ML_Pathakota_Pranavi_2.pdf
   ```

2. **Check data exists**:
   ```bash
   # Verify jobs are collected
   ls linkedin_collector/job_search_results/
   ls data/
   ```

---

## 📸 Screenshots to Take (for Challenge)

### Screenshot 1: Tools List
- Capture the Tools tab showing all 4 tools
- Shows professional API design

### Screenshot 2: Tool Execution
- Click `get_job_statistics`
- Execute
- Capture the result showing 521 jobs

### Screenshot 3: AI Matching
- Execute `match_jobs` with top_n=5
- Capture results with scores and reasoning
- Shows AI integration

### Screenshot 4: Request/Response Logs
- Click "Logs" tab
- Shows MCP protocol in action
- Technical depth

---

## 🎥 Video Recording Tips

### Recommended Flow (60 seconds)

**0:00 - 0:10**: Launch inspector, show web interface
```bash
./launch_mcp_inspector.sh
```

**0:10 - 0:20**: Navigate to Tools tab, show 4 tools

**0:20 - 0:35**: Execute `get_job_statistics`
- Click tool
- Execute
- Show results: "521 jobs from 2 sources"

**0:35 - 0:55**: Execute `match_jobs`
- Set top_n = 3
- Execute
- Show AI results with scores

**0:55 - 1:00**: Closing
"MCP-powered job matching in action!"

---

## 🚀 Advanced Features

### Logs Tab

Shows all MCP protocol messages:
```json
Request:
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "match_jobs",
    "arguments": {"top_n": 5}
  }
}

Response:
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{
      "type": "text",
      "text": "🎯 Top 5 Job Matches:..."
    }]
  }
}
```

**Use for**: Understanding MCP protocol, debugging

---

### Resources Tab

Shows available data resources:
- Resume PDFs
- Job collections
- Match results

**Use for**: Context awareness demonstration

---

## 📋 Checklist for Challenge Demo

- [ ] Inspector launches successfully
- [ ] All 4 tools are visible
- [ ] Server connects (green checkmark)
- [ ] `get_job_statistics` executes and shows 521 jobs
- [ ] `match_jobs` executes and returns scored matches
- [ ] Screenshots/video captured
- [ ] Can explain each tool's purpose
- [ ] Can show AI reasoning in results

---

## 💡 Why Web Inspector is Important

### For Challenge Submission

✅ **Visual Proof**: Shows working MCP implementation
✅ **Interactive Demo**: Judges can test tools themselves
✅ **Professional**: Industry-standard tooling
✅ **Transparency**: Shows MCP protocol compliance

### vs. CLI Inspector

| Feature | Web Inspector | CLI Inspector |
|---------|--------------|---------------|
| Visual | ✅ Beautiful UI | ❌ Text only |
| Screenshots | ✅ Easy | ❌ Harder |
| Demo-friendly | ✅ Yes | ⚠️ Technical |
| Testing | ✅ Click & test | ⚠️ Type commands |
| Logs | ✅ Visual | ❌ Scrolling |

**Recommendation**: Use both!
- **Web Inspector**: For demos, screenshots, presentation
- **CLI Inspector**: For development, debugging, testing

---

## 🎯 Success Criteria

After running web inspector, you should be able to:

✅ See all 4 tools in the interface
✅ Execute `get_job_statistics` successfully
✅ Execute `match_jobs` and see AI-generated results
✅ Take professional screenshots
✅ Record a demo video
✅ Explain how MCP enables context-aware AI

---

## 🔗 Quick Links

- **Launch**: `./launch_mcp_inspector.sh`
- **Config**: `mcp-server-config.json`
- **Server**: `job_matcher_mcp_stdio.py`
- **Docs**: This file!

---

## 📞 Getting Help

If inspector isn't working:

1. Check terminal output for errors
2. Verify config file paths are correct
3. Test server standalone: `python3 job_matcher_mcp_stdio.py`
4. Ensure port 5173 is free: `lsof -i :5173`

**Ready to launch?**

```bash
./launch_mcp_inspector.sh
```

🎉 Enjoy exploring your MCP server in the web interface!

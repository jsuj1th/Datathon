# Using Databricks MCP with Kiro

## What is Databricks MCP?

The Databricks MCP (Model Context Protocol) server allows Kiro to interact directly with your Databricks workspace - upload files, run queries, execute notebooks, and more - all from within Kiro!

## Setup Steps

### Step 1: Get Your Databricks Credentials

1. **Workspace URL**
   - Your Databricks workspace URL (e.g., `https://dbc-12345678-abcd.cloud.databricks.com`)
   - You should already have this from signing up

2. **Access Token**
   - Go to Databricks → User Settings → Developer → Access Tokens
   - Click "Generate New Token"
   - Comment: `Kiro MCP Access`
   - Lifetime: 90 days
   - Click "Generate"
   - **Copy the token immediately!**

### Step 2: Configure MCP in Kiro

1. **Edit the MCP config file**
   - File is at: `.kiro/settings/mcp.json`
   - Update these values:

```json
{
  "mcpServers": {
    "databricks": {
      "command": "uvx",
      "args": ["databricks-mcp-server"],
      "env": {
        "DATABRICKS_HOST": "https://your-workspace.cloud.databricks.com",
        "DATABRICKS_TOKEN": "dapi1234567890abcdef..."
      },
      "disabled": false,
      "autoApprove": [
        "list_workspace_files",
        "read_workspace_file",
        "execute_sql_query",
        "list_volumes"
      ]
    }
  }
}
```

2. **Replace:**
   - `your-workspace.cloud.databricks.com` → Your actual workspace URL
   - `dapi1234567890abcdef...` → Your actual access token

### Step 3: Install UV (if not already installed)

The Databricks MCP server uses `uvx` to run. Install UV:

```bash
# On Mac/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv

# Or with pip
pip install uv
```

### Step 4: Restart Kiro

After updating the MCP config, restart Kiro to load the Databricks MCP server.

### Step 5: Test the Connection

In Kiro, you can now ask:

```
"List files in my Databricks workspace"
"Upload config.py to Databricks workspace at /Users/me/document_classifier/"
"Create a Unity Catalog volume for document storage"
"Run this SQL query in Databricks: CREATE CATALOG IF NOT EXISTS main"
```

## What You Can Do with Databricks MCP

### 1. Upload Files

```
"Upload all Python files from the current directory to Databricks workspace at /Users/my-email/document_classifier/"
```

### 2. Create Storage

```
"Create Unity Catalog volumes for document classification:
- main.document_classifier.input_documents
- main.document_classifier.output_results"
```

### 3. Run SQL Queries

```
"Execute this SQL in Databricks:
CREATE CATALOG IF NOT EXISTS main;
CREATE SCHEMA IF NOT EXISTS main.document_classifier;
CREATE VOLUME IF NOT EXISTS main.document_classifier.input_documents;"
```

### 4. List and Read Files

```
"List all files in /Users/my-email/document_classifier/"
"Read the content of config.py from Databricks workspace"
```

### 5. Execute Notebooks

```
"Run the document classification notebook in Databricks"
```

### 6. Manage Clusters

```
"List all Databricks clusters"
"Start the document-classifier-cluster"
```

## Complete Deployment via MCP

Once MCP is set up, you can deploy everything through Kiro:

### Step 1: Upload Python Files

```
"Upload these files to Databricks workspace at /Users/my-email/document_classifier/:
- config.py
- preprocessor.py
- classifier.py
- prompt_library.py
- hitl_manager.py
- metrics_tracker.py
- batch_processor.py"
```

### Step 2: Create Storage

```
"Create Unity Catalog storage for documents:
1. Create catalog 'main' if not exists
2. Create schema 'main.document_classifier'
3. Create volumes:
   - main.document_classifier.input_documents
   - main.document_classifier.output_results
   - main.document_classifier.test_documents"
```

### Step 3: Upload Test Documents

```
"Upload all PDF files from test_documents/ to Databricks volume main.document_classifier.test_documents"
```

### Step 4: Create and Run Notebook

```
"Create a Databricks notebook called 'classify_documents' with this code:
[paste the classification code]

Then run it on the document-classifier-cluster"
```

## Available MCP Tools

The Databricks MCP server provides these tools:

| Tool | Description |
|------|-------------|
| `list_workspace_files` | List files in workspace |
| `read_workspace_file` | Read file content |
| `write_workspace_file` | Upload/create files |
| `delete_workspace_file` | Delete files |
| `execute_sql_query` | Run SQL queries |
| `list_catalogs` | List Unity Catalog catalogs |
| `list_schemas` | List schemas |
| `list_volumes` | List volumes |
| `list_clusters` | List compute clusters |
| `start_cluster` | Start a cluster |
| `stop_cluster` | Stop a cluster |
| `run_notebook` | Execute a notebook |
| `get_notebook_output` | Get notebook results |

## Auto-Approved Tools

These tools are auto-approved (no confirmation needed):
- `list_workspace_files`
- `read_workspace_file`
- `execute_sql_query`
- `list_volumes`

Other tools will ask for confirmation before executing.

## Security Notes

1. **Token Security**
   - Your Databricks token is stored in `.kiro/settings/mcp.json`
   - This file should be in `.gitignore` (it is)
   - Never commit this file to Git

2. **Token Permissions**
   - The token has full access to your Databricks workspace
   - Only use it in trusted environments
   - Rotate tokens regularly (every 90 days)

3. **Auto-Approve Carefully**
   - Only auto-approve read-only operations
   - Write operations should require confirmation

## Troubleshooting

### "uvx: command not found"

Install UV:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### "Connection failed"

Check:
1. Workspace URL is correct (include `https://`)
2. Token is valid (not expired)
3. Token has proper permissions

### "MCP server not found"

The Databricks MCP server might not be available yet. Check:
```bash
uvx databricks-mcp-server --help
```

If not available, use the manual upload method from `SIMPLE_UI_UPLOAD.md`

## Alternative: Use Databricks CLI via MCP

If Databricks MCP server isn't available, you can use the filesystem MCP to run Databricks CLI commands:

```
"Run this command: databricks workspace import config.py /Users/me/document_classifier/config.py"
```

## Benefits of Using MCP

✅ **No manual uploads** - Upload files directly from Kiro
✅ **Automated setup** - Create storage and notebooks via chat
✅ **Integrated workflow** - Deploy and test without leaving Kiro
✅ **Version control** - Easy to update files when code changes
✅ **Batch operations** - Upload multiple files at once

## Example: Complete Deployment via Kiro

```
User: "Deploy the document classification system to Databricks"

Kiro will:
1. Upload all Python files to workspace
2. Create Unity Catalog volumes
3. Upload test documents
4. Create classification notebook
5. Set up batch job
6. Test with a sample document

All through MCP - no manual steps needed!
```

## Summary

With Databricks MCP configured:
- ✅ Upload files from Kiro
- ✅ Create storage via SQL
- ✅ Run notebooks remotely
- ✅ Manage clusters
- ✅ Complete deployment automation

**No more manual file uploads!** 🚀

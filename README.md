# LinkedIn Jobs MCP Server

A Model Context Protocol (MCP) server that provides LinkedIn job search functionality with structured JSON output. Perfect for integrating with Claude Desktop and other MCP-compatible clients.

## 🚀 Features

### Core Functionality
- **LinkedIn Job Search**: Search for jobs on LinkedIn with keywords and location filters
- **Structured JSON Output**: Returns standardized job data format for easy integration
- **MCP Protocol Compliance**: Works seamlessly with Claude Desktop and other MCP clients
- **Real-time Data**: Direct access to LinkedIn's job listings through unofficial API

## 🛠️ Architecture

### MCP Server Structure
```
├── src/
│   └── server/          # MCP server implementation
│       └── linkedin_mcp_client.py  # Main LinkedIn Jobs MCP client
├── main.py              # Server entry point
├── requirements.txt     # Python dependencies
├── .env.example        # Environment template
└── test_json_format.py  # JSON format validation test
```

### Available Tool

#### `search_jobs` Tool
**Purpose**: Search for jobs on LinkedIn and return structured JSON data

**Parameters**:
- `keywords`: Job search terms (e.g., "software engineer", "data scientist")
- `limit`: Number of results to return (default: 10)
- `offset`: Skip first N results (for pagination)
- `location`: Geographic filter (e.g., "San Francisco", "Remote")

**Returns**: JSON string with structured job data in the following format:
```json
{
  "company": "Company Name",
  "position": "Job Title",
  "apply_link": "https://www.linkedin.com/jobs/view/12345",
  "location": "City, State",
  "salary": null,
  "description": "Job description...",
  "requirements": null,
  "benefits": null,
  "job_type": "full_time",
  "experience_level": null,
  "posted_date": null,
  "deadline": null,
  "days_since_posted": null,
  "remote_option": "onsite",
  "visa_sponsorship": null,
  "source": "linkedin",
  "collection_method": "mcp_linkedin",
  "collected_at": "2025-11-08T12:26:13.688951",
  "field": null,
  "company_type": null
}
```

## 📋 Prerequisites

- Node.js 18+ or Python 3.9+
- Valid email account for notifications
- API keys for supported platforms (where available)
- Chrome/Chromium for web scraping

## ⚡ Quick Start

### Installation

### Installation

#### Quick Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/jobly-linkedin-mcp-server.git
cd jobly-linkedin-mcp-server

# Run the setup script
./setup.sh

# Edit your LinkedIn credentials
cp .env.example .env
# Edit .env and add your LinkedIn email and password
```

#### Manual Installation

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install Python dependencies
pip install -r requirements.txt
pip install -e .

# Copy environment configuration
cp .env.example .env
# Edit .env with your LinkedIn credentials
```

#### Using the Existing LinkedIn MCP Server

This project is based on the excellent work from [adhikasp/mcp-linkedin](https://github.com/adhikasp/mcp-linkedin). You can also install directly via Smithery:

```bash
npx -y @smithery/cli install mcp-linkedin --client claude
```

### Configuration

Create a `.env` file with your settings:

```env
# LinkedIn API Credentials (Required)
LINKEDIN_EMAIL=your_linkedin_email@example.com
LINKEDIN_PASSWORD=your_linkedin_password

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# API Keys (optional but recommended)
LINKEDIN_API_KEY=your-linkedin-key
GLASSDOOR_API_KEY=your-glassdoor-key
GITHUB_TOKEN=your-github-token

# Job Search Preferences
TARGET_LOCATIONS=San Francisco,New York,Remote
EXPERIENCE_LEVEL=mid,senior
JOB_TYPES=full-time,contract
SALARY_MIN=80000

# MCP Server Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
DEBUG=false
```

#### Claude Desktop Configuration

To use with Claude Desktop, add this configuration to your Claude Desktop settings:

```json
{
  "mcpServers": {
    "linkedin": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/your/jobly-linkedin-mcp-server",
      "env": {
        "LINKEDIN_EMAIL": "your_linkedin_email",
        "LINKEDIN_PASSWORD": "your_linkedin_password"
      }
    }
  }
}
```

### Running the Server

```bash
# Test the installation first
python test_linkedin_mcp.py

# Start the MCP server
python main.py

# The server will be available at the configured MCP endpoint
```

### Testing

```bash
# Test LinkedIn API functionality
python test_simple_linkedin.py

# Test JSON format output
python test_json_format.py

# Start the MCP server
python main.py
```

## 🎯 Usage

### Basic Job Search with Claude Desktop

Once configured with Claude Desktop, you can use natural language commands:

- **"Search for Python developer jobs in San Francisco"**
  - Calls: `search_jobs("python developer", 3, 0, "San Francisco")`

- **"Find remote data scientist positions"** 
  - Calls: `search_jobs("data scientist", 10, 0, "remote")`

- **"Look for entry-level software engineer jobs"**
  - Calls: `search_jobs("entry level software engineer", 5, 0, "")`

### Direct Function Call

```python
from src.server.linkedin_mcp_client import test_search_jobs
import json

# Search for jobs
result = test_search_jobs("software engineer", "remote", 5)
print(json.dumps(result, indent=2))
```

## 🔧 Configuration Options

### Job Search Parameters
- **Keywords**: Any job title, skill, or company name
- **Location**: City, state, country, or "remote"
- **Limit**: Number of jobs to return (1-25 recommended)
- **Offset**: For pagination through large result sets

### Data Fields Returned
- **Basic Info**: Company, position, location, apply link
- **Job Details**: Description, salary, requirements, benefits
- **Job Type**: full_time, part_time, contract, internship, entry_level
- **Work Style**: onsite, remote, hybrid
- **Metadata**: Source, collection method, timestamp

## 🚨 Troubleshooting

### Common Issues

#### LinkedIn API Connection Issues
```bash
# Test LinkedIn credentials
python test_simple_linkedin.py

# Check if LinkedIn login works manually
# Sometimes LinkedIn requires you to verify your account
```

#### No Jobs Found
```bash
# Try different search terms
python -c "from src.server.linkedin_mcp_client import test_search_jobs; print(test_search_jobs('python', '', 5))"

# Check if location is too specific
# Try broader location terms like 'remote' or 'United States'
```

#### MCP Server Issues
```bash
# Test the server startup
python main.py

# Check if all dependencies are installed
pip install -r requirements.txt
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone and setup
git clone https://github.com/yourusername/jobly-linkedin-mcp-server.git
cd jobly-linkedin-mcp-server
./setup.sh

# Test the setup
python test_simple_linkedin.py

# Start development server
python main.py
```

### Testing
```bash
# Test LinkedIn API functionality
python test_simple_linkedin.py

# Test MCP server import
python -c "from src.server.linkedin_mcp_client import mcp; print('MCP server ready')"

# Start the server
python main.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MCP Protocol developers
- Open source scraping libraries
- Job board APIs and documentation
- Resume parsing libraries
- Email service providers

## 📞 Support

- **Documentation**: [docs.jobseeker-mcp.com](https://docs.jobseeker-mcp.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/jobseeker-mcp-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/jobseeker-mcp-server/discussions)
- **Email**: support@jobseeker-mcp.com

## 🗺️ Roadmap

### Version 1.0 (Current)
- [x] Basic job scraping
- [x] Resume analysis
- [x] Email notifications
- [x] LinkedIn integration

### Version 1.1 (Next)
- [ ] Advanced AI matching
- [ ] Application tracking
- [ ] Interview preparation
- [ ] Salary negotiation tools

### Version 2.0 (Future)
- [ ] Mobile app companion
- [ ] Team collaboration features
- [ ] Advanced analytics dashboard
- [ ] API marketplace integration

---

**Made with ❤️ for job seekers everywhere**
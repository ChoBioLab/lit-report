# Semantic Scholar Paper Search Tool

A powerful Python toolkit for searching and analyzing academic papers using the Semantic Scholar API with **advanced semantic search capabilities**. This tool goes beyond simple keyword matching to understand the meaning and context of your research queries.

## 🚀 Key Features

### **🧠 Semantic Search Powered**

- **Natural Language Queries**: Use full sentences and research questions instead of just keywords
- **Conceptual Understanding**: Finds papers about "inflammatory bowel disease" when you search "IBD"
- **Synonym Recognition**: Automatically matches related terms and concepts
- **Context-Aware**: Understands research methodology, populations, and domains

### **📊 Dual Analysis Modes**

- **Top Cited Papers**: Find the most influential papers in your field within a specific timeframe
- **Recent Papers**: Discover the latest research across multiple keywords

### **🎯 Smart Filtering**

- Exclude unwanted topics or methodologies
- Customizable time ranges
- Configurable result limits
- Field-specific data retrieval

## 📋 Prerequisites

- Python 3.7+
- Semantic Scholar API key ([Get one here](https://www.semanticscholar.org/product/api))
- Required packages: `requests`

## ⚙️ Setup

1. **Install dependencies:**

   ```bash
   pip install requests
   ```

2. **Set your API key:**

   ```bash
   # Windows
   set SEMANTIC_SCHOLAR_API_KEY=your_api_key_here

   # Mac/Linux
   export SEMANTIC_SCHOLAR_API_KEY=your_api_key_here
   ```

## 🔍 Usage Examples

### **Basic Usage**

```bash
# Default search (IBD research)
python main.py

# Simple keyword search
python main.py --query "machine learning"
```

### **🧠 Semantic Search Examples**

**Natural Language Research Questions:**

```bash
python main.py --query "What are the genetic risk factors for inflammatory bowel disease?"

python main.py --query "How effective are biologics in treating pediatric Crohn's disease?"

python main.py --query "What machine learning approaches show promise for early IBD diagnosis?"
```

**Complex Semantic Phrases:**

```bash
python main.py --query "personalized medicine approaches for treatment-resistant ulcerative colitis"

python main.py --query "gut-brain axis mechanisms in inflammatory bowel disease pathogenesis"

python main.py --query "novel therapeutic targets for preventing IBD complications"
```

**Multi-Keyword Semantic Search:**

```bash
python main.py --keywords "How do genetic variants influence IBD susceptibility" "What environmental factors trigger Crohn's disease" "Why do some patients not respond to anti-TNF therapy"
```

### **🎯 Advanced Filtering**

**Exclude Specific Topics:**

```bash
python main.py --query "IBD treatment" --exclude-terms "surgery" "pediatric" "animal model"
```

**Custom Time Ranges:**

```bash
# Recent papers from last 30 days
python main.py --days-back 30

# Top cited papers from last 6 months
python main.py --months-back 6
```

**Result Customization:**

```bash
# Get top 10 papers, show 5 per keyword
python main.py --top-n 10 --display-limit 5

# Fetch more comprehensive results
python main.py --max-results-per-keyword 300 --max-fetch-top-cited 2000
```

## 📊 Output Format

Each paper includes:

- **Title** and **Authors** (formatted for readability)
- **Journal/Venue** and **Publication Date**
- **Citation Count** (for impact assessment)
- **DOI/URL** (direct access links)
- **TLDR** (AI-generated summary when available)

## 🛠️ Command Line Options

| Option                      | Description                                      | Default                                                     |
| --------------------------- | ------------------------------------------------ | ----------------------------------------------------------- |
| `--query`                   | Primary search query (supports natural language) | `"IBD"`                                                     |
| `--keywords`                | Multiple keywords for recent search              | `["IBD genetics", "Crohn's disease", "ulcerative colitis"]` |
| `--exclude-terms`           | Terms to filter out from results                 | `["microbiome", "prebiotics", "probiotics"]`                |
| `--days-back`               | Days back for recent papers search               | `7`                                                         |
| `--months-back`             | Months back for top cited papers                 | `12`                                                        |
| `--top-n`                   | Number of top cited papers to retrieve           | `5`                                                         |
| `--max-results-per-keyword` | Max results per keyword                          | `150`                                                       |
| `--display-limit`           | Papers to display per keyword                    | `3`                                                         |
| `--fields`                  | API fields to retrieve                           | All standard fields                                         |

## 🧠 Semantic Search Tips

### **Best Practices for Natural Language Queries:**

1. **Use Research Questions:**

   - ✅ "What causes inflammatory bowel disease flares?"
   - ❌ "IBD flares causes"

2. **Include Context and Specificity:**

   - ✅ "machine learning approaches for predicting IBD treatment response"
   - ❌ "ML IBD"

3. **Describe Your Research Interest:**

   - ✅ "genetic biomarkers for early detection of Crohn's disease"
   - ❌ "genetics Crohn's"

4. **Use Domain-Specific Language:**
   - ✅ "genome-wide association studies in pediatric inflammatory bowel disease"
   - ❌ "GWAS kids IBD"

### **The API Automatically Handles:**

- **Acronym Expansion**: "IBD" → "inflammatory bowel disease"
- **Synonym Matching**: "ML" → "machine learning", "artificial intelligence"
- **Concept Relationships**: "biologics" → "anti-TNF", "adalimumab", "infliximab"
- **Methodological Terms**: "GWAS" → "genome-wide association study"

## 📁 Project Structure

```
├── main.py                    # Main CLI interface
├── semantic_scholar_client.py # API client with rate limiting
├── top_cited_papers.py       # Top cited papers functionality
├── recent_papers_search.py   # Recent papers search
└── paper_utils.py            # Utilities for filtering and formatting
```

## 🔧 Extending the Tool

The modular design makes it easy to:

- Add new search strategies
- Implement additional filtering criteria
- Create custom output formats
- Integrate with other academic databases

## 📝 Example Research Workflows

**Literature Review Workflow:**

```bash
# 1. Get overview of most cited recent work
python main.py --query "your research topic" --top-n 10

# 2. Find latest developments
python main.py --keywords "specific aspect 1" "specific aspect 2" --days-back 30

# 3. Exclude saturated areas
python main.py --query "your topic" --exclude-terms "overresearched area"
```

**Hypothesis Generation:**

```bash
# Find gaps and emerging areas
python main.py --query "What are the unresolved questions in [your field]?" --days-back 90
```

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the tool's semantic search capabilities and functionality.

## 📄 License

This project is open source. Please ensure you comply with Semantic Scholar's API terms of service.

---

**🧠 Powered by Semantic Scholar's Advanced AI** - Leveraging state-of-the-art natural language processing to understand research intent and deliver contextually relevant results.

# Semantic Scholar Paper Search Tool

A Python toolkit for searching and analyzing academic papers using the Semantic Scholar API with **advanced semantic search capabilities**. This tool goes beyond simple keyword matching to understand the meaning and context of your research queries.

## Key Features

### **Semantic Search Powered**

- **Natural Language Queries**: Use full sentences and research questions instead of just keywords
- **Conceptual Understanding**: Finds papers about "inflammatory bowel disease" when you search "IBD"
- **Synonym Recognition**: Automatically matches related terms and concepts
- **Context-Aware**: Understands research methodology, populations, and domains

### **Dual Analysis Modes**

- **Top Cited Papers**: Find the most influential papers in your field within a specific timeframe
- **Recent Papers**: Discover the latest research across multiple keywords

### **Smart Filtering**

- Exclude unwanted topics or methodologies
- Customizable time ranges
- Configurable result limits
- Field-specific data retrieval

## Prerequisites

- Python 3.7+
- Semantic Scholar API key ([Get one here](https://www.semanticscholar.org/product/api))
- Required packages: `requests`

## Setup

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

## Usage Examples

### **Basic Usage**

```bash
# Default search (IBD research)
python main.py

# Simple keyword search
python main.py --query "machine learning"
```

### **Semantic Search Examples**

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

### **Advanced Filtering**

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

## Output Format

Each paper includes:

- **Title** and **Authors** (formatted for readability)
- **Journal/Venue** and **Publication Date**
- **Citation Count** (for impact assessment)
- **DOI/URL** (direct access links)
- **TLDR** (AI-generated summary when available)

## Command Line Options

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

This project is open source. Please ensure you comply with Semantic Scholar's API terms of service.

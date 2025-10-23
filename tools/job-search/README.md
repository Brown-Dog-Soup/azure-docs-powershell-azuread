# Job Search Tool

A Python-based command-line tool to search and display job postings matching your specified skills.

## Features

- **Multi-source searching**: Queries multiple free job APIs
- **Skill-based filtering**: Automatically filters jobs based on your skills
- **Smart matching**: Ranks results by number of skill matches
- **Flexible input**: Specify skills via command-line or file
- **Export capability**: Save results to JSON for further analysis
- **No API keys required**: Uses free public APIs (for basic usage)

## Supported Job Sources

- **Remotive.io**: Remote job listings across various categories
- **Arbeitnow**: International job board with focus on tech roles

## Requirements

- Python 3.6 or higher
- No external dependencies (uses Python standard library only)

## Installation

No installation required! Just make the script executable:

```bash
chmod +x job_search.py
```

## Usage

### Basic Usage

Search for jobs matching specific skills:

```bash
python3 job_search.py python javascript react
```

### Advanced Usage

**Limit results:**
```bash
python3 job_search.py python django --limit 5
```

**Use a skills file:**
```bash
# Create a skills file
cat > my_skills.txt << EOF
Python
JavaScript
Azure
PowerShell
Docker
Kubernetes
EOF

python3 job_search.py --skills-file my_skills.txt
```

**Save results to JSON:**
```bash
python3 job_search.py azure devops terraform --output results.json
```

**Filter by location:**
```bash
# Only US jobs
python3 job_search.py python javascript --demo --location us

# Only EU jobs
python3 job_search.py azure devops --demo --location eu

# Only worldwide remote jobs
python3 job_search.py python --demo --location worldwide
```

**Verbose mode for debugging:**
```bash
python3 job_search.py "machine learning" python --verbose
```

**Combine options:**
```bash
python3 job_search.py --skills-file skills.txt --limit 10 --location us --output my_jobs.json --verbose
```

## Command-Line Options

```
positional arguments:
  skills                Skills to search for (space-separated)

optional arguments:
  -h, --help            Show help message and exit
  --skills-file, -f     File containing skills (one per line)
  --limit, -l          Maximum number of results to display
  --output, -o         Save results to JSON file
  --location           Filter jobs by location (e.g., "us", "eu", "remote", "worldwide")
  --verbose, -v        Enable verbose output
  --demo, -d           Use demo mode with sample data (for testing)
```

## Example Output

```
Searching for jobs matching skills: python, docker, kubernetes

================================================================================
Found 15 matching job(s). Displaying top 15:
================================================================================

[1] Senior Backend Engineer
    Company: TechCorp Inc.
    Location: Remote
    Posted: 2025-10-20
    Source: Remotive
    Matched Skills: python, docker, kubernetes (3 match(es))
    URL: https://example.com/job/123
    Description: We are looking for a Senior Backend Engineer with strong Python...
--------------------------------------------------------------------------------

[2] DevOps Engineer
    Company: CloudStart
    Location: Remote - EU
    Posted: 2025-10-19
    Source: Arbeitnow
    Matched Skills: docker, kubernetes (2 match(es))
    URL: https://example.com/job/456
    Description: Join our DevOps team to build scalable infrastructure...
--------------------------------------------------------------------------------

Total jobs found: 15
```

## Skills File Format

Create a text file with one skill per line:

```
Python
JavaScript
React
Node.js
AWS
Azure
Docker
Kubernetes
Machine Learning
Data Science
```

## Output JSON Format

When using `--output`, results are saved in the following format:

```json
[
  {
    "title": "Senior Backend Engineer",
    "company": "TechCorp Inc.",
    "location": "Remote",
    "url": "https://example.com/job/123",
    "posted_date": "2025-10-20",
    "description": "Job description...",
    "matched_skills": ["python", "docker", "kubernetes"],
    "match_score": 3,
    "source": "Remotive"
  }
]
```

## Tips for Best Results

1. **Be specific**: Use exact technology names (e.g., "React" instead of "frontend")
2. **Mix broad and specific**: Include both languages (Python) and frameworks (Django)
3. **Use common variations**: Try both "JavaScript" and "JS", "Kubernetes" and "k8s"
4. **Save results**: Use `--output` to keep a record of searches over time
5. **Regular searches**: Job postings update frequently, so search regularly

## Limitations

- Relies on free public APIs (some job sources may require API keys for extended features)
- Search is text-based matching (not semantic understanding)
- Some job boards are not included due to lack of free APIs
- Rate limits may apply from API providers

## Extending the Tool

To add more job sources:

1. Create a new search method (e.g., `search_newapi()`)
2. Create a normalization method (e.g., `normalize_newapi_job()`)
3. Add the search call in `search_all()` method

## Troubleshooting

**No results found:**
- Try broader skill terms
- Check your internet connection
- Use `--verbose` to see API responses

**Timeout errors:**
- API might be temporarily unavailable
- Check firewall/proxy settings
- Try again later

**Skills not matching:**
- Skills are case-insensitive but must match the text in job descriptions
- Try alternative terms (e.g., "ML" vs "Machine Learning")

## Contributing

This tool is part of a larger project. Feel free to submit improvements!

## License

See the repository LICENSE file for details.

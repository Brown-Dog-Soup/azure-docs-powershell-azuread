#!/usr/bin/env python3
"""
Job Search Tool - Search and display job postings matching specified skills

This tool searches multiple job APIs and filters results based on skills.
Free APIs used:
- Remotive.io (remote jobs)
- Adzuna (requires free API key)
- GitHub Jobs (deprecated but can be used if available)
"""

import argparse
import json
import sys
from typing import List, Dict, Any, Set
from datetime import datetime
import urllib.request
import urllib.parse
import urllib.error


class JobSearcher:
    """Main job search class that queries multiple APIs"""

    def __init__(self, skills: List[str], verbose: bool = False, demo_mode: bool = False, location: str = None):
        self.skills = [skill.lower() for skill in skills]
        self.verbose = verbose
        self.demo_mode = demo_mode
        self.location = location.lower() if location else None
        self.results = []

    def log(self, message: str):
        """Print verbose logging"""
        if self.verbose:
            print(f"[DEBUG] {message}", file=sys.stderr)

    def search_remotive(self) -> List[Dict[str, Any]]:
        """Search Remotive.io for remote jobs"""
        self.log("Searching Remotive.io...")
        url = "https://remotive.io/api/remote-jobs"

        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                jobs = data.get('jobs', [])
                self.log(f"Found {len(jobs)} jobs from Remotive")
                return jobs
        except urllib.error.URLError as e:
            self.log(f"Error fetching from Remotive: {e}")
            return []
        except Exception as e:
            self.log(f"Unexpected error with Remotive: {e}")
            return []

    def search_arbeitnow(self) -> List[Dict[str, Any]]:
        """Search Arbeitnow API for job postings"""
        self.log("Searching Arbeitnow...")
        url = "https://www.arbeitnow.com/api/job-board-api"

        try:
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                jobs = data.get('data', [])
                self.log(f"Found {len(jobs)} jobs from Arbeitnow")
                return jobs
        except urllib.error.URLError as e:
            self.log(f"Error fetching from Arbeitnow: {e}")
            return []
        except Exception as e:
            self.log(f"Unexpected error with Arbeitnow: {e}")
            return []

    def match_skills(self, text: str) -> Set[str]:
        """Check which skills match in the given text"""
        text_lower = text.lower()
        matched = set()

        for skill in self.skills:
            # Check for whole word match or as part of compound words
            if skill in text_lower:
                matched.add(skill)

        return matched

    def matches_location(self, job_location: str) -> bool:
        """Check if job location matches the filter"""
        if not self.location:
            return True  # No filter, accept all

        job_location_lower = job_location.lower()

        # Check if the filter location is in the job location string
        return self.location in job_location_lower

    def normalize_remotive_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize Remotive job data to common format"""
        description = job.get('description', '')
        title = job.get('title', '')
        tags = ' '.join(job.get('tags', []))

        searchable_text = f"{title} {description} {tags}"
        matched_skills = self.match_skills(searchable_text)

        return {
            'title': title,
            'company': job.get('company_name', 'Unknown'),
            'location': job.get('candidate_required_location', 'Remote'),
            'url': job.get('url', ''),
            'posted_date': job.get('publication_date', ''),
            'description': description[:500] + '...' if len(description) > 500 else description,
            'matched_skills': list(matched_skills),
            'match_score': len(matched_skills),
            'source': 'Remotive'
        }

    def normalize_arbeitnow_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize Arbeitnow job data to common format"""
        description = job.get('description', '')
        title = job.get('title', '')
        tags = ' '.join(job.get('tags', []))

        searchable_text = f"{title} {description} {tags}"
        matched_skills = self.match_skills(searchable_text)

        return {
            'title': title,
            'company': job.get('company_name', 'Unknown'),
            'location': job.get('location', 'Remote'),
            'url': job.get('url', ''),
            'posted_date': job.get('created_at', ''),
            'description': description[:500] + '...' if len(description) > 500 else description,
            'matched_skills': list(matched_skills),
            'match_score': len(matched_skills),
            'source': 'Arbeitnow'
        }

    def get_demo_jobs(self) -> List[Dict[str, Any]]:
        """Get demo/sample job postings for testing"""
        self.log("Using demo mode with sample data...")
        return [
            {
                'title': 'Senior Python Developer',
                'company_name': 'TechCorp Inc.',
                'candidate_required_location': 'Remote - Worldwide',
                'url': 'https://example.com/jobs/1',
                'publication_date': '2025-10-20',
                'description': 'We are looking for a Senior Python Developer with experience in Django, Docker, and Kubernetes. You will work on building scalable backend systems.',
                'tags': ['python', 'django', 'docker', 'kubernetes', 'backend']
            },
            {
                'title': 'Full Stack Engineer',
                'company_name': 'StartupXYZ',
                'candidate_required_location': 'Remote - US Only',
                'url': 'https://example.com/jobs/2',
                'publication_date': '2025-10-19',
                'description': 'Join our team as a Full Stack Engineer. Required skills: JavaScript, React, Node.js, Python, and AWS experience. Build modern web applications.',
                'tags': ['javascript', 'react', 'nodejs', 'python', 'aws', 'fullstack']
            },
            {
                'title': 'DevOps Engineer',
                'company_name': 'CloudStart',
                'candidate_required_location': 'Remote - EU',
                'url': 'https://example.com/jobs/3',
                'publication_date': '2025-10-18',
                'description': 'DevOps Engineer needed to manage our cloud infrastructure. Experience with Azure, Terraform, Kubernetes, and CI/CD pipelines required.',
                'tags': ['azure', 'terraform', 'kubernetes', 'devops', 'ci/cd']
            },
            {
                'title': 'Machine Learning Engineer',
                'company_name': 'AI Innovations',
                'candidate_required_location': 'Remote',
                'url': 'https://example.com/jobs/4',
                'publication_date': '2025-10-17',
                'description': 'ML Engineer position focusing on NLP and computer vision. Required: Python, TensorFlow, PyTorch, Docker. Experience with MLOps is a plus.',
                'tags': ['python', 'machine learning', 'tensorflow', 'pytorch', 'docker', 'mlops']
            },
            {
                'title': 'Frontend Developer',
                'company_name': 'WebStudio',
                'candidate_required_location': 'Remote - Americas',
                'url': 'https://example.com/jobs/5',
                'publication_date': '2025-10-16',
                'description': 'Frontend Developer role working with modern JavaScript frameworks. Required: React, TypeScript, CSS. Experience with Next.js preferred.',
                'tags': ['javascript', 'react', 'typescript', 'css', 'frontend']
            },
            {
                'title': 'Backend Engineer - Go',
                'company_name': 'ScaleUp Co',
                'candidate_required_location': 'Remote',
                'url': 'https://example.com/jobs/6',
                'publication_date': '2025-10-15',
                'description': 'Backend Engineer specializing in Go. Build microservices with Go, Docker, Kubernetes, and PostgreSQL. Strong distributed systems knowledge required.',
                'tags': ['go', 'golang', 'docker', 'kubernetes', 'microservices', 'postgresql']
            },
            {
                'title': 'Azure Cloud Architect',
                'company_name': 'Enterprise Solutions Ltd',
                'candidate_required_location': 'Remote - Worldwide',
                'url': 'https://example.com/jobs/7',
                'publication_date': '2025-10-14',
                'description': 'Azure Cloud Architect to design and implement cloud solutions. Required: Azure, PowerShell, ARM templates, Azure DevOps. Certifications preferred.',
                'tags': ['azure', 'powershell', 'cloud', 'devops', 'arm']
            },
            {
                'title': 'Data Engineer',
                'company_name': 'DataFlow Systems',
                'candidate_required_location': 'Remote - EU/US',
                'url': 'https://example.com/jobs/8',
                'publication_date': '2025-10-13',
                'description': 'Data Engineer to build ETL pipelines. Skills needed: Python, SQL, Airflow, Spark, AWS. Experience with data warehousing required.',
                'tags': ['python', 'sql', 'airflow', 'spark', 'aws', 'data engineering']
            }
        ]

    def search_all(self) -> List[Dict[str, Any]]:
        """Search all available job sources"""
        all_jobs = []

        if self.demo_mode:
            # Use demo data instead of API calls
            demo_jobs = self.get_demo_jobs()
            for job in demo_jobs:
                normalized = self.normalize_remotive_job(job)
                if normalized['match_score'] > 0 and self.matches_location(normalized['location']):
                    all_jobs.append(normalized)
        else:
            # Search Remotive
            remotive_jobs = self.search_remotive()
            for job in remotive_jobs:
                normalized = self.normalize_remotive_job(job)
                if normalized['match_score'] > 0 and self.matches_location(normalized['location']):
                    all_jobs.append(normalized)

            # Search Arbeitnow
            arbeitnow_jobs = self.search_arbeitnow()
            for job in arbeitnow_jobs:
                normalized = self.normalize_arbeitnow_job(job)
                if normalized['match_score'] > 0 and self.matches_location(normalized['location']):
                    all_jobs.append(normalized)

        # Sort by match score (descending)
        all_jobs.sort(key=lambda x: x['match_score'], reverse=True)

        return all_jobs


def display_jobs(jobs: List[Dict[str, Any]], limit: int = None):
    """Display jobs in a formatted way"""
    if not jobs:
        print("\nNo jobs found matching your skills.")
        return

    display_count = len(jobs) if limit is None else min(limit, len(jobs))

    print(f"\n{'='*80}")
    print(f"Found {len(jobs)} matching job(s). Displaying top {display_count}:")
    print(f"{'='*80}\n")

    for i, job in enumerate(jobs[:display_count], 1):
        print(f"[{i}] {job['title']}")
        print(f"    Company: {job['company']}")
        print(f"    Location: {job['location']}")
        print(f"    Posted: {job['posted_date']}")
        print(f"    Source: {job['source']}")
        print(f"    Matched Skills: {', '.join(job['matched_skills'])} ({job['match_score']} match(es))")
        print(f"    URL: {job['url']}")
        print(f"    Description: {job['description'][:200]}...")
        print(f"{'-'*80}\n")


def save_to_file(jobs: List[Dict[str, Any]], filename: str):
    """Save results to a JSON file"""
    try:
        with open(filename, 'w') as f:
            json.dump(jobs, f, indent=2)
        print(f"\nResults saved to: {filename}")
    except Exception as e:
        print(f"\nError saving to file: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description='Search job postings based on skills',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s python javascript react
  %(prog)s "machine learning" python tensorflow --limit 5
  %(prog)s azure powershell --output results.json
  %(prog)s --skills-file skills.txt --verbose
        """
    )

    parser.add_argument(
        'skills',
        nargs='*',
        help='Skills to search for (space-separated)'
    )

    parser.add_argument(
        '--skills-file',
        '-f',
        help='File containing skills (one per line)'
    )

    parser.add_argument(
        '--limit',
        '-l',
        type=int,
        help='Maximum number of results to display'
    )

    parser.add_argument(
        '--output',
        '-o',
        help='Save results to JSON file'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--demo',
        '-d',
        action='store_true',
        help='Use demo mode with sample data (for testing)'
    )

    parser.add_argument(
        '--location',
        help='Filter jobs by location (e.g., "us", "eu", "remote", "worldwide")'
    )

    args = parser.parse_args()

    # Collect skills from arguments and/or file
    skills = list(args.skills) if args.skills else []

    if args.skills_file:
        try:
            with open(args.skills_file, 'r') as f:
                file_skills = [line.strip() for line in f if line.strip()]
                skills.extend(file_skills)
        except FileNotFoundError:
            print(f"Error: Skills file '{args.skills_file}' not found", file=sys.stderr)
            sys.exit(1)

    if not skills:
        parser.print_help()
        print("\nError: No skills specified. Provide skills as arguments or use --skills-file",
              file=sys.stderr)
        sys.exit(1)

    print(f"Searching for jobs matching skills: {', '.join(skills)}")
    if args.location:
        print(f"Location filter: {args.location}")
    if args.demo:
        print("(Running in DEMO mode with sample data)")

    # Create searcher and search
    searcher = JobSearcher(skills, verbose=args.verbose, demo_mode=args.demo, location=args.location)
    jobs = searcher.search_all()

    # Display results
    display_jobs(jobs, limit=args.limit)

    # Save to file if requested
    if args.output:
        save_to_file(jobs, args.output)

    # Print summary
    print(f"\nTotal jobs found: {len(jobs)}")


if __name__ == '__main__':
    main()

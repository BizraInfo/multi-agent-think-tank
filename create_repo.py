import os
import requests
import sys

def create_github_repo(token):
    """Create a new GitHub repository using the GitHub API."""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': 'multi-agent-think-tank',
        'description': 'A sophisticated multi-agent system that leverages collaborative AI agents for complex problem-solving and analysis',
        'private': False,
        'has_issues': True,
        'has_projects': True,
        'has_wiki': True
    }
    
    response = requests.post(
        'https://api.github.com/user/repos',
        headers=headers,
        json=data
    )
    
    if response.status_code == 201:
        repo_info = response.json()
        print(f"Repository created successfully: {repo_info['html_url']}")
        return repo_info['clone_url']
    else:
        print(f"Failed to create repository: {response.status_code}")
        print(response.json())
        return None

def setup_git_remote(clone_url):
    """Set up the Git remote and push the code."""
    os.system('git remote add origin ' + clone_url)
    os.system('git branch -M main')
    os.system('git push -u origin main')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_repo.py <github_token>")
        sys.exit(1)
        
    token = sys.argv[1]
    clone_url = create_github_repo(token)
    
    if clone_url:
        setup_git_remote(clone_url)

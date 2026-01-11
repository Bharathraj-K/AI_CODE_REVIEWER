import requests
from .config import GITHUB_TOKEN, GITHUB_API_BASE

class GitHubAPI:
    def __init__(self):
        self.headers = { 
            "authorization" : f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json" 
        }
    
    def get_pr_files(self, repo, pr_number):
        url  = f"{GITHUB_API_BASE}/repos/{repo}/pulls/{pr_number}/files"
        reponse = requests.get(url, headers=self.headers)
        if reponse.status_code == 200:
            return reponse.json()
        else:
            raise Exception(f"Failed to fetch PR files: {reponse.status_code} - {reponse.text}")
    
    def post_comment(self,repo, pr_number, body):
        url  = f"{GITHUB_API_BASE}/repos/{repo}/issues/{pr_number}/comments"
        data = {"body" : body}
        reponse = requests.post(url, json=data, headers=self.headers)
        if reponse.status_code == 201:
            return reponse.json()
        else:
            raise Exception(f"Failed to post comment: {reponse.status_code} - {reponse.text}")

    def get_file_contents(self, repo, path, ref = "main"):
        url = f"{GITHUB_API_BASE}/repos/{repo}/contents/{path}?ref={ref}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch file contents: {response.status_code} - {response.text}")
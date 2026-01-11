from app.github_api import GitHubAPI

api = GitHubAPI()

repo = "Bharathraj-K/Ai-Code-Review-Test-Repo"
pr_number = 1

files = api.get_pr_files(repo, pr_number)
print(f"Found {len(files)} changed files")
for file in files:
    print(f"- {file['filename']}")
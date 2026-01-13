from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib
from .github_api import GitHubAPI
from .llm_analyzer_lmstudio import CodeAnalyzer
from .config import WEBHOOK_SECRET

app = FastAPI(title="AI Code Reviewer")
github_api = GitHubAPI()
analyzer = CodeAnalyzer()

@app.get("/")
def read_root():
    return {"message": "AI Code Reviewer is running!", "version": "1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/webhook")
async def handle_webhook(request: Request):
    """Handle GitHub webhook events"""
    
    # Verify webhook signature (security)
    signature = request.headers.get("X-Hub-Signature-256")
    if not verify_signature(await request.body(), signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    payload = await request.json()
    
    # Only handle PR events
    if "pull_request" not in payload:
        return {"message": "Event ignored"}
    
    pr = payload["pull_request"]
    action = payload["action"]
    
    # Only review when PR is opened or synchronized (new commits)
    if action not in ["opened", "synchronize"]:
        return {"message": "Action ignored"}
    
    # Extract details
    repo = payload["repository"]["full_name"]
    pr_number = pr["number"]
    
    # Get changed files
    files = github_api.get_pr_files(repo, pr_number)
    
    # Analyze each file
    reviews = {}
    for file in files[:5]:  # Limit to 5 files for now
        filename = file["filename"]
        patch = file.get("patch", "")
        
        if patch:  # Only review files with changes
            review = analyzer.analyze_code(patch, filename)
            reviews[filename] = review
    
    # Post review
    if reviews:
        comment = analyzer.format_review(reviews)
        github_api.post_comment(repo, pr_number, comment)
    
    return {"message": "Review posted", "files_reviewed": len(reviews)}

def verify_signature(payload_body, signature_header):
    """Verify GitHub webhook signature"""
    if not signature_header:
        return False
    
    hash_object = hmac.new(
        WEBHOOK_SECRET.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)
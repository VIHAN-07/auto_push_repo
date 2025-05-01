from dotenv import load_dotenv
import os
import subprocess
from datetime import datetime

# Load environment (Render or local .env)
load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
REPO_NAME       = os.getenv("REPO_NAME")
TOKEN           = os.getenv("GITHUB_TOKEN")
BRANCH          = os.getenv("GIT_BRANCH", "main")

# Validate essential variables
if not all([GITHUB_USERNAME, REPO_NAME, TOKEN]):
    raise EnvironmentError("GITHUB_USERNAME, REPO_NAME, and GITHUB_TOKEN must be set")

def run(cmd):
    subprocess.run(cmd, check=True)

def sync_remote():
    """
    Fetch the remote branch and reset local working copy
    so we always start from the latest commit.
    """
    repo_url = f"https://{GITHUB_USERNAME}:{TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    # Fetch only the target branch
    run(["git", "fetch", repo_url, BRANCH])
    # Reset the working directory to match remote
    run(["git", "reset", "--mixed", "FETCH_HEAD"])

def update_readme():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("README.md", "a") as f:
        f.write(f"\nUpdated on {now}")

def commit_and_push():
    repo_url = f"https://{GITHUB_USERNAME}:{TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    # Configure identity
    run(["git", "config", "user.name", "Auto Bot"])
    run(["git", "config", "user.email", "bot@example.com"])
    # Stage and commit
    run(["git", "add", "README.md"])
    run(["git", "commit", "-m", "Automated README update"])
    # Push HEAD to main
    run(["git", "push", repo_url, f"HEAD:{BRANCH}"])

if __name__ == "__main__":
    sync_remote()
    update_readme()
    commit_and_push()

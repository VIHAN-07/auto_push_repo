from dotenv import load_dotenv
import os
import subprocess
from datetime import datetime

# Load environment variables (Render injects these)
load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
REPO_NAME       = os.getenv("REPO_NAME")
TOKEN           = os.getenv("GITHUB_TOKEN")
BRANCH          = os.getenv("GIT_BRANCH", "main")

# Validate
if not all([GITHUB_USERNAME, REPO_NAME, TOKEN]):
    raise EnvironmentError("GITHUB_USERNAME, REPO_NAME, and GITHUB_TOKEN must be set")

def update_readme():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("README.md", "a") as f:
        f.write(f"\nUpdated on {now}")

def push_to_github():
    # Configure Git identity
    subprocess.run(["git", "config", "user.name", "Auto Bot"], check=True)
    subprocess.run(["git", "config", "user.email", "bot@example.com"], check=True)

    # Stage and commit
    subprocess.run(["git", "add", "README.md"], check=True)
    subprocess.run(
        ["git", "commit", "-m", "Automated README update"],
        check=True,
        stderr=subprocess.DEVNULL  # ignore "nothing to commit" message
    )

    # Build the authenticated repo URL
    repo_url = f"https://{GITHUB_USERNAME}:{TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

    # Push current HEAD to your branch
    subprocess.run(
        ["git", "push", repo_url, f"HEAD:{BRANCH}"],
        check=True
    )

if __name__ == "__main__":
    update_readme()
    push_to_github()

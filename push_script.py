from dotenv import load_dotenv
import os
import subprocess
from datetime import datetime

# Load .env (locally) or environment (in Render)
load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
REPO_NAME       = os.getenv("REPO_NAME")
TOKEN           = os.getenv("GITHUB_TOKEN")
BRANCH          = os.getenv("GIT_BRANCH", "main")

if not all([GITHUB_USERNAME, REPO_NAME, TOKEN]):
    raise EnvironmentError("GITHUB_USERNAME, REPO_NAME, and GITHUB_TOKEN must be set")

def update_readme():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("README.md", "a") as f:
        f.write(f"\nUpdated on {now}")

def push_to_github():
    repo_url = f"https://{GITHUB_USERNAME}:{TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

    # 1. Ensure we have the branch locally (reset to match origin)
    subprocess.run(["git", "fetch", "origin"], check=True)
    subprocess.run(
        ["git", "checkout", "-B", BRANCH, f"origin/{BRANCH}"],
        check=True
    )

    # 2. Configure Git identity
    subprocess.run(["git", "config", "user.name", "Auto Bot"], check=True)
    subprocess.run(["git", "config", "user.email", "bot@example.com"], check=True)

    # 3. Stage, commit, and push
    subprocess.run(["git", "add", "README.md"], check=True)
    subprocess.run(["git", "commit", "-m", "Automated README update"], check=True)
    subprocess.run(["git", "push", repo_url, BRANCH], check=True)

if __name__ == "__main__":
    update_readme()
    push_to_github()

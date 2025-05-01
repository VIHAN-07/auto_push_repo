from dotenv import load_dotenv
import os
import subprocess
from datetime import datetime

# Load .env into environment
load_dotenv()

# Read from environment
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
REPO_NAME       = os.getenv("REPO_NAME")
TOKEN           = os.getenv("GITHUB_TOKEN")

if not all([GITHUB_USERNAME, REPO_NAME, TOKEN]):
    raise EnvironmentError("GITHUB_USERNAME, REPO_NAME, and GITHUB_TOKEN must be set in .env")

def update_readme():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("README.md", "a") as f:
        f.write(f"\nUpdated on {now}")

def push_to_github():
    # Configure git author
    subprocess.run(["git", "config", "user.name", "Auto Bot"], check=True)
    subprocess.run(["git", "config", "user.email", "bot@example.com"], check=True)

    # Stage & commit
    subprocess.run(["git", "add", "README.md"], check=True)
    subprocess.run(["git", "commit", "-m", "Automated README update"], check=True)

    # Build authenticated remote URL
    repo_url = f"https://{GITHUB_USERNAME}:{TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    subprocess.run(["git", "push", repo_url], check=True)

if __name__ == "__main__":
    update_readme()
    push_to_github()

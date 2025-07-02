import os
import requests
import json

ORG = os.environ['ORG_NAME']
REPO = os.environ['REPO_NAME']
TOKEN = os.environ['GITHUB_TOKEN']
HEADERS = {'Authorization': f'token {TOKEN}'}
MEMBERS_FILE = '.github/scripts/members.json'

def get_members():
    url = f"https://api.github.com/orgs/{ORG}/members?per_page=100"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return [m["login"] for m in r.json()]

def load_previous():
    if os.path.exists(MEMBERS_FILE):
        with open(MEMBERS_FILE) as f:
            return json.load(f)
    return []

def save_members(members):
    with open(MEMBERS_FILE, 'w') as f:
        json.dump(members, f)

def create_issue(username):
    url = f"https://api.github.com/repos/{ORG}/{REPO}/issues"
    issue = {
        "title": f" Welcome @{username}!",
        "body": f"Hi @{username}, welcome to the organization! 🎊\n\nLet us know if you need anything to get started."
    }
    r = requests.post(url, headers={**HEADERS, "Accept": "application/vnd.github+json"}, json=issue)
    if r.status_code == 201:
        print(f"Issue created for {username}")
    else:
        print(f"Failed to create issue for {username}: {r.text}")

def main():
    current_members = get_members()
    previous_members = load_previous()
    new_members = list(set(current_members) - set(previous_members))

    if new_members:
        print(f"New members: {new_members}")
        for user in new_members:
            create_issue(user)
    else:
        print("No new members")

    save_members(current_members)

if __name__ == "__main__":
    main()

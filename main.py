import httpx
import os
import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description="Backup GitHub repositories.")
    parser.add_argument(
        "--path",
        default=os.getcwd(),
        help="The base path for the backup directory. If --name is not provided, this will be the full path to the backup directory.",
    )
    parser.add_argument(
        "--name",
        help="The name of the backup directory. If not provided, the --path argument will be treated as the full path to the backup directory.",
    )
    parser.add_argument("--token", help="GitHub personal access token.")
    args = parser.parse_args()

    gh_token = args.token

    if not gh_token:
        print("GitHub token is required. Provide it via --token argument.")
        return

    headers = {
        "Authorization": f"Bearer {gh_token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github+json",
    }

    URL = "https://api.github.com/user/repos?per_page=100"

    try:
        result = []
        while URL:
            response = httpx.get(URL, headers=headers)
            response.raise_for_status()
            result.extend(response.json())
            URL = response.links.get("next", {}).get("url")

            if args.name:
                backup_dir = os.path.join(args.path, args.name)
            else:
                # If no name is provided, and path is default, use a default name.
                # Otherwise, path is the full backup directory.
                if args.path == os.getcwd():
                    backup_dir = os.path.join(args.path, "gh-backup")
                else:
                    backup_dir = args.path
            os.makedirs(backup_dir, exist_ok=True)
        for repo in result:
            repo_name = repo["name"]
            repo_url = repo["clone_url"]
            repo_path = os.path.join(backup_dir, f"{repo_name}")

            if os.path.exists(repo_path):
                print(f"Updating {repo_name}...")
                subprocess.run(["git", "remote", "update"], cwd=repo_path, check=True)
            else:
                print(f"Cloning {repo_name}...")
                subprocess.run(
                    ["git", "clone", "--mirror", repo_url, repo_path],
                    cwd=backup_dir,
                    check=True,
                )
    except httpx.HTTPStatusError as e:
        print(f"Error: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"An error occurred while requesting: {e}")
    except subprocess.CalledProcessError as e:
        print(f"A git command failed: {e}")
    except Exception as e:
        print(f"Unknown ISSUE: {e}")


if __name__ == "__main__":
    main()

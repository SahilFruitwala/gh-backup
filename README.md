# GitHub Backup Tool

This script backs up all of a user's GitHub repositories.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/gh-backup.git
    cd gh-backup
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Get a GitHub Personal Access Token:**
    You need to create a GitHub personal access token with the `repo` scope. You can create one [here](https://github.com/settings/tokens).

2.  **Run the script:**
    Execute the script from your terminal, providing your GitHub token and desired backup location.

    ```bash
    python3 main.py --token YOUR_GITHUB_TOKEN [OPTIONS]
    ```

### CLI Arguments

*   `--token TOKEN`: **(Required)** Your GitHub personal access token.
*   `--path PATH`: The base path for the backup directory. If `--name` is not provided, this will be the full path to the backup directory. Defaults to the current directory.
*   `--name NAME`: The name of the backup directory. If not provided, the `--path` argument will be treated as the full path to the backup directory.

### Examples

*   **Backup to a `gh-backup` directory in the current folder:**
    ```bash
    python3 main.py --token YOUR_GITHUB_TOKEN
    ```

*   **Backup to a specific directory:**
    ```bash
    python3 main.py --token YOUR_GITHUB_TOKEN --path /path/to/your/backups
    ```

*   **Backup to a specific directory with a custom name:**
    ```bash
    python3 main.py --token YOUR_GITHUB_TOKEN --path /path/to/your/backups --name my-gh-backup
    ```
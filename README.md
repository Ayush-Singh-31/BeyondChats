# Reddit Persona Generator

A command-line tool that fetches a Reddit user’s recent posts/comments, prompts an LLM to generate a detailed persona based on that history, and outputs the result to a text file with citations.

## Prerequisites

- Python 3.8 or higher
- A Reddit API application (to obtain `client_id`, `client_secret`, and `user_agent`)
- An OpenAI API key

## Installation

1. Clone this repository or download `Main.py`.
2. (Optional) Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required packages:

   ```bash
   pip install praw openai
   ```

## Configuration

The script reads credentials from environment variables. Set the following in your shell:

```bash
export REDDIT_CLIENT_ID="your_reddit_client_id"
export REDDIT_CLIENT_SECRET="your_reddit_client_secret"
export REDDIT_USER_AGENT="your_app_user_agent"
export OPENAI_API_KEY="your_openai_api_key"
```

## Usage

```bash
python3 Main.py <reddit_user_url> [--limit N] [--output FILENAME]
```

- `<reddit_user_url>`: Full URL to the user profile (supports both `/user/` and `/u/` formats).
- `--limit N`: (Optional) Maximum number of submissions/comments to fetch (default: 100).
- `--output FILENAME`: (Optional) Path to write the generated persona (default: `<username>_persona.txt`).

### Example

Fetch up to 200 items from `kojied`’s history and write to `kojied_persona.txt`:

```bash
python3 Main.py https://reddit.com/user/kojied --limit 200 --output kojied_persona.txt
```

## Features & Notes

- **Robust URL parsing**: Supports both `reddit.com/user/` and `reddit.com/u/` URL formats.
- **Citation enforcement**: Verifies that each characteristic in the persona has an associated source URL.
- **Retry logic**: Implements exponential backoff for Reddit API rate limits and network errors.
- **Content validation**: Ensures sufficient data before calling the LLM.
- **Extensible design**: Easily swap in a different LLM or adapt to other social platforms.

## Contribution

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for details.

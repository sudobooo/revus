# Revus

## What's Revus?

Revus is an automated pull request (PR) review application that uses large language models (LLMs) to streamline and standardize code reviews.

## Install

```bash
pipx install revus
```

## Setup

Create a configuration file called `revus.toml` with the following parameters:

- `OPENAI_API_KEY` - your OpenAI API key, available [here](https://platform.openai.com/).
- `model_name` - any available OpenAI model (default is gpt-4o-mini).
- `file_types` - specify file types for the application to read using an array of strings (default is [“.py”]).
- `language` - specify the language for review content (default is English).
- `exclude_paths` - files or paths the application should ignore.
- `custom_rules`- custom rules for review, if needed.

## Usage

To review changes with Revus, first add modified files to staging:
```bash
git add <file_name>
```
or add all files:
```bash
git add .
```
Then, run the application in the project folder:
```bash
revus
```

**Important**: Revus reviews each file individually, simplifying context management.

*New features will be added soon.*

## Additional Notes

This project is in active development, currently in alpha, and may have limited or experimental features.

### Contacts

For issues or suggestions, reach out on [Telegram](https://t.me/serge_masiutin) or [Linkedin](https://www.linkedin.com/in/serge-masiutin/).

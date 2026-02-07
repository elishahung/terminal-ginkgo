# AI Terminal

A blazing-fast, lightweight command-line helper that translates natural language into shell commands.

> If you're like me — you don't trust AI to do your work, but your brain is too small to remember all those commands.

## Why AI Terminal?

I originally used `claude -p` and `gemini` CLI tools, but they were just **too slow** to start up.

All I wanted was to quickly get an `ffmpeg` command or `grep` something — simple tasks that shouldn't require waiting.

I discovered that **Gemini 2.5 Flash Lite** is more than capable for these use cases. Plus, by using raw HTTP requests instead of the heavy `google-genai` SDK, the cold start time is dramatically reduced.

After building with Nuitka and adding the executable to PATH, you can simply:

```bash
ai ffmpeg get first 10s of mp4, no transcode
```
```
ffmpeg -i input.mp4 -c copy -t 10 output.mp4
```

Or:

```bash
ai ytdlp https://www.youtube.com/watch?v=xxxxx mp3 only
```
```
yt-dlp -x --audio-format mp3 https://www.youtube.com/watch?v=xxxxx
```

**Lightning fast response. No waiting.**

## Features

- ⚡ **Instant startup** — No heavy SDK, just pure HTTP requests to Gemini API
- 🐚 **Shell-aware** — Auto-detects your shell (cmd, PowerShell, Bash, Zsh, Fish) and generates appropriate commands
- 📋 **Auto-paste** — LLM Response is automatically pasted to your terminal

## Installation

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- A [Google Gemini API key](https://ai.google.dev/)

### Build

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-terminal.git
cd ai-terminal

# Install dependencies
uv sync

# Build the executable
build.bat
```

The compiled `ai.exe` will be in the `dist/` folder.

### Setup

1. Add the `dist/` folder to your system PATH (or copy `ai.exe` to a folder already in PATH)

2. Set your API key as an environment variable:
   ```bash
   # Windows (cmd)
   setx AI_TERMINAL_API_KEY "your-api-key-here"
   
   # Or use GEMINI_API_KEY
   setx GEMINI_API_KEY "your-api-key-here"
   ```

3. Restart your terminal

## Usage

```bash
ai <your request in natural language>
```

## Project Structure

```
ai-terminal/
├── main.py          # Entry point
├── gemini.py        # Gemini API client (using raw requests)
├── instruction.py   # System prompts for different shells
├── settings.py      # Environment variable handling
├── spinner.py       # Loading spinner animation
├── clipboard.py     # Copy & paste functionality
├── build.bat        # Nuitka build script
└── dist/
    └── ai.exe       # Compiled executable
```

## Configuration

| Environment Variable | Description |
|---------------------|-------------|
| `AI_TERMINAL_API_KEY` | Your Gemini API key (primary) |
| `GEMINI_API_KEY` | Your Gemini API key (fallback) |

## How It Works

1. User types `ai <request>`
2. The tool detects your current shell type (cmd, PowerShell, Bash, etc.)
3. Sends request to Gemini 2.5 Flash Lite with shell-specific system prompt
4. Receives command response
5. Auto-copies and pastes the command to your terminal

## License

MIT

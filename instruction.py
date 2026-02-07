import os
import platform


def get_parent_process_name() -> str:
    """
    Get the name of the parent process.

    Returns:
        str: Parent process name (lowercase), or empty string if unavailable
    """
    try:
        import psutil
        parent = psutil.Process(os.getpid()).parent()
        if parent:
            # May need to look further up, as Python's parent might be another wrapper
            parent_name = parent.name().lower()
            # If parent is python, look one level higher
            if "python" in parent_name:
                grandparent = parent.parent()
                if grandparent:
                    return grandparent.name().lower()
            return parent_name
    except ImportError:
        pass
    except Exception:
        pass
    return ""


def detect_shell() -> str:
    """
    Dynamically detect the current shell type.

    Uses parent process detection (more accurate) with environment variable fallback.

    Returns:
        str: 'cmd', 'powershell', 'bash', 'zsh', 'fish', or 'unknown'
    """
    # Method 1: Detect via parent process (most accurate)
    parent_name = get_parent_process_name()
    if parent_name:
        if "powershell" in parent_name or "pwsh" in parent_name:
            return "powershell"
        elif "cmd" in parent_name:
            return "cmd"
        elif "bash" in parent_name:
            return "bash"
        elif "zsh" in parent_name:
            return "zsh"
        elif "fish" in parent_name:
            return "fish"

    # Method 2: Detect via environment variables (fallback)
    # Check SHELL environment variable (Unix-like systems)
    shell_env = os.environ.get("SHELL", "")

    # Check Unix shells
    if shell_env:
        shell_name = os.path.basename(shell_env).lower()
        if "bash" in shell_name:
            return "bash"
        elif "zsh" in shell_name:
            return "zsh"
        elif "fish" in shell_name:
            return "fish"
        elif "sh" in shell_name:
            return "bash"  # Default to bash-compatible commands

    # Windows default detection
    if platform.system() == "Windows":
        # Check if running in Git Bash or WSL
        if os.environ.get("MSYSTEM"):  # Git Bash
            return "bash"
        if os.environ.get("WSL_DISTRO_NAME"):  # WSL
            return "bash"
        # Windows defaults to cmd
        return "cmd"

    # Other Unix-like systems default to bash
    return "bash"


# =============================================================================
# System Prompt Modular Configuration
# =============================================================================

# Common base rules
BASE_RULES = """Rules:
- Only respond with plain text single-line commands
- Do not use JSON, Markdown, or any formatting
- If the command contains parts the user needs to replace, use obvious placeholders like input.mp4, output.mp4, etc.
- If really necessary, you may add a brief explanation"""

# Shell-specific configurations
SHELL_CONFIGS = {
    "cmd": {
        "name": "Windows cmd.exe",
        "context": "Windows Terminal",
        "syntax_rules": "- Do not use PowerShell or bash-specific syntax, only use cmd.exe compatible commands",
    },
    "powershell": {
        "name": "PowerShell",
        "context": "PowerShell",
        "syntax_rules": "- Use native PowerShell syntax and cmdlets (e.g., Get-ChildItem, ForEach-Object, etc.)",
    },
    "bash": {
        "name": "Bash",
        "context": "Bash shell",
        "syntax_rules": "- Use standard Unix/Linux commands and Bash syntax",
    },
    "zsh": {
        "name": "Zsh",
        "context": "Zsh shell",
        "syntax_rules": "- Use standard Unix/Linux commands, may use Zsh-specific syntax (e.g., glob expansion)",
    },
    "fish": {
        "name": "Fish",
        "context": "Fish shell",
        "syntax_rules": "- Use Fish syntax (e.g., set instead of export, use ; instead of && to chain commands)",
    },
}


def build_system_prompt(shell_type: str) -> str:
    """
    Build system prompt dynamically based on shell type.

    Args:
        shell_type: Shell type ('cmd', 'powershell', 'bash', 'zsh', 'fish')

    Returns:
        str: Assembled system prompt
    """
    config = SHELL_CONFIGS.get(shell_type, SHELL_CONFIGS["bash"])

    return f"""You are a command-line assistant. The user will ask questions in very brief phrases within {config['context']}. Respond with commands that can be directly executed in {config['name']}.

{BASE_RULES}
{config['syntax_rules']}"""


# Convenient direct import
SYSTEM_PROMPT = build_system_prompt(detect_shell())


if __name__ == "__main__":
    # Test: Display detection results
    shell = detect_shell()
    print(f"Detected shell: {shell}")
    print(f"SYSTEM_PROMPT first 50 chars: {SYSTEM_PROMPT[:50]}...")
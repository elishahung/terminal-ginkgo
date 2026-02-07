import os
import platform


def get_parent_process_name() -> str:
    """
    取得父程序的名稱。
    
    Returns:
        str: 父程序名稱（小寫），如果無法取得則回傳空字串
    """
    try:
        import psutil
        parent = psutil.Process(os.getpid()).parent()
        if parent:
            # 可能需要往上找，因為 Python 的父程序可能是另一個 Python 或包裝程式
            parent_name = parent.name().lower()
            # 如果父程序是 python，再往上找
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
    動態偵測目前使用的 shell 類型。
    
    優先使用父程序偵測（較準確），fallback 到環境變數檢查。
    
    Returns:
        str: 'cmd', 'powershell', 'bash', 'zsh', 'fish', 或 'unknown'
    """
    # 方法 1: 透過父程序偵測（最準確）
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
    
    # 方法 2: 透過環境變數偵測（fallback）
    # 檢查 SHELL 環境變數 (Unix-like 系統)
    shell_env = os.environ.get("SHELL", "")
    
    # 檢查 Unix shell
    if shell_env:
        shell_name = os.path.basename(shell_env).lower()
        if "bash" in shell_name:
            return "bash"
        elif "zsh" in shell_name:
            return "zsh"
        elif "fish" in shell_name:
            return "fish"
        elif "sh" in shell_name:
            return "bash"  # 預設使用 bash 相容指令
    
    # Windows 預設檢查
    if platform.system() == "Windows":
        # 檢查是否在 Git Bash 或 WSL 中
        if os.environ.get("MSYSTEM"):  # Git Bash
            return "bash"
        if os.environ.get("WSL_DISTRO_NAME"):  # WSL
            return "bash"
        # Windows 預設使用 cmd
        return "cmd"
    
    # 其他 Unix-like 系統預設使用 bash
    return "bash"


# =============================================================================
# 系統提示詞模組化配置
# =============================================================================

# 共同的基礎規則
BASE_RULES = """規則：
- 只回答純文字單行指令
- 不要使用 JSON、Markdown 或任何格式化
- 如果指令包含使用者需要替換的部分，用明顯的佔位符如 input.mp4、output.mp4 等
- 如果真的需要，可以加上簡短的解釋"""

# 各 Shell 的特定配置
SHELL_CONFIGS = {
    "cmd": {
        "name": "Windows cmd.exe",
        "context": "Windows Terminal",
        "syntax_rules": "- 不要使用 PowerShell 或 bash 專屬語法，只能用 cmd.exe 相容的指令",
    },
    "powershell": {
        "name": "PowerShell",
        "context": "PowerShell",
        "syntax_rules": "- 使用 PowerShell 原生語法和 cmdlet（如 Get-ChildItem、ForEach-Object 等）",
    },
    "bash": {
        "name": "Bash",
        "context": "Bash shell",
        "syntax_rules": "- 使用標準的 Unix/Linux 指令和 Bash 語法",
    },
    "zsh": {
        "name": "Zsh",
        "context": "Zsh shell",
        "syntax_rules": "- 使用標準的 Unix/Linux 指令，可以使用 Zsh 特有語法（如 glob 擴展）",
    },
    "fish": {
        "name": "Fish",
        "context": "Fish shell",
        "syntax_rules": "- 使用 Fish 語法（如 set 而非 export，使用 ; 而非 && 連接指令）",
    },
}


def build_system_prompt(shell_type: str) -> str:
    """
    根據 shell 類型動態組裝系統提示詞。
    
    Args:
        shell_type: shell 類型 ('cmd', 'powershell', 'bash', 'zsh', 'fish')
    
    Returns:
        str: 組裝好的系統提示詞
    """
    config = SHELL_CONFIGS.get(shell_type, SHELL_CONFIGS["bash"])
    
    return f"""你是一個命令列助手。使用者會在 {config['context']} 中用非常簡短的方式問問題，請你回答可以直接在 {config['name']} 執行的指令。

{BASE_RULES}
{config['syntax_rules']}"""


# 方便直接 import 使用
SYSTEM_PROMPT = build_system_prompt(detect_shell())


if __name__ == "__main__":
    # 測試用：顯示偵測結果
    shell = detect_shell()
    print(f"偵測到的 Shell: {shell}")
    print(f"使用的 SYSTEM_PROMPT 前 50 字元: {SYSTEM_PROMPT[:50]}...")
    
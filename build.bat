uv run python -m nuitka ^
  --onefile ^
  --onefile-tempdir-spec="{CACHE_DIR}/ai-terminal" ^
  --output-dir=dist ^
  --remove-output ^
  --lto=yes ^
  src/main.py ^
  -o ai.exe

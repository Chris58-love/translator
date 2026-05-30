# one_click_start_auto.py
# Python 3.9 compatible version

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path
from typing import Optional


PROJECT_ROOT = Path(__file__).resolve().parent
VENV_DIR = PROJECT_ROOT / ".venv"
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
ENV_FILE = PROJECT_ROOT / ".env"
ENV_TEMPLATE_FILE = PROJECT_ROOT / ".env.template"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"

BACKEND_HOST = "0.0.0.0"
BACKEND_PORT = "8000"
FRONTEND_PORT = "5500"
FRONTEND_URL = f"http://127.0.0.1:{FRONTEND_PORT}/"

PIP_INDEX_URL = "https://pypi.tuna.tsinghua.edu.cn/simple"


def print_header() -> None:
    print("=" * 60)
    print("Realtime Interpreter - One Click Launcher")
    print("=" * 60)
    print(f"Project root: {PROJECT_ROOT}")
    print()


def read_env_file() -> dict:
    env_data = {}

    if not ENV_FILE.exists():
        return env_data

    try:
        lines = ENV_FILE.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        lines = ENV_FILE.read_text(encoding="utf-8-sig").splitlines()

    for line in lines:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        env_data[key.strip()] = value.strip()

    return env_data


def validate_project_structure() -> None:
    missing_items = []

    if not BACKEND_DIR.exists():
        missing_items.append("backend folder")

    if not FRONTEND_DIR.exists():
        missing_items.append("frontend folder")

    if not REQUIREMENTS_FILE.exists():
        missing_items.append("requirements.txt")

    if missing_items:
        print("[ERROR] Project structure is incomplete:")
        for item in missing_items:
            print(f"  - Missing: {item}")
        print()
        print("Please make sure this script is placed in the project root directory.")
        sys.exit(1)


def validate_env_file() -> None:
    if not ENV_FILE.exists():
        print("[ERROR] .env file not found.")
        print()

        if ENV_TEMPLATE_FILE.exists():
            print("Please copy .env.template to .env, then fill in your DeepSeek API key.")
            print("Example:")
            print("  copy .env.template .env")
        else:
            print("Please create a .env file in the project root directory.")
            print("Required example:")
            print("  DEEPSEEK_API_KEY=your_deepseek_api_key_here")
            print("  DEEPSEEK_BASE_URL=https://api.deepseek.com")
            print("  DEEPSEEK_MODEL=deepseek-chat")

        print()
        sys.exit(1)

    env_data = read_env_file()
    api_key = env_data.get("DEEPSEEK_API_KEY", "").strip()

    if not api_key:
        print("[ERROR] DEEPSEEK_API_KEY is empty in .env.")
        print("Please open .env and fill in your DeepSeek API key.")
        print()
        sys.exit(1)

    if api_key == "your_deepseek_api_key_here":
        print("[ERROR] DEEPSEEK_API_KEY is still a placeholder.")
        print("Please replace it with your real DeepSeek API key in .env.")
        print()
        sys.exit(1)


def print_runtime_config() -> None:
    env_data = read_env_file()

    network_mode = env_data.get("DEEPSEEK_NETWORK_MODE", "auto")
    proxy = env_data.get("DEEPSEEK_PROXY", "")
    stream_enabled = env_data.get("DEEPSEEK_STREAM_ENABLED", "false")
    model = env_data.get("DEEPSEEK_MODEL", "deepseek-chat")

    print("Runtime configuration:")
    print(f"  DEEPSEEK_MODEL: {model}")
    print(f"  DEEPSEEK_NETWORK_MODE: {network_mode}")
    print(f"  DEEPSEEK_STREAM_ENABLED: {stream_enabled}")

    if proxy:
        print("  DEEPSEEK_PROXY: configured")
    else:
        print("  DEEPSEEK_PROXY: not configured")

    print()

    if network_mode.lower() == "proxy" and not proxy:
        print("[WARNING] DEEPSEEK_NETWORK_MODE is proxy, but DEEPSEEK_PROXY is empty.")
        print("          If you use Clash/Mihomo, set for example:")
        print("          DEEPSEEK_PROXY=http://127.0.0.1:7897")
        print()

    if network_mode.lower() == "auto":
        print("Network mode auto: direct connection will be tried first, then proxy if configured.")
        print()

    print("If you use Clash/Mihomo, make sure DEEPSEEK_PROXY matches the mixed proxy port.")
    print("Example: DEEPSEEK_PROXY=http://127.0.0.1:7897")
    print()


def clean_proxy_env_for_launcher() -> None:
    """
    Only remove system proxy variables from the launcher process environment.
    This does NOT modify the .env file.

    DeepSeek dedicated proxy should be configured in .env as DEEPSEEK_PROXY.
    """
    proxy_keys = [
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "http_proxy",
        "https_proxy",
        "ALL_PROXY",
        "all_proxy",
    ]

    for key in proxy_keys:
        os.environ.pop(key, None)

    print("System proxy environment variables cleaned for launcher process.")
    print("DeepSeek dedicated proxy from .env will not be modified.")
    print()


def create_venv() -> None:
    if VENV_DIR.exists():
        print(".venv already exists. Skip creating virtual environment.")
        return

    print("Creating virtual environment .venv ...")
    subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
    print("Virtual environment created.")
    print()


def get_python_exe() -> Path:
    if os.name == "nt":
        python_exe = VENV_DIR / "Scripts" / "python.exe"
    else:
        python_exe = VENV_DIR / "bin" / "python"

    if not python_exe.exists():
        print("[ERROR] Python executable not found in virtual environment.")
        print(f"Expected path: {python_exe}")
        sys.exit(1)

    return python_exe


def upgrade_pip() -> None:
    python_exe = get_python_exe()

    print("Checking pip ...")
    cmd = [
        str(python_exe),
        "-m",
        "pip",
        "install",
        "--upgrade",
        "pip",
        "-i",
        PIP_INDEX_URL,
        "--trusted-host",
        "pypi.tuna.tsinghua.edu.cn",
        "--disable-pip-version-check",
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("[WARNING] Failed to upgrade pip. Continue installing requirements.")
    print()


def install_requirements() -> None:
    if not REQUIREMENTS_FILE.exists():
        print("[ERROR] requirements.txt not found.")
        sys.exit(1)

    python_exe = get_python_exe()

    print("Installing requirements ...")
    cmd = [
        str(python_exe),
        "-m",
        "pip",
        "install",
        "-r",
        str(REQUIREMENTS_FILE),
        "-i",
        PIP_INDEX_URL,
        "--trusted-host",
        "pypi.tuna.tsinghua.edu.cn",
        "--trusted-host",
        "pypi.org",
        "--trusted-host",
        "files.pythonhosted.org",
        "--disable-pip-version-check",
    ]

    subprocess.run(cmd, check=True)

    print("Requirements installed.")
    print()


def start_backend() -> subprocess.Popen:
    python_exe = get_python_exe()

    print(f"Starting backend: http://127.0.0.1:{BACKEND_PORT}")

    backend_cmd = [
        str(python_exe),
        "-m",
        "uvicorn",
        "main:app",
        "--reload",
        "--host",
        BACKEND_HOST,
        "--port",
        BACKEND_PORT,
    ]

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    process = subprocess.Popen(
        backend_cmd,
        cwd=str(BACKEND_DIR),
        env=env,
    )

    return process


def start_frontend() -> subprocess.Popen:
    python_exe = get_python_exe()

    print(f"Starting frontend: http://127.0.0.1:{FRONTEND_PORT}")

    frontend_cmd = [
        str(python_exe),
        "-m",
        "http.server",
        FRONTEND_PORT,
    ]

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    process = subprocess.Popen(
        frontend_cmd,
        cwd=str(FRONTEND_DIR),
        env=env,
    )

    return process


def open_browser() -> None:
    time.sleep(2)
    webbrowser.open(FRONTEND_URL)
    print(f"Browser opened: {FRONTEND_URL}")
    print()


def terminate_process(process: Optional[subprocess.Popen], name: str) -> None:
    if process is None:
        return

    try:
        if process.poll() is None:
            print(f"Stopping {name} ...")
            process.terminate()

            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print(f"{name} did not stop in time. Killing it ...")
                process.kill()

    except Exception as exc:
        print(f"[WARNING] Failed to stop {name}: {exc}")


def wait_for_processes(
    backend_process: subprocess.Popen,
    frontend_process: subprocess.Popen,
) -> None:
    print("Project started.")
    print()
    print("Open page:")
    print(f"  {FRONTEND_URL}")
    print()
    print("Backend check:")
    print(f"  http://127.0.0.1:{BACKEND_PORT}/health")
    print(f"  http://127.0.0.1:{BACKEND_PORT}/config-check")
    print(f"  http://127.0.0.1:{BACKEND_PORT}/deepseek-health?refresh=true")
    print()
    print("Press Ctrl+C in this window to stop services.")
    print()

    try:
        while True:
            backend_status = backend_process.poll()
            frontend_status = frontend_process.poll()

            if backend_status is not None:
                print(f"[ERROR] Backend process exited with code {backend_status}.")
                break

            if frontend_status is not None:
                print(f"[ERROR] Frontend process exited with code {frontend_status}.")
                break

            time.sleep(1)

    except KeyboardInterrupt:
        print()
        print("Ctrl+C received. Stopping services ...")

    finally:
        terminate_process(backend_process, "backend")
        terminate_process(frontend_process, "frontend")
        print("Services stopped.")


def main() -> None:
    os.chdir(PROJECT_ROOT)

    print_header()
    validate_project_structure()
    validate_env_file()
    print_runtime_config()

    clean_proxy_env_for_launcher()
    create_venv()
    upgrade_pip()
    install_requirements()

    backend_process = None
    frontend_process = None

    try:
        backend_process = start_backend()
        time.sleep(1)
        frontend_process = start_frontend()
        open_browser()
        wait_for_processes(backend_process, frontend_process)

    except subprocess.CalledProcessError as exc:
        print()
        print("[ERROR] Command failed.")
        print(f"Return code: {exc.returncode}")
        print()

        terminate_process(backend_process, "backend")
        terminate_process(frontend_process, "frontend")
        sys.exit(exc.returncode)

    except Exception as exc:
        print()
        print("[ERROR] Project failed to start.")
        print(f"{type(exc).__name__}: {exc}")
        print()

        terminate_process(backend_process, "backend")
        terminate_process(frontend_process, "frontend")
        sys.exit(1)


if __name__ == "__main__":
    main()
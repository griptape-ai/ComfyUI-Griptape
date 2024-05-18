import importlib.util
import subprocess
import sys


def is_playwright_installed():
    package_name = "playwright"
    spec = importlib.util.find_spec(package_name)
    return spec is not None


def install_playwright():
    try:
        # Upgrade pip
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"]
        )
        # Install Playwright package
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
        # Install Playwright browsers
        subprocess.check_call(["playwright", "install"])
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing Playwright: {e}")
        sys.exit(1)


def main():
    if not is_playwright_installed():
        print("Playwright is not installed. Installing now...")
        install_playwright()
        print("Playwright has been successfully installed.")
    else:
        print("Playwright is already installed.")


if __name__ == "__main__":
    main()

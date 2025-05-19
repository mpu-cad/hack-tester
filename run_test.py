import subprocess

def run_test():
    subprocess.run([
        "locust",
        "-f", "tester.py",
        "--host", "http://localhost:8000",
        "--headless",
        "-u", "1000",
        "-r", "1000000",
        "-t", "1m",
        "--only-summary"
    ])

if __name__ == "__main__":
    run_test()
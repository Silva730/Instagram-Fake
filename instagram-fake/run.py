import subprocess
import threading
from app import app

def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False)

def run_cloudflared():
    process = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", "http://localhost:5000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    for line in process.stdout:
        if "trycloudflare.com" in line:
            print("\n🌍 Seu link público está pronto:")
            print(line.strip())
            print()
        print(line.strip())

if __name__ == "__main__":
    t1 = threading.Thread(target=run_flask)
    t2 = threading.Thread(target=run_cloudflared)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
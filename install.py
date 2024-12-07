import os

def install():
    os.system("pip install -r requirements.txt")
    os.system("npm ci")
    os.system("npm run build")


if __name__ == "__main__":
    install()
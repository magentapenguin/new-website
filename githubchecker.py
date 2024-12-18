import github, sched, time, os, sys, threading

gh = github.Github()
repo = gh.get_repo("magentapenguin/new-website")

# Check for updates every 5 seconds
def check():
    print("Checking for updates...")
    commits = repo.get_commits()
    latest_commit = commits[0]
    try:
        with open("latest_commit.txt") as f:
            if f.read() == latest_commit.sha:
                print("No updates.")
            else:
                print("New updates found!")
                with open("latest_commit.txt", "w") as f:
                    f.write(latest_commit.sha)
                # Fetch the latest changes
                print("Fetching latest changes...")
                os.system("git pull")
                print("Restarting server...")
                time.sleep(1)
                os.execl(sys.executable, sys.executable, *sys.argv)
    except FileNotFoundError:
        with open("latest_commit.txt", "w") as f:
            f.write(latest_commit.sha)
        print("Initial commit saved.")


def main():
    def _main():
        s = sched.scheduler(time.time, time.sleep)
        while True:
            s.enter(120, 1, check)
            s.run()
    p = threading.Thread(target=_main, daemon=True)
    p.start()

if __name__ == "__main__":
    main()
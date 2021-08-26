from requests import get
from json import loads
from os import system, mkdir, chdir, environ
PAT = environ['PAT'] # requires `export PAT="ghp_************************************"`
users = loads(get("https://api.github.com/search/users?q=followers:>20000").text)["items"]
usernames = [i["login"] for i in users]
name = "20000-followers-plus"
mkdir(name)
chdir(name)
system("git init")
for username in usernames:
    commits = loads(get(f"https://api.github.com/users/{username}/events").text)
    for commit in commits:
        if "payload" in commit:
            payload = commit["payload"]
            if "commits" in payload:
                email = payload["commits"][0]["author"]["email"]
                if username in email or payload["commits"][0]["author"]["name"] == username:
                    break
    else: continue
    system(f"git -c user.name=\"{username}\" -c user.email=\"{email}\" commit --allow-empty -m \"\u200B\"")
system(f"cp ../{__file__} . && git add {__file__} && git commit -m \"main commit\" && git push --set-upstream https://{PAT}@github.com/donno2048/{name}.git master")

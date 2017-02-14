from Hackerrank import Hackerrank
from GitHub import GitHub

hackerrank_completed_challenges = Hackerrank('username', 'password').start_sync()

github = GitHub()

for challenge_name, challenge_file_name in completed_challenges.items():
    github.add_to_hackerrank_git(challenge_file_name,challenge_name)
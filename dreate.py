
from github import Github
from six.moves import urllib
from BeautifulSoup4 import BeautifulSoup

g = Github("9f6e85e68df27dba27afaa5a822e83edb6264911")


# repo = g.get_repo("us/tensorflow-gsoc-proposal")
# repo.create_issue(title="This is a new issue", body="This is the issue body")

# a = urllib.request.urlopen('https://github-trending-api.now.sh/developers?language=python').read()
import requests
response = requests.get('https://github-trending-api.now.sh/developers')
response = response.json()
print(response)
print('===================. == = = = == ')
print(BeautifulSoup(response))

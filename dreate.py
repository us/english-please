
from github import Github
from six.moves import urllib
import pprint
import requests
from langdetect import detect
from bs4 import BeautifulSoup
from markdown import markdown
import re

def markdown_to_text(markdown_string):
    """ Converts a markdown string to plaintext """

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string)

    # remove code snippets
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.findAll(text=True))

    return text



g = Github("761a81080d3e4cb906bc95846c42bf1bd0730535")


repo = g.get_repo("hemreari/easy-comment")
# repo.create_issue(title="This is a new issue", body="This is the issue body")

# a = urllib.request.urlopen('https://github-trending-api.now.sh/developers?language=python').read()
response = requests.get('https://github-trending-api.now.sh/developers')
response = response.json()
#pprint.pprint(response[0]['repo']['description'])

repo_name = response[4]['username'] + '/' + response[4]['repo']['name']
print(repo_name)

#repo = g.get_repo(repo_name)
readme = repo.get_readme().decoded_content
#readme = 'https://raw.githubusercontent.com/{}/master/README.md'.format(repo_name)
readme = markdown_to_text(readme)
md_language = detect(readme)

f=open("issue_body.md", "r")

if md_language == 'en':
	issue = repo.create_issue(title="This is a new issue", body=f.read())
	print(issue, 'Issue created.')


# print(readme)
# print('=========')
print(detect(readme))
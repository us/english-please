from github import Github
import requests
from langdetect import detect
from bs4 import BeautifulSoup
from markdown import markdown
import re

g = Github("")  # github auth token

_issue_template = " - [{repo}](https://github.com/{repo}/issues/{issue_number})\n"


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


def get_trending_as_json():
    response = requests.get('https://github-trending-api.now.sh/developers')
    response = response.json()
    return response


def check_repo_language(repo_name):
    repo = g.get_repo(repo_name)
    readme = repo.get_readme().decoded_content
    readme = markdown_to_text(readme)

    repo_language = detect(readme)
    creating_issue(repo, repo_language)
    print(detect(readme))


def creating_issue(repo, repo_language):
    f = open("issue_body.md", "r", encoding="utf-8")
    issue = ''
    if repo_language == 'en':
        issue = repo.create_issue(title="About sharing knowledge", body=f.read())
        print('Issue created.')
    f.close()
    save_created_issues(repo.full_name, issue.number)


def save_created_issues(repo, issue_number):
    f = open("created_repo_issues.md", "a+")
    f.write(_issue_template.format(repo=repo, issue_number=issue_number))


def main():
    print("python main function")

    for repo in get_trending_as_json():
        repo_name = repo['username'] + '/' + repo['repo']['name']
        print(repo_name)
        check_repo_language(repo_name)


if __name__ == '__main__':
    main()

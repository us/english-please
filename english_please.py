from github import Github, GithubException
import requests
from langdetect import detect
from bs4 import BeautifulSoup
from markdown import markdown
import re

g = Github("")  # github auth token

_issue_template = " - [{repo}](https://github.com/{repo}/issues/{issue_number})\n"


def markdown_to_text(markdown_string):
    """ Cleaning md file to detect method """
    html = markdown(markdown_string)
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)

    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.findAll(text=True))
    return text


def get_trending_as_json():
    """ Get github trending as json from unofficial trending api. """
    response = requests.get('https://github-trending-api.now.sh/')
    response = response.json()
    return response


def check_repo_language(repo_name):
    """Get, clean and check repos README.md language"""
    try:
        repo = g.get_repo(repo_name)
        readme = repo.get_readme().decoded_content
        readme = markdown_to_text(readme)

        repo_language = detect(readme)
        creating_issue(repo, repo_language)
    except GithubException as e:
        print(e, ", issue couldn't created! ",repo_name)
        pass

def creating_issue(repo, repo_language):
    """ Create issue according to README.md language. """
    f = open("issue_body.md", "r", encoding="utf-8")
    created_repos_file = open("created_repo_issues.md", "r", encoding="utf-8")
    created_repos = created_repos_file.read()
    if repo_language != 'en' and repo.full_name not in created_repos:
        try:
            issue = repo.create_issue(title="English Please",
                                      body=f.read())
            print('Issue created in {}.'.format(repo.full_name))
            save_created_issues(repo.full_name, issue.number)
        except:
            print(repo.full_name + ' issue could\'nt opened.')
            pass

    created_repos_file.close()
    f.close()


def save_created_issues(repo, issue_number):
    """ Write created issues to `created_repo_issues.md` """
    with open("created_repo_issues.md", "a+") as f:
        f.write(_issue_template.format(repo=repo, issue_number=issue_number))


def main():
    for repo in get_trending_as_json():
        repo_name = repo['url'][19:]
        check_repo_language(repo_name)


if __name__ == '__main__':
    main()

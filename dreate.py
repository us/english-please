from github import Github
import requests
from langdetect import detect
from bs4 import BeautifulSoup
from markdown import markdown
import re

g = Github("")  # github auth token


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


def check_repo(repo_name):
    repo = g.get_repo(repo_name)
    readme = repo.get_readme().decoded_content
    readme = markdown_to_text(readme)
    md_language = detect(readme)

    f = open("issue_body.md", "r")

    # if md_language == 'en':
    #   #issue = repo.create_issue(title="This is a new issue", body=f.read())
    #   print('Issue created.')
    f.close()
    print(detect(readme))


def main():
    print("python main function")

    for repo in get_trending_as_json():
        repo_name = repo['username'] + '/' + repo['repo']['name']
        print(repo_name)
        check_repo(repo_name)
    print(check_repo('linlinjava/litemall'))

if __name__ == '__main__':
    main()

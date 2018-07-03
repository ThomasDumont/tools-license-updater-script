#!/usr/bin/python3.5
# -*-coding:utf-8 -*

import argparse
import getpass
import xml.etree.ElementTree as ET

import sh

from service import jira_service
from service import github_service

"""
    Update files license headers in all Lutece components on Github
"""

JIRA_URL = "https://dev.lutece.paris.fr/jira/"
GITHUB_PLATFORM = ["lutece-platform", "lutece_secteur-public"]

def main():
    parser = argparse.ArgumentParser(
        description=('Script permettant de mettre à jour les licences sur '
                     + 'tous les composants Lutece dans GitHub')
        )

    parser.add_argument(
        "jira_user",
        help="Votre code d'accès sur Jira"
        )
    parser.add_argument(
        "github_user",
        help="Votre code d'accès sur GitHub"
        )

    args = parser.parse_args()

    jira_user = args.jira_user
    github_user = args.github_user

    jira_password = getpass.getpass(prompt="Mot de passe Jira : ")
    jira_client = jira_service.JiraService(JIRA_URL, jira_user, jira_password)

    github_password = getpass.getpass(prompt="Mot de passe GitHub : ")
    github_client = github_service.GithubService(github_user, github_password)


    for lutece_organization in LUTECE_ORGANIZATIONS
        org = github_client.get_organization(lutece_organization)
        for repo in org.get_repos():
            update_license(github_repo, jira_client, project_key, github_user,
                           github_password)

def update_license(github_repo, jira_client, git_user, git_password):
    """Update license"""
    url = github_repo.clone_url
    name = github_repo.name

    sh.git.clone(url, name)
    sh.cd(name)
    sh.git.checkout("develop")

    sh.mvn("license:format")

    if (sh.git.status("--porcelain") != ""):
        sh.git.add("src/java")
        sh.git.add("src/test/java")

        try:
            issue_key = ""

            tree = ET.parse('pom.xml')
            project = tree.getroot()
            ns = {"mvn": "http://maven.apache.org/POM/4.0.0"}
            properties = project.find("mvn:properties", ns)
            if properties is not None:
                jira_project_name = properties.find('mvn:jiraProjectName', ns)
                if jira_project_name is not None:
                    project_key = jira_project_name.text

                    version = jira_client.get_last_version(project_key)
                    user = jira_client.user
                    issue_key = jira_client.create_issue(project_key,
                                                         "Update license",
                                                         user, "Major", "Task",
                                                         version)
        except FileNotFoundError, ET.ParseError:
            pass

        issue_key += " : " if issue_key else ""
        sh.git.commit("-m", "{}Update license".format(issue_key))

        remote = str(sh.git.remote("get-url", "--push", "origin").replace("\n",
                                                                          ""))
        remote = remote.replace("https://",
                                "https://{}:{}@".format(git_user, git_password))
        sh.git.push(remote, "develop")
        jira_client.close_issue(issue_key)

    sh.cd("..")
    sh.rm("-rf", name)

if __name__ == "__main__":
    main()

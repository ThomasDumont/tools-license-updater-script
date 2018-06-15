#!/usr/bin/python3.5
# -*-coding:utf-8 -*

import github


class GithubService:

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.client = github.Github(user, password)

    def create_github_repo(self, github_platform, name):
        """Complete the GitHub repository from the SVN repository"""

        org = self.client.get_organization(github_platform)
        org.create_repo(name)

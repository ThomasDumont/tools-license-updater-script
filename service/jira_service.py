#!/usr/bin/python3.5
# -*-coding:utf-8 -*

import jira


class JiraService:

    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password
        self.client = jira.JIRA(url, basic_auth=(user, password))

    def create_issue(self, project_key, summary, user, priority, type, version):
        """Create an issue and return its key"""

        fields = {
            "project": {"key": project_key},
            "summary": summary,
            "reporter": {"name": user},
            "assignee": {"name": user},
            "priority": {"name": priority},
            "issuetype": {"name": type},
            "versions": [{"name": version}],
            "fixVersions": [{"name": version}]
            }
        issue = self.client.create_issue(fields=fields)

        return issue.key

    def close_issue(self, issue_key):
        """Close an issue"""

        fields = {
            "resolution": {"name": "Fixed"},
            }
        issue = self.client.issue(issue_key)
        self.client.transition_issue(issue, '5', fields=fields)

    def get_last_version(self, project_key):
        """Get the last version in a project"""
        versions = self.client.project_versions(project_key)
        return versions[-1].name

    def find_issue_key(self, project_key, issue_summary):
        """Find the first issue in the project with the specified summary"""

        issues = self.client.search_issues("project = '{}' AND summary ~ '{}'"
                                           .format(project_key, issue_summary))

        return issues[0].key

    def find_unresolved_issues(self, project_key, before, after):
        """Find the unresolved issues ina project"""

        before = "AND created < '{}'".format(before) if before != "" else ""
        after = "AND created > '{}'".format(after) if after != "" else ""

        issues = self.client.search_issues(("project = '{}' AND "
                                            + "resolution = unresolved "
                                            + "{} {}")
                                           .format(project_key, before, after))
        return issues

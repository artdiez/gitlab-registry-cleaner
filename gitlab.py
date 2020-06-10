import requests
import json
import sys
import configs
import logging


class GitLabRegistry(object):

    # Init GitLab object
    def __init__(self, object):
        self.server = object.server
        self.headers = {'PRIVATE-TOKEN': object.token}
        self.datas = {'name_regex_delete': object.name_regex_delete,
                      'keep_n': object.keep_tags, 'older_than': object.older_tags}
        self.timeout = 3
        self.groups = {}
        self.projects = {}
        self.registries = []
        self.deletedTags = []
        self.tags = []
        logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.info("GitLab registry cleaner started")
        try:
            self.getGroups()
            self.getProjects()
            self.getRegistry()
            self.getTags()
            self.deleteTags()
            self.getDeletedTags()
        except Exception as e:
            logging.error(e)
            sys.exit(e)

    # List GitLab groups
    def getGroups(self):
        logging.info("Getting list GitLab groups...")
        r = requests.get('{}/api/v4/groups/?per_page=1000'.format(
            self.server), headers=self.headers, timeout=self.timeout)
        r.raise_for_status()
        groups_data = json.loads(r.text)
        for _ in groups_data:
            self.groups[_['id']] = _['full_path']
        return self.groups

    # List GitLab projects with container registry
    def getProjects(self):
        logging.info("Getting list GitLab projects...")
        for key in self.groups:
            r = requests.get('{}/api/v4/groups/{}/projects?per_page=1000'.format(
                self.server, key), headers=self.headers, timeout=self.timeout)
            r.raise_for_status()
            projects_data = json.loads(r.text)
            for _ in projects_data:
                if _['container_registry_enabled'] is True:
                    self.projects[_['id']] = _['web_url']
        return self.projects

    # List GitLab registry repositories
    def getRegistry(self):
        logging.info("Getting list GitLab registry repositories...")
        for key in self.projects:
            r = requests.get('{}/api/v4/projects/{}/registry/repositories?per_page=1000'.format(
                self.server, key), headers=self.headers, timeout=self.timeout)
            r.raise_for_status()
            registries_data = json.loads(r.text)
            for _ in registries_data:
                temp_registries = {'project_id': _['project_id'], 'repository_id': _[
                    'id'], 'location': _['location']}
                self.registries.append(temp_registries)
        return self.registries

    # List GitLab registry repositories tags
    def getTags(self):
        logging.info("Getting list GitLab registry repositories tags...")
        self.tags = []
        for i in self.registries:
            r = requests.get('{}/api/v4/projects/{}/registry/repositories/{}/tags?per_page=1000'.format(
                self.server, i['project_id'], i['repository_id']), headers=self.headers, timeout=self.timeout)
            r.raise_for_status()
            tags_data = json.loads(r.text)
            for _ in tags_data:
                temp_tags = {'project_id': i['project_id'], 'repository_id': i['repository_id'], 'tag': _[
                    'name'], 'location': _['location']}
                self.tags.append(temp_tags)
        return self.tags

    # Delete GitLab registry repositories tags
    def deleteTags(self):
        logging.info("Deleting GitLab registry repositories tags...")
        for i in self.registries:
            r = requests.delete('{}/api/v4/projects/{}/registry/repositories/{}/tags'.format(
                self.server, i['project_id'], i['repository_id']), headers=self.headers, data=self.datas, timeout=self.timeout)
            r.raise_for_status()

        orig_tags = self.tags  # List tags before delete
        temp_tags = self.getTags()  # Get list tags after delete

        for _ in orig_tags:
            if _ not in temp_tags:
                self.deletedTags.append(_)

        return self.deletedTags

    # List deleted tags
    def getDeletedTags(self):
        logging.info("Listing GitLab registry repositories deleted tags...")
        for _ in self.deletedTags:
            logging.info('DELETED: ' + _['location'])

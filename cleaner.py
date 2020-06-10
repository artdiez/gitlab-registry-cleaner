import requests
import json
import sys
from configs import Configs
from gitlab import GitLabRegistry


if __name__ == "__main__":

    config = Configs()

    git = GitLabRegistry(config)

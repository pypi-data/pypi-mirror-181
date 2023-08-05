"""
    Owner: CyberSuki (https://github.com/cybersuki)
    Project: Shinigami
    License: BSD 2-Clause
"""

import os, requests

# Logging library
from faye.faye import Faye

class Shinigami():
    """
    Shinigami is an open source Python library allowing the user to generate and build Dockerfiles during runtime
    """

    def __init__(self, lang_os="", version="", build=False):
        self.lang_os = lang_os
        self.version = version
        self.build = build

    def generate_dockerfile(self):
        """
        Generate a Dockerfile your current working directory
        """
        
        try:

            # Queries open source Dockerfile repository
            docker_data = requests.get(f"https://raw.githubusercontent.com/cybersuki/StoreDock/main/Docker/{self.lang_os}/{self.version}/Dockerfile")

            # Checks the status code for the repository connection
            if docker_data.status_code == 200:
                with open("Dockerfile", "w") as f:
                    f.write(docker_data.text)

                # Grab the size of the Dockerfile
                dockerfile_size = os.path.getsize("Dockerfile")

                # Displays a progress bar for download
                Faye.progress(total=dockerfile_size, description="Dockerfile")

                if os.path.exists("Dockerfile"):
                    print(Faye.log(msg="Downloading Dockerfile complete", level="INFO"))

            # Allows the user to build the Docker container during runtime (+ Dockerfile generation)
            if docker_data.status_code == 200 and self.build:
                with open("Dockerfile", "w") as f:
                    f.write(docker_data.text)

                # Builds the Docker container
                # NOTE: This requires Docker to be installed on the user's system and be configured in the PATH
                os.system(f"docker build . -t shinigami-{self.lang_os}{self.version}")

                print(Faye.log(msg="Successfully built Docker container", level="INFO"))

            # If the Dockerfile doesn't exist, we do a simple print statement and unclean exit
            if docker_data.status_code != 200:
                print(Faye.log(msg="This Docker configuration is not currently supported", level="WARNING"))
                exit(0)
        
        except Exception as e:
            return e
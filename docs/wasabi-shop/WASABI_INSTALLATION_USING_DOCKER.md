![](data:image/png;base64...)

WASABI

INSTANCE INSTALLATION

USING DOCKER

|  |  |
| --- | --- |
| Title | Wasabi Instance Installation using Docker |
| Document Owners | Federico Tonin (I-Deal) |
| Contributors |  |
| Dissemination |  |
| Date | 25/06/2024 |
| Version | 1.0 |

![](data:image/png;base64...)

VERSION HISTORY

|  |  |  |  |
| --- | --- | --- | --- |
| Nr. | Date | Author (Organization) | Description |
| 1.0 | 25/06/2024 | Federico Tonin (I-Deal) | First version | |
|  |  |  |  | |
|  |  |  |  | |
|  |  |  |  | |
|  |  |  |  | |
|  |  |  |  | |

**Reviewers**

|  |  |
| --- | --- |
| Name | Organization |
|  |  |
|  |  |

DISCLAIMER

This document does not represent the opinion of the European Commission, and the European Commission is not responsible for any use that might be made of its content. This document may contain material, which is the copyright of certain WASABI consortium parties, and may not be reproduced or copied without permission. This document is supplied confidentially and must not be used for any purpose other than that for which it is supplied. It must not be reproduced either wholly or partially, copied or transmitted to any person without the authorisation of the Consortium.

ACKNOWLEDGEMENT

This document is a deliverable of the WASABI project. This project has received funding from the European Union’s Horizon Europe programme under grant agreement Nº 101092176

ContenT

[1. INTRODUCTION 2](#_Toc170216323)

[1.1 Why this document 2](#_Toc170216324)

[2. Requirements 3](#_Toc170216325)

[2.1 Docker Desktop installation 3](#_Toc170216326)

[3. WASABI Instance installation 6](#_Toc170216327)

[3.1 Wasabi project folder download 6](#_Toc170216328)

[3.2 Set-up Wasabi instance using Docker 6](#_Toc170216329)

[3.3 Testing and optimizations 8](#_Toc170216330)

# INTRODUCTION

## Why this document

The documentation provided in deliverable D3.3 outlines the installation of a Wasabi instance directly from the source code.

This installation process can be challenging to follow if certain components are missing or if the architecture does not fully comply with PrestaShop requirements.

Based on initial feedback and suggestions, we have prepared a Docker file (docker-compose.yml) that includes all necessary components. Thanks to this new procedure, to replicate these steps you only need to have Docker installed on your machine.

# Requirements

## Docker Desktop installation

To begin, ensure that Docker Desktop is installed on your machine, as it is the sole prerequisite for this setup. Docker Desktop is available for various operating systems including Windows, macOS, and Linux.

You can download the appropriate version for your operating system from the official Docker website (<https://www.docker.com/products/docker-desktop>).

![](data:image/jpeg;base64...)

Figure 1: Docker Official Website

Follow the installation instructions provided on the site to successfully install Docker Desktop, for example on a MacOS just drag & drop the Docker Application into Applications folder.

Once installed, verify the installation by running a simple Docker command in your terminal or command prompt.

**![](data:image/png;base64...)**

This will confirm that Docker is correctly installed and ready for use, showing actual version number and build.

With Docker Desktop installed, you are equipped to proceed with setting up the Wasabi instance using the provided Docker image.

# WASABI Instance installation

## Wasabi project folder download

The first step is the download of the WASABI project folder from Gitlab, in order to obtain every project file with the following command:

git clone https://<WASABI_GITLAB_USER>:<WASABI_GITLAB_TOKEN>@gitlab.com/wasabimarketplace/wasabi.git

For the HumanEnerDIA release deployment, do not commit or paste the real token into
project files. Prefer a temporary credential helper, a one-shot environment variable,
or an interactive Git prompt on the target server.

![](data:image/png;base64...)

## Set-up Wasabi instance using Docker

After the download of project folder, we can move in wasabi folder and launch the following Docker command:

docker compose -f ./Docker/docker-compose.yml up --build -d

![](data:image/png;base64...)

and you will see a long output, showing every component being downloaded and extracted (figure 2).

![](data:image/png;base64...)

Figure 2: Docker compose output

The last step of the installation procedure is the import of the Database file, with command

docker exec -it wasabi-db sh -c "mysql -u root -proot wasabi < PS-Wasabi-Default.sql"

![](data:image/png;base64...)

You can ignore the warning, since default MySQL username and password are root/root we can safely show them.

You can change them later according to your security policy.

## Testing and optimizations

After the installation process you can go to Docker dashboard and see the two containers created.

You can click on the highlighted link to open the browser at the right location.

![](data:image/jpeg;base64...)

Figure 3: Docker container created and link to test WASABI Instance

![](data:image/jpeg;base64...)

Figure 4: Wasabi Backoffice login page

As usual, you can login with the following credentials:

admin@wasabi.test

admin

Then you have to go to Advanced Parameters 🡪 Performance

![](data:image/jpeg;base64...)

Figure 5: Performance settings

And enable Apache Optimization in order to create / update .htaccess file

![](data:image/jpeg;base64...)

Figure 6: Apache optimization activated

Your Wasabi Instance is now populated with demo data, and it’s ready to be customized.

![](data:image/jpeg;base64...)

Figure 7: Wasabi frontend

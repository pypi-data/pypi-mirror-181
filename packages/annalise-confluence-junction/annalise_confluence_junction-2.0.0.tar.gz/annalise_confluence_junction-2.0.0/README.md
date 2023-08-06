
# Annalise AI - Confluence Junction

This project is expanded from (https://github.com/HUU/Junction) 

# TO DO

- move away from using a docker image and use a pushlished python package
- unit tests for everything
# Running Locally

To run this locally run docker compose up with the documents and images directory as env vairables
```sh
DOCS=<path to docs> IMAGE=<path to images> docker-compose up
```

# Overview

Junction works by inspecting the changes made on a commit-by-commit basis to your Git repository, and determining what needs to be changed in Confluence to reflect those changes.  Junction (currently) expects to manage the entire [space in Confluence](https://confluence.atlassian.com/doc/spaces-139459.html).  Thus when using Junction you must tell it which Space to target and update.  You must not manually change, create, or modify pages in the target space, or else Junction may be unable to synchronize the state in Git with the state in Confluence.

To allow mixing code (and other items) with markdown files for Junction in a single repository, you can tell Junction a subpath within your repository that functions as the root e.g. all markdown files will be kept in `docs/`.  All files should end with the `.md` extension.

The page will gets its title from the file name, and its contents will be translated into Confluence markup.  See [this example for what output looks like in Confluence](#output-example).

# Usage

Collect a set of credentials that Junction will use to login to Confluence.  You will need to create an [API token](https://confluence.atlassian.com/cloud/api-tokens-938839638.html) to use instead of a password.  **I recommend you make a dedicated user account with access permissions limited to the space(s) you want to manage with Junction**.

In your git repository, create a folder structure and markdown files you would like to publish.  Commit those changes.
``` bash

.
├── (your code and other files)
└── docs/
    ├── Welcome.md
    ├── Installation.md
    └── Advanced Usage
    |   ├── Airflow.md
    |   ├── Visual Studio Online.md
    |   ├── Atlassian Bamboo.md
    |   └── GitHub Actions.md
    └── Credits.md
```

## Images
Images should be placed inside the `images` directory within a subdirectory that has the same name as the respective file. for the above example the image directory could look like this.

```
.
└── images/
    ├── Welcome/
        ├── image1.png
        └── image2.png
    ├──  Installation/
        └── image1.png
    └── Advanced Usage/
        ├── image1.png
        ├── image2.png
        ├── Airflow/
            └── image1.png
```

# Mermaid Diagrams
Mermaid diagrams can be included in the markdown but must include the document name in the opening fence:

` ```mermaid filename=<document name>`

see [here for using mermaid.js in github](https://github.blog/2022-02-14-include-diagrams-markdown-files-mermaid/)
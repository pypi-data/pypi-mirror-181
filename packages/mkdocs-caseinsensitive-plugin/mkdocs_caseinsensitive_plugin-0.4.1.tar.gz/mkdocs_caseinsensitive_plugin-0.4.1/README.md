# mkdocs-caseinsensitive-plugin

This plugin allows you to link to case-insensitive documentation files.

## Usecase

When presented with the following tree directory structure:

```
project
│   works_for_images.md (contains link to "folder1/IMAGE.PNG")
│   works_for_markdown.md (contains link to "FOLDER1/readme.md")
│
└───folder1
│   │   image.png
│   │   README.md
```

MkDocs will produce the following logging warning messages

```
WARNING  -  Documentation file 'works_for_images.md' contains a link to 'folder1/IMAGE.PNG' which is not found in the documentation files.
WARNING  -  Documentation file 'works_for_markdown.md' contains a link to 'FOLDER1/readme.md' which is not found in the documentation files.
```

Consequently, the rendered HTML files will not have the appropriate links in place.

This issue has been raised on the [MkDocs repository](https://github.com/mkdocs/mkdocs) before [here](https://github.com/mkdocs/mkdocs/issues/1810). Understandably, this is desirable behaviour due to the differences in operating systems in how lax they are when it comes to case-sensitivity in files and directories.

## Installation

Install the package with pip:

```bash
pip install mkdocs-caseinsensitive-plugin
```

TODO:
Install the package from source with pip:

```bash
git clone https://github.com/TheMythologist/mkdocs-caseinsensitive-plugin.git
```

Enable the plugin in your `mkdocs.yml`:

```yml
plugins:
    - search: {}
    - caseinsensitive: {}
```

> **NOTE:** If you have no `plugins` entry in your configuration file yet, you'll likely also want to add the `search` plugin. MkDocs enables it by default if there is no `plugins` entry set, but now you have to enable it explicitly.

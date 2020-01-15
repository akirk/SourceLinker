# SourceLinker
Sublime Text plugin to open URLs for files in your project. Inspired by https://github.com/rscherf/GitLink

# How it works
Use the shortcut `command + shift + o` to open the configured source URL in your browser.

# Configuration
By default it will fall back to a Github URL and determine the org and repo from git.

You can also add custom URL configuration via project settings:
```
{
    "settings": {
        "sourcelinker_remote_url": "https://myownrepo.com/{path}{filename}#{line}"
    }
}
```

# Installation
To install, please clone Git repository directly:
* `cd ~/Library/Application Support/Sublime Text 3/Packages/`
* `git clone git@github.com:akirk/SourceLinker.git`
* Restart Sublime Text

Visual Git
==========
View and interact with your git repositories like never before!

At it's core, Visual Git is a learning tool for git. We believe that everyone that learns git, loves git. So it's our hope to provide a tool to ease that learning process, and get folks to the git lovin' faster, and maybe funner.

We all know that git provides a pretty solid command line interface that allows us to perform actions on our repositories that range from the basic to the downright magic. Visual Git is a handy new graphical tool for interacting with (and hopefully learning more about) your git repositories. All pertinent information about a repository and any actions taken on it are displayed, and animated when possible.

The Canvas is the real shining star of Visual Git. It's a visual representation of the commit history for a local repository, and supports various gestures for common git actions such as showing log information, checking out a branch, merging, and rebasing. The Canvas is housed within the Dashboard, which is where all other repository information is displayed. The dashboard also provides additional functionality for interacting with the repository.

All actions taken on the git repository via the Canvas or Dashboard are logged and displayed, so the user can see how to accomplish the same amazing feats via the command line. We believe that by providing users with a rich set of information about their repository, allowing them to interact intuitively with it, and animating those interactions while simultaneously showing the underlying git commands, we can ease the learning curve of git.

Requirements
============
- [Python 3.4.0](https://www.python.org/download/releases/3.4.0/) (updating to [3.4.1](https://www.python.org/download/releases/3.4.1/) soon)
- [PyQt4](http://pyqt.sourceforge.net/Docs/PyQt4/)
- [Qt Designer](http://qt-project.org/doc/qt-4.8/designer-manual.html) for editing user interface
- Although it's not a requirement, we are major fans of [PyCharm](http://www.jetbrains.com/pycharm/) (and everything else by JetBrains, for that matter), and so we recommend you try it out if you haven't already. It's the bee's knees of Python IDEs. And don't bother wasting our time telling us why _your_ IDE is better. It's not. Just get over it.

Installation
============
Installation instructions coming soon.

Usage
=====
Platform-specific executables and detailed usage instructions coming soon.

API Documentation
=================
The API documentation will be available shortly via ReadTheDocs. We are working to get it up and running as soon as possible. Please excuse our shortcomings in the meantime (sorry, we're Sphinx noobs).

Features
========
###Completed
- Local Repo API
    - Get all branches in a local repo
    - Get the contents of a git object by sha
    - Get complete commit history for a repository

###Planned
- Canvas UI
    - Nodes and arrows to represent git graph(s)
    - Gestures
        - Drag branch onto branch to merge
        - Drag arrows to rebase
        - Drag HEAD to checkout
        - Tool Tips (always when hovering)
            - Commit messages over commit nodes
        - Zooming and panning
    - Animations
        - Slow and educational!
        - Reflect ALL commands run on repo
        - Auto scroll to latest activity
        - Mimic gestures
- Dashboard UI
    - Merge Tool
        - Show ‘ours’ and ‘theirs’, and middle pane reflecting
        - Use Intellij’s as a guide
    - Everything from Gitk
    - Widget(s) for showing info on selected canvas item
    - Multiple canvas tabs
    - Command output pane
    - Menus
    - Git API interactions
    - Correct resizing behavior
    - Staging area shown
- Local Repo API
    - Refactor this into the LocalRepository class
    - Deserialize a commit object file into a CommitObject
    - Get tags (lightweight and annotated)
    - File watcher
- Git API
    - All basic git commands, with options (detailed list coming soon)
    - Return useful data, including error messages
- Github API
    - Use requests library
    - Get collaborator info
    - Get repo usage data


Contributing
============
We welcome contributions with open arms! Well, not _too_ open... For detailed information on how to contribute to this project, please read our [Coding Conventions Wiki](http://visualgit.readthedocs.org/en/latest/index.html). It has all you need to know about how to prepare your code for submission. Even if we know you and like you, if your code isn't up to spec, it's not touching this repository!

Communication
=============
As noted in our [Coding Conventions Wiki](http://visualgit.readthedocs.org/en/latest/index.html), [GitHub Issues](https://github.com/AnthonyReid99/VisualGit/issues) will be the primary means of communication for this project. Whether it be a question, comment, bug report. feature request, or anything else involving the project, it would be best to keep our discussion there. We love feedback, so head on over there whenever the mood strikes you and let us know how you feel!

About the Team
==============
Visual Git is currently being developed by a group of Computer Science students from UMass Boston, but we hope to have contributors from all over the world someday! Credit to Anthony Reid for the initial idea.

See a complete list of contributors [here](https://github.com/AnthonyReid99/VisualGit/graphs/contributors).

License
=======
GNU General Public License. See LICENSE for more information.

This is a free, open-source project.
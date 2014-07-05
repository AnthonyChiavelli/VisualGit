Visual Git
==========
![Visual Git Main Window](http://i.imgur.com/L2AQEMN.png)

View and interact with your git repositories like never before!

At it's core, Visual Git is a learning tool for git. We believe that everyone that learns git, loves git. So it's our hope to provide a tool to ease that learning process, and get folks to the git lovin' faster, and maybe funner.

We all know that git provides a pretty solid command line interface that allows us to perform actions on our repositories that range from the basic to the downright magic. Visual Git is a handy new graphical tool for interacting with (and hopefully learning more about) your git repositories. All pertinent information about a repository and any actions taken on it are displayed, and animated when possible.

The Canvas is the real shining star of Visual Git. It's a visual representation of the commit history for a local repository, and supports various gestures for common git actions such as showing log information, checking out a branch, merging, and rebasing. The Canvas is housed within the Dashboard, which is where all other repository information is displayed. The dashboard also provides additional functionality for interacting with the repository.

All actions taken on the git repository via the Canvas or Dashboard are logged and displayed, so the user can see how to accomplish the same amazing feats via the command line. We believe that by providing users with a rich set of information about their repository, allowing them to interact intuitively with it, and animating those interactions while simultaneously showing the underlying git commands, we can ease the learning curve of git.

VisualGit is a free, open-source project. If you're interested in contributing, please check out the [Contributions](https://github.com/AnthonyReid99/VisualGit#contributions) section below.

Requirements
============
- [Python 3.4.0](https://www.python.org/download/releases/3.4.0/) (updating to [3.4.1](https://www.python.org/download/releases/3.4.1/) soon)
- [PyQt4](http://pyqt.sourceforge.net/Docs/PyQt4/)
- [Qt Designer](http://qt-project.org/doc/qt-4.8/designer-manual.html) for editing user interface
- Although it's not a requirement, we are major fans of [PyCharm](http://www.jetbrains.com/pycharm/) (and everything else by JetBrains, for that matter), and so we recommend you try it out if you haven't already. It's the bee's knees of Python IDEs. And don't bother wasting our time telling us why _your_ IDE is better. It's not. Just get over it.

Installation
============
Python 3 and PyQt4 are required. These can be installed from the Ubuntu repos as "python3" and ("python3-qt4" or "python3-pyqt4") respectively.

At release, this project will be available on the python package index. Use pip or easy-install to install it, and the dependencies will be handled for you.

We also plan to release binaries for linux (i386 and amd64), mac, and windows.

More detailed installation instructions coming soon.

Usage
=====
Platform-specific executables and detailed usage instructions coming soon.

API Documentation
=================
The API documentation will be available shortly via ReadTheDocs. We are working to get it up and running as soon as possible. Please excuse our shortcomings in the meantime (sorry, we're Sphinx noobs).

Contributions
=============
We welcome contributions with open arms! For detailed information on how you can contribute to this project, please read our [Python Conventions Wiki](http://visualgit.readthedocs.org/en/latest/index.html). It has all you need to know about how to prepare your code for submission. Even if we know and like you, if your code isn't up to spec, it's not touching this repository!

We strongly recommend that all contributors (and anyone else that would like to dig a little deeper into git) read [Git Internals](https://github.com/pluralsight/git-internals-pdf/releases) by Scott Chacon. It's a great read, and we'd like to say a big thank you Mr. Chacon for all his amazing git documentation! 

During this phase of the project, it is best if you contact the Reviewers, Anthony Reid (anthonyreid99@gmail.com) and Kahmali Rose (krose72205@gmail.com), before starting any work. We will do our best to respond in a timely manner!

Communication
=============
As noted in our [Coding Conventions Wiki](http://visualgit.readthedocs.org/en/latest/index.html), [GitHub Issues](https://github.com/AnthonyReid99/VisualGit/issues) will be the primary means of communication for this project. Whether it be a question, comment, bug report. feature request, or anything else involving the project, it would be best to keep our discussion there. We love feedback, so head on over there whenever the mood strikes you and let us know how you feel!

Features
========
###Completed
- LocalRepository
    - Get all branches in a local repo
    - Get the contents of a git object by sha
    - Get complete commit history for a repository
    - Deserialize a commit object file into a CommitObject

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
    - Staging area displayed
- LocalRepository
    - File modification event listener for refresh alert
- Git API (our python library for running git commands)
    - Return all pertinent, deserialized data, including error messages
    - Git commands supported
        - **Setup/Config:** init, clone, config, help
        - **Snapshotting:** add, commit, diff, status
        - **Branching:** branch, checkout, log, merge, stash, tag
        - **Sharing:** fetch, pull, push,
        - **Patching:** rebase, interactive rebase
        - **Misc:** grep, cat-file, show
- GitHub API
    - Use requests library
    - Get collaborator info
    - Get repo usage data
    - Get any other interesting API data

About the Team
==============
Visual Git is currently being developed by a group of Computer Science students from UMass Boston, but we hope to have contributors from all over the world someday! Credit to Anthony Reid for the idea.

Check out a complete list of contributors [here](https://github.com/AnthonyReid99/VisualGit/graphs/contributors).

License
=======
This is a free, open-source project under the GNU General Public License. See LICENSE for more information.

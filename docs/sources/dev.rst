.. _GitHub: https://github.com/

.. _Git: https://git-scm.com/

.. _Miniconda: http://conda.pydata.org/miniconda.html

.. _PyCharm: https://www.jetbrains.com/pycharm/

.. _dev:

For developers
==============

This page provides technical notes for the developers of the Linguistica 5 project group.
For introductory background about the Linguistica 5 codebase,
please consult :ref:`codebase`.

None of the development notes below are
new, as they all come from the collective wisdom of the open-source and
software development community -- notably, for what is known as "gitflow".
They should be taken as best practice recommendations, and nothing is set in stone.
While your general goal is to get pull requests up,
the way how you make pull requests is entirely up to you.
Naturally, you can deviate from any of the advice given here;
in that case, you are on your own and you know what you are doing.

.. _dev_reminders:

Important reminders
-------------------

1. **Never commit changes to a master branch.**

      Not even at your own fork -- this ensures that the master branch
      is always clean and serves as a fall back.

2. **Create task-specific branches.**

      Never create a branch like "develop" and "research" and plan to vomit
      a huge amount of your great work into it before making any pull requests
      (this would make code review impossible). Think of a branch as something
      much more concrete like a mini project, with branch names like
      "add-feature-x" or "fix-function-x".

3. **Keep pull requests small.**

      A pull request has to be small (say, fewer than 300 lines of changes)
      so that the code review can be done efficiently and effectively with
      useful feedback.

4. **Follow PEP 8 in coding.**

      The `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_
      coding conventions exist precisely because we would like to schedule
      exactly no time for discussing things like "how to name variables",
      "whether space is needed" and so on for coding.
      There are excellent IDEs such as PyCharm_ for maintaining Python projects
      at a high level of quality.

5. **Do not directly modify the HTML files of the documentation.**

     To update the documentation, edit the source ``.rst`` files under
    ``docs/sources/``, and then follow the notes in ``readme-dev.md`` to
    generate the new HTML files.

Setting up the development environment
--------------------------------------

1. You will need a GitHub_ account. If you are creating a new one,
   pick a username preferably with lowercase letters only, e.g. "joesmith".
   The Linguistica 5 codebase is hosted on GitHub.
   Your contributions will be added to it via the GitHub interface.

2. You will need Git_ for version control.
   Your contributions will be managed and uploaded from your local drive to
   GitHub by Git.

3. Log on to your GitHub account and go to https://github.com/linguistica-uchicago/lxa5

4. At the top right hand corner, click "Fork".
   (If prompted for "where should we fork this repository", choose your own personal GitHub username.)

5. Now under your personal GitHub account, you see a new repository called "lxa5".

6. Clone this repository onto your local disk using Git,
   and also install the Linguistica 5 Python library and its dependencies:

   .. code::

      $ git clone https://github.com/<your-github-username>/lxa5.git
      $ cd lxa5
      $ pip install -r requirements.txt
      $ pip install -r dev-requirements.txt
      $ python setup.py develop

   In the last command just above,
   ``python`` is meant to point to the specific Python interpreter
   you are using for the Linguistica 5 project. Depending on how your Python
   distribution is set up, the command you need could be something else, e.g.
   ``python3``.
   Also, if you're on Linux, you will probably need ``sudo``.

   Now you have the Python library (called ``linguistica``) installed in development mode
   (i.e. changes in source code are immediately effective -- no need to uninstall
   and reinstall to try out new code).

7. Add a link to the linguistica-uchicago/lxa5 repository:

   .. code::

      $ git remote add upstream https://github.com/linguistica-uchicago/lxa5.git

   This command adds a new link to the linguistica-uchicago/lxa5 repository
   (not your fork on GitHub) and names it as "upstream".
   From time to time, you will need to keep your local
   copy of the Linguistica 5 codebase up-to-date by pulling the latest code
   from the linguistica-uchicago/lxa5 repository. This added link (with the name
   "upstream") tells Git where to pull updates from.

   By default, after you have cloned and created a copy of Linguistica 5 on
   your local drive (in step 4 above), there is already a link called "origin"
   set up and linked to your fork on GitHub. Run the following to verify you
   have "origin" pointing to your fork and "upstream" pointing to
   linguistica-uchicago/lxa5:

   .. code::

      $ git remote -v


Committing changes and making a pull request
--------------------------------------------

After you have set up your system and downloaded Linguistica 5 as described above,
you are now (almost) ready to do awesome work!

1. **Verify that the master branch on your local drive is up-to-date in sync with
   the master on linguistica-uchicago/lxa5.**

      It is important to make sure you start working with the latest
      codebase:

      .. code::

         $ git checkout master  # go to master branch
         $ git pull upstream master  # pull latest from master branch of upstream

      Recall that "upstream" means the linguistica-uchicago/lxa5 repository.


2. **Create a new branch for your great work.**

      Never work from the master branch.
      (Run "git branch" anytime to see what branches you have and which branch you're on.)

      Instead, work on a different branch whose name indicates what you are doing,
      e.g. "revamp-stems-to-signatures", "update-docs", "fix-bug-in-function-x":

      .. code::

         $ git checkout -b <branch-name>

      After this command is run, the new branch is created *and* you are on
      that branch as well (no longer on master branch).

3. **Start committing changes to source code.**

      Now (and finally!) you can actually make changes to the source code.
      Make changes incrementally and commit them with Git.
      Run this pair of commands for each commit:

      .. code::

         $ git add <files-changed>
         $ git commit -m "<commit-message>"

      ``<files-changed>`` can be a single file (e.g. ``foo.py``) or multiple ones
      separated by spaces (e.g. ``foo.py bar.py``).

      Write brief and meaningful commit messages,
      e.g. "Fix bug in stems_to_signatures".
      Aim at making each commit a logical and meaningful chunk of changes.

4. **Repeat step 3 above as needed.**

      Repeat step 3 for making more commits on your way to what the branch
      is for. Limit the number of line changes to below 300 to make
      efficient and effective code review possible.

5. **Run tests to make sure nothing breaks.**

      Run the tests (and get a detailed report if anything breaks):

      .. code::

         $ py.test -vv --cov linguistica linguistica


      Make sure the code is PEP8 compliant:

      .. code::

         $ flake8 linguistica

6. **Push your changes to your fork on GitHub.**

      To make your changes available for review and for merging,
      you will first have to push your changes to your fork on GitHub:

      .. code::

         $ git push origin <branch-name>

      Recall that "origin" is the (default) name point to your fork <your-github-username>/lxa5 on GitHub.

7. **Make a pull request.**

      Log on to your GitHub and go to your fork <your-github-username>/lxa5.
      Now you are ready to make a pull request
      (i.e. you want linguistica-chicago/lxa5 to get the changes
      from your <branch-name> of <your-github-name>/lxa5, as it were).
      Click "Pull request"
      (or something like "Make pull request" -- it should be something fairly prominent visually).
      Create the pull request by giving your pull request a title
      (most probably something very similar to the branch name) and
      providing brief notes on what the new changes are in the "comments" section.
      Now you'll wait for feedback.

8. **Start a new branch for a new mini project.**

      After all your hard work in the pull request has been accepted (= merged
      into linguistica-uchicago/lxa5), you can go back to step 1
      to update your master branch for the latest code and prepare
      for a new branch and an upcoming pull request!

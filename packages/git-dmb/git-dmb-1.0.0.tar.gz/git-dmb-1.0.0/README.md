# git-dmb

A convenient command-line tool helping you keep repositories clean.

git-dmb on PyPI is technically a "virtual" or "meta" package
that leverages Setuptools' feature `install_requires`
to pull in the current latest version
of package [git-delete-merged-branches](https://pypi.org/project/git-delete-merged-branches/)
which comes with command `git-dmb` and the actual software.

The motivation behind this package is to protect users against
[attacks like Pytosquatting](https://pytosquatting.overtag.dk/), primarily.

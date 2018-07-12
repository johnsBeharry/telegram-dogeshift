# Getting Started

The first thing you will need to do is to clone the repository.

1. `git clone git@github.com:peakshift/telegram-dogecoin.git`
2. `cd telegram-dogecoin`

# Contributing

### Branches
- A branch name should begin with the issue number, and have short name (2-4 words). New features or fixes should be based off of the `master` branch.
  - `git checkout -b 123-short-name master`

### Pushing Changes
1. Open Terminal.
2. `git pull`
3. `git add file_name.py`
4. `git commit -m "type(component): subject line"`
5. `git push origin 123-short-name `

### Commit Messages

*We follow the [Angular commit guidelines](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#-git-commit-guidelines) so that we can generate changelogs and have a clean commit history — see Pushing Changes #3 for an example commit.*

- Type, for your commit message commiting you should select a type from this list below:
  - feat: a new features
  - fix: a bug fix
  - docs: documentation only changes
  - style: changes that do not affect the menaing of the code (white-space, formatting, missing semi-colons, etc)
  - refactor: a code change that neither fixes a bug or adds a feature
  - pref: a code change that improves performance
  - test: adding missing tests
  - chore: changes to the build process or auxiliary tools and libraries such as documentation generation
- Components, represent the larger feature / scope of the change
- Subject line, use the imperative form of a verb
  - GOOD "add contributing guidelines"
  - BAD "adding contribuing guidelines"

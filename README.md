# Prerequisites

#### Setup Block.io Account
[block.io](https://block.io) will be used by the bot so it can create and label wallets for users who type `/register`.

1. Go to [block.io](https://block.io) and create an account (free)
2. Set a pin, and save your [mnemonic](https://en.wikipedia.org/wiki/Mnemonic) phrase offline.
_This will be used to generate your wallet again in the event you lose access to your account so always have the habit of keeping this safe._
3. Click on "Show API Key" then copy the key for "Dogecoin (testnet)"

#### Create a Telegram Bot [@BotFather](https://core.telegram.org/bots#6-botfather)
Further bot  documentation [link](https://core.telegram.org/bots#6-botfather)

1. Start a chat with [@botfather](https://telegram.me/botfather)
2. Type `/newbot` then follow the instructions
3. @botfather will send you your bot's authentication token

# Getting Started

Once you have a Block.io Account setup, and created your own Telegram Bot it's time to clone the project and get it setup.

1. `git clone git@github.com:peakshift/telegram-dogecoin.git`
2. `cd telegram-dogecoin`
3. `pip install block-io`
4. `pip install requests`
5. `pip install behave`
6. `TELEGRAM_BOT_TOKEN=<your token> BLOCKIO_API_KEY=<your key> BLOCKIO_PIN=<your pin> python3 run.py`

_In step 5, replace the entire of `<your token>`, `<your token>`, `<your token>`._

# Contributing

### Branches
- A branch name should begin with the issue number, and have short name (2-4 words). New features or fixes should be based off of the `master` branch.
  - `git checkout -b 123-short-name master`

### Testing
When making changes or adding a new feature, to ensure the feature works correctly or the changes made have not broken the code then you can do unit testing using the behave framework and gherkin scenarios.
*[Behave Framework Docs](https://behave.readthedocs.io/en/latest/) 

To begin testing your scenarios
- do `pipenv install`
- run `pipenv run behave`
- if it passes
  - commit and push your branch
  - checkout develop and merge your branch
  - push the develop branch
  - open a pull request for your branch in master
- if it fails
  - fix the problem so all tests pass

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

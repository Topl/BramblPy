# Contributing to BramblPy

You want to contribute to BramblPy? Awesome. Please take a few moments to
review the following guidelines to get you started. Cheers.

* [Communication channels](#communication)
* [Team members](#team)
* [Documentation](#documentation)
* [Issue tracker](#issues)
* [Bug reports](#bugs)
* [Pull requests](#pull-requests)
* [Versioning](#versioning)
* [License](#license)

<a name="communication"></a>
## Communication channels

Before you get lost in the repository, here are a few starting points
for you to check out. You might find that others have had similar
questions or that your question rather belongs in one place than another.

* Chat: https://discord.gg/CHaG8utU
* Website: https://www.topl.co/
* Twitter: https://twitter.com/topl_protocol


<a name="team"></a>
## Team members

BramblPy is developed as an open source project by [Topl](https://www.topl.co/)
headquartered in Houston, TX. The core maintainers you will encounter in this project
are all part of Topl.

## Documentation

The BramblPy documentation is primarily auto-generated.
Any pull requests to improve the documentation are highly appreciated.

<a name="issues"></a>
## Using the issue tracker

The issue tracker is the preferred channel for [bug reports](#bugs),
[features requests](#features) and [submitting pull
requests](#pull-requests), but please respect the following restriction:

Please **do not** use the issue tracker for personal support requests (use [Discord chat](https://discord.gg/CHaG8utU)).

<a name="bugs"></a>
## Bug reports

A bug is a _demonstrable problem_ that is caused by the code in the repository.
Good bug reports are extremely helpful - thank you!

A good bug report shouldn't leave others needing to chase you up for more
information. Please try to be as detailed as possible in your report. What is
your environment? What steps will reproduce the issue? What would you expect to
be the outcome? All these details will help people to fix any potential bugs.

<a name="pull-requests"></a>
## Pull requests

Good pull requests - patches, improvements, new features - are a fantastic
help. Thanks for taking the time to contribute.

**Please ask first** before embarking on any significant pull request,
otherwise you risk spending a lot of time working on something that the
project's developers might not want to merge into the project.

bip-topl follows the [GitFlow branching model](http://nvie.com/posts/a-successful-git-branching-model). The ```main``` branch always reflects a production-ready state while the latest development is taking place in the ```dev``` branch.

Each time you want to work on a fix or a new feature, create a new branch based on the ```dev``` branch: ```git checkout -b BRANCH_NAME dev```. Only pull requests to the ```dev``` branch will be merged.

<a name="commit-message-convention"></a>
## Commit Message Convention

BramblPy adapts the [Vue's commit convention](https://github.com/vuejs/vue/blob/dev/.github/COMMIT_CONVENTION.md). Commit messages can have the following types:

- `build:` Changes that affect the build system or external dependencies
- `chore:` Changes to readme, etc
- `ci:` Changes to our CI configuration files and scripts
- `docs:` Documentation only changes
- `feat:` A new feature
- `fix:` A bug fix
- `perf:` A code change that improves performance
- `refactor:` A code change that neither fixes a bug nor adds a feature
- `style:` Changes that do not affect the meaning of the code (white-space, formatting, etc)
- `test:` Adding missing tests or correcting existing tests

## Versioning

BramblPy is maintained by using the [Semantic Versioning Specification (SemVer)](http://semver.org).

<a name="license"></a>
## License

By contributing your code, you agree to license your contribution under the [MPL 2.0](LICENSE)
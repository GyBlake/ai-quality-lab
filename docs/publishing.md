# Publishing ai-quality-lab

Suggested repository name: **ai-quality-lab**

Suggested description:

> Synthetic AI evaluation cases, prompt regression fixtures, and reproducible data-quality checks.

Suggested topics: `ai-evaluation`, `data-quality`, `quality-assurance`, `prompt-engineering`, `python`.

## Prepare the local content

Review the README, MIT license, examples, and Git author identity. Keep the local `.delivery/` handoff folder excluded; it contains a separate profile README draft and review notes, not project source.

Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/audit_data.py --check
git status --short
git diff --check
```

This package began in an empty Git repository on branch `main`. If the initial commit has not been made, stage the project files and create one truthful initial commit:

```bash
git add README.md LICENSE CONTRIBUTING.md TODO.md .gitignore .github docs projects scripts tests
git diff --cached --stat
git diff --cached --check
git commit -m "Add synthetic AI evaluation and data quality lab"
```

Use the Git identity you intend to publish; a GitHub-provided no-reply address is an option if you do not want a personal address in commit metadata. Do not backdate commits or split completed work into an artificial activity history.

## Create the GitHub repository

On GitHub, create an empty public repository named `ai-quality-lab` under `GyBlake`. Do not initialize it with another README, license, or .gitignore because those files already exist locally. Then, if `origin` has not been configured:

```bash
git remote add origin https://github.com/GyBlake/ai-quality-lab.git
git push -u origin main
```

If a remote already exists, inspect `git remote -v` before changing it. Do not force-push over another repository.

Alternatively, with an authenticated GitHub CLI and a committed local repository:

```bash
gh repo create GyBlake/ai-quality-lab --public --source=. --remote=origin --push
```

Choose one publishing route. These commands publish the committed files and history; they are instructions, not a record that publication has occurred. The workflow follows [GitHub’s local-code publishing guide](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github) and [GitHub CLI repository creation](https://cli.github.com/manual/gh_repo_create).

## After publication

Check the repository URL while signed out or in a public preview. Open each example, inspect CSV rendering, and reproduce the commands from a fresh clone. Add the description and topics, and use genuine open issues for the items you actually intend to work on in TODO.md.

The local profile README draft is intended for a separate `GyBlake/GyBlake` repository. Its project link becomes valid once this lab is published. Review any existing profile README before replacing it. See [GitHub’s profile README instructions](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).

Use an actual public email or professional contact URL if you want hiring inquiries outside GitHub. A profile link identifies the maintainer but is not a direct messaging channel. Review the profile's visitor view when deciding whether the lab can be discovered from it.

No status badge is necessary at launch. Add a CI badge only after a real workflow exists and its status is useful to contributors. Future commits should describe actual changes, such as a verified engine discrepancy or a new failure case.

# Branches and branch protection

In projects with one contributor, git history is often linear. Each time the contributor works on something, they commit it to main.

Where there are multiple contributors - and even when a single contributor is working on multiple independent and experimental features at once - it makes sense to consider using [branches](https://book.the-turing-way.org/reproducible-research/vcs/vcs-workflow-branches/). When working with branches, contributors work on individual features in an isolated branch, and merge these changes into the main branch when they are finished. This makes it easier to work concurrently.

To protect us from our own mistakes (and other people's), it makes sense to both 
- Block local commits to main using a pre-commit hook, and  
- Enforce branch protection rules at the github repository level

This repository template comes with a script to enable both, which you can run (whenever you feel like branch protection makes sense for your repo, this may not be immediately), with

```
uv run .github/rulesets/protect.py
```

This will prevent anyone from pushing directly to main, or from rewriting history on the `main` branch of the repository. These *can* be bypassed by repository admins.


## Requiring reviews to PRs

In highly collaborative projects where you want to enforce quality checks, you can enforce stricter standards and require at least `N` approving reviews before a pull request can be merged into your main branch with

```
uv run .github/rulesets/protect.py --reviews N
```

## Notes

To apply branch protection rules, you'll need GitHub credentials: 
either a `GITHUB_TOKEN` environment variable (fine-grained token for the repo, permission **Administration: write**) 
or the GitHub CLI if you happen to have it installed — the script reuses `gh auth token` automatically. 
If you have neither, it prints instructions.


You can skip the pre-commit hook with 
```sh
SKIP=no-commit-to-branch git commit -m "important commit that must be to main!!"
```

### Plan limitations (pik-ecs org)

- **Private repos can't be protected at all** on the org's current GitHub Free plan - both rulesets and legacy branch protection return an "upgrade to Pro" error. 

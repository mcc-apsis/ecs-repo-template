## I want to use this template, but I don't agree with the specific choices, what do I do?

Please create a branch from this template and add your preferred way to set up a repo.

For example, you may want to extend or restrict the code style rules implemented with ruff, or you may want to use a different tool altogether for code styling.

You can just make changes directly in the branch, and refer to this when creating a project from the template.

```
uvx copier copy gh:mcc-apsis/ecs-repo-template --trust --vcs-ref cool-new-branch my-new-project
```

If you think that others would benefit from this change, please open a pull request into main.

If you think that this may be something that a user would want to configure, consider editing the questions in copier.yml, and making the change dependent on those answers.
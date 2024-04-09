# Python Package Template

This repository contains the basic structure for a python package as well as some useful GitHub actions for maintaining the package.

In order to use this template you must perform the following steps. In each step I will explain how you can do it manually and I will also provide commands (sorry windows users, sucks to suck) to automate the process where possible.

## 1. Set command variables

In the following instructions, commands will make reference to several variables. You can set these variables now so you can run all subsequent commands without having to edit them. (Replace `...` with actual values.)

```sh
PACKAGE="..." # The name of your package. Use kebab-case.
MODULE=$(echo $PACKAGE | tr - _) # The name of your module. Should be the package name in snake_case.
PACKAGE_DESCRIPTION="..." # A short description of your package
YOUR_NAME="..." # Your name. Use spaces and start each word with an uppercase letter
YOUR_EMAIL="..." # Your email address
GITHUB_USERNAME="..." # Your GitHub username
MIN_PYTHON_VERSION="..." # The minimum version of Python required to use this package
```

If you won't be using the commands below, just make a note of the values you would give to each variable for when they're needed.

## 2. Clone the template

Download the code and place it in a folder, then enter the folder. From now on all commands will be relative to this folder.

```sh
git clone https://github.com/abrahammurciano/python-package-template.git python-$PACKAGE
cd python-$PACKAGE
rm -rf .git
```

## 3. Replace placeholder text

There are several placeholders that you must replace with values from step 1. These match this regular expression: `<<[A-Z_]+>>`. You can use your IDE to find all such placeholders and replace them, or you can use the following commands to do the same.

```sh
find ./ -type f -exec sed -i -e "s/lenient-string-formatter/$PACKAGE/g" {} \;
find ./ -type f -exec sed -i -e "s/lenient_string_formatter/$MODULE/g" {} \;
find ./ -type f -exec sed -i -e "s/A lenient string formatter that leaves unmatched fields untouched in the output string instead of raising a KeyError./$PACKAGE_DESCRIPTION/g" {} \;
find ./ -type f -exec sed -i -e "s/Abraham Murciano/$YOUR_NAME/g" {} \;
find ./ -type f -exec sed -i -e "s/abrahammurciano@gmail.com/$YOUR_EMAIL/g" {} \;
find ./ -type f -exec sed -i -e "s/abrahammurciano/$GITHUB_USERNAME/g" {} \;
find ./ -type f -exec sed -i -e "s/3.12/$MIN_PYTHON_VERSION/g" {} \;
```

Also don't forget to replace any occurences of a placeholder in folder and file names.

```sh
mv '<<MODULE_NAME>>' $MODULE
```

## 4. Create a GitHub repository

- Click [here](https://github.com/new) to create a new GitHub repository.
- Name it `python-$PACKAGE`.
- Enter the value of `$PACKAGE_DESCRIPTION` as the description.
- Don't initialize the repository with a readme, a .gitignore, a license, or any other files.

## 5. Store the necessary credentials

### Create the necessary accounts
- Create a [PyPI](https://pypi.org/account/register/) account if you don't have one.

### Create a GitHub personal access token
- Go to `Settings` > `Developer settings` > `Personal access tokens` > `Generate new token`.
- Name it `GitHub Actions for $PACKAGE`.
- Set it to not expire.
- Select `repo` as the `Scopes` field.
- Click `Generate token`.
- Copy it for the next step.

### Create a PyPI token
You can generate one [here](https://pypi.org/manage/account/). Name it `$PACKAGE`.

### Create the necessary secrets
- Go to `your repository` > `Settings` > `Secrets` > `Actions`.
- Create these new repository secrets:
	- `PERSONAL_GH_TOKEN`
	- `PYPI_TOKEN`

### Grant write access to GitHub Actions
- Go to `your repository` > `Settings` > `Actions` > `General`.
- Under `Workflow permissions` select `Read and write permissions`.
- Click `Save`.

## 6. Push your code to GitHub

You can push your code with the following commands.

```sh
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin git@github.com:$GITHUB_USERNAME/python-$PACKAGE.git
git push -u origin main
```

## 7. Enable GitHub pages

- Go to `your repository` > `Settings` > `Pages`.
- Under `source` select the branch `main`.
- Then for the folder, instead of `/ (root)` choose `/docs`.
- Click save.

## 8. Enforce CI on pull requests to main

First you must trigger the flow once so GitHub is aware of its existance.

- Go to `your repository` > `Actions` > `Tests` > `Run Workflow` > `Run Workflow`
- Go to `your repository` > `Actions` > `Docs & Format` > `Run Workflow` > `Run Workflow`

Now you can require the test flow to run.

- Go to `your repository` > `Settings` > `Branches` > `Add branch protection rule`.
- For the `Branch name pattern` type `main`.
- Check `Require status checks to pass before merging`.
- Type `test`, make sure it comes up in autocomplete, and click it.
- Type `docs_and_format`, make sure it comes up in autocomplete, and click it.
- Then click `Save changes`.

## 9. Some notes

- If your minimum python version is less than 3.8, replace `importlib.metadata` with `importlib_metadata` in your `__init__.py` and add it as a dependency.
```sh
poetry add importlib_metadata
```

## 10. Delete these instructions

Remove the text up to here from this file.

# lenient-string-formatter
A lenient string formatter that leaves unmatched fields untouched in the output string instead of raising a KeyError.

## Installation

You can install this package with pip.
```sh
$ pip install lenient-string-formatter
```

## Links

[![Documentation](https://img.shields.io/badge/Documentation-C61C3E?style=for-the-badge&logo=Read+the+Docs&logoColor=%23FFFFFF)](https://abrahammurciano.github.io/python-lenient-string-formatter)

[![Source Code - GitHub](https://img.shields.io/badge/Source_Code-GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=%23FFFFFF)](https://github.com/abrahammurciano/python-lenient-string-formatter.git)

[![PyPI - lenient-string-formatter](https://img.shields.io/badge/PyPI-lenient_string_formatter-006DAD?style=for-the-badge&logo=PyPI&logoColor=%23FFD242)](https://pypi.org/project/lenient-string-formatter/)

## Usage

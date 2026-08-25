# Git Intro

## Installing Git
Open up a terminal and run the following command to check if Git is already installed on your system:

```bash
git --version
```
If Git is not installed, you can download it from the official website: [https://git-scm.com/downloads](https://git-scm.com/downloads). Follow the installation instructions for your operating system.

## Installing Visual Studio Code
Visual Studio Code (VS Code) is a popular code editor that integrates well with Git. You can download it from the official website: [https://code.visualstudio.com/](https://code.visualstudio.com/). Follow the installation instructions for your operating system.

## Create a GitHub Account
To use Git and GitHub, you need to create a GitHub account. Go to [https://github.com/signup](https://github.com/signup) and follow the instructions to create your account.

Use your student email to create the account.  Upon creating the account, sign up for the GitHub Student Developer Pack to access free tools and resources. You can sign up for the pack at [https://education.github.com/pack](https://education.github.com/pack).

## Setting Up Git
Open VSCode and log in using your GitHub account. You can do this by clicking on the Source Control icon in the left sidebar and then clicking on "Sign in to GitHub".

Sign in using your GitHub credentials. Once signed in, you can start using Git within VSCode.  If you have trouble join a Cyber Security course at Kangan.

## Create a project directory/folder
In most software development environments, directories are used to contain all the files related to a specific project.

Let's navigate to a new directory to start a new project.  Go to the File menu in VSCode, select "Open Folder", and choose a location on your computer where you want to create your project directory.  If you want to create a new directory click the "New Folder" button in the dialog box that appears. Name your folder appropriately for your project.

This will take you to the new directory in VSCode, where you can start creating files for your project.  From here new folders and files can be created by right clicking in the left sidebar and selecting "New File" or "New Folder".

## Initialize a Git Repository
Once you have your project directory set up, you can initialize a Git repository. To do this click on the Source Control icon in the left sidebar of VSCode and then click on "Initialize Repository". This will create a new Git repository in your project directory.

You now have a Git repo!

## Add files to the repository
- Create a new file called *README.md*
- Add the line "# My First Git Project" to the file and save it."

## Staging and Committing Changes
Once you have made changes to your files, you need to stage and commit those changes to your Git repository. Staging allows you to select which changes you want to include in your next commit.

The VSCode Source Control extension can automatically stage changes for you as you commit.  Click the blue commit button.  You will prompted to enter a commit message.  Enter a descriptive message that summarizes the changes you made, such as "Initial commit with README.md".  Press Enter to complete the commit.

To stop this message in future, you can add a commit message in the text box before clicking the commit button.

*What is a commit?*

## Pushing Changes to GitHub
To push your changes to GitHub, you need to create a new repository on GitHub.  You can do this from the the VSCode Source Control extension by clicking on the "Publish to GitHub" button (it's a cloud with an arrow).  You will be prompted to enter a name for your repository and choose whether it should be public or private (choose public to make things simpler).  After entering the information, click "Publish Repository".

*What is a push?*

Using a browser, navigate to your GitHub account and verify that your repository has been created and that your changes have been pushed successfully.

## Add another line to the README.md file
Open the *README.md* file in VSCode and add another line of text, such as "Markdown is a lightweight markup language for creating formatted text using a plain-text editor." Save the file.

- stage, commit and push the changes to GitHub.

## Create a new files
- Create a new file called *git-intro.md* in your project directory.
- Add some content to the file, such as "This is a new file created for the Git Intro project." Save the file.
- Stage, commit, and push the changes to GitHub

- Create another folder called *extras*
- In the *extras* folder, create a new file called *roaches.md*
- Add some content to the file.  The content should be facts about cockroaches.  The content should follow the guide below:
    - Two sections indicated by headings.
        - Cockroach Facts - must have at least 3 facts about cockroaches.  These must be in a bulleted list.
        - Cockroach Anatomy - must have at least 3 facts about cockroach anatomy.  These must be in a table format with two columns.  The first column should be the name of the body part and the second column should be a description of that body part.
    - Include a link to a reputable source for more information about cockroaches.  The link should be in the format of ```[link text](URL)```.
    - Include an image of a cockroach.  The image should be in the *extras* folder and should be referenced in the *roaches.md* file using Markdown syntax.

You can find a markdown cheat sheet here: [https://www.markdownguide.org/cheat-sheet/](https://www.markdownguide.org/cheat-sheet/)

- stage, commit, and push the changes to GitHub.

## Cloning a Repository
To clone a repository from GitHub to your local machine, you can use the following steps:
1. Navigate to the repository on GitHub that you want to clone.
2. Click on the "Code" button and copy the URL of the repository.
3. Open VSCode and go to the Source Control view.
4. Click on the "Clone Repository" button and paste the URL of the repository.
5. Choose a location on your local machine where you want to clone the repository and click "Clone".

- clone the git repo of one of your classmates to your local machine.  Make sure you have permission to clone the repo.

## Make changes to the cloned repository
- Open the cloned repository in VSCode.
- Make some changes to one of the files in the repository, such as adding a new line of text or modifying existing content.
- Stage, commit, and push the changes to GitHub.

*What happens?  Why?*

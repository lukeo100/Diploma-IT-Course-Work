# Fork, Branch & Merge Back

A hands-on Git practice activity using the Source Control panel in VS Code. You'll reinforce cloning, committing, and syncing — and learn three new skills: **forking**, **branching**, and **merging**.

## What you'll practice

- 🆕 Forking
- ✅ Cloning (review)
- ✅ Committing (review)
- ✅ Syncing / pushing (review)
- 🆕 Branching
- 🆕 Merging

---

## Step 1: Fork the repo 🆕

- [ ] Open this repo on GitHub
- [ ] Click the **Fork** button in the top-right corner
- [ ] Confirm the details and click **Create fork**
- [ ] You should now be looking at *your own copy* of the repo, under your GitHub username

> **What's a fork?** It's your own personal copy of someone else's repository, hosted on GitHub under your account. Changes you make to your fork don't affect the original repo unless you explicitly send them back (e.g. via a Pull Request).

## Step 2: Clone your fork

- [ ] Open VS Code
- [ ] Open the Source Control panel (`Ctrl+Shift+G` / `Cmd+Shift+G`)
- [ ] Click **Clone Repository** and paste the URL of **your fork** (not the original repo!)
- [ ] Open the cloned folder in VS Code

## Step 3: Add your student file (commit + sync review)

- [ ] Create a new file called `<studentid>.md` (replace `<studentid>` with your actual student ID)
- [ ] Add your name and course using markdown formatting:
  - A heading with your name (e.g. `## Jane Smith`)
  - A line stating your course
- [ ] Save the file
- [ ] Go to Source Control panel → stage the change (`+`)
- [ ] Write a commit message and commit
- [ ] Click **Sync Changes** to push to the remote

> Your instructor will later add a `judo.md` file to the original repo with some judo facts. Once that happens, you'll be able to pull those changes into your fork too.

## Step 4: Create a new branch 🆕

- [ ] In the bottom-left corner of VS Code, click on the branch name (probably says `main`)
- [ ] Choose **Create new branch...**
- [ ] Name it `add-cockroaches`
- [ ] Confirm the branch name now shows `add-cockroaches` in the bottom-left corner

## Step 5: Make changes on your branch

- [ ] Find the `cockroaches.md` file included in this repo
- [ ] Copy its contents into a new file, also called `cockroaches.md`, in your project directory
- [ ] Save the file
- [ ] Stage, commit, and sync (same steps as before — VS Code may ask to **publish the branch**, click yes)

## Step 6: See branches in action 🆕

- [ ] Click the branch name in the bottom-left corner → switch to `main`
- [ ] Look in your file explorer — is `cockroaches.md` there? (It shouldn't be!)
- [ ] Switch back to `add-cockroaches`
- [ ] Confirm `cockroaches.md` is back

> **Why did this happen?** Each branch holds its own snapshot of the project. Changes made on one branch don't exist on another — until you merge them.

## Step 7: Merge your branch into main 🆕

- [ ] Switch to the `main` branch
- [ ] Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
- [ ] Type and select **Git: Merge Branch**
- [ ] Choose `add-cockroaches`
- [ ] Check your file explorer — `cockroaches.md` should now be on `main` too
- [ ] Sync (push) `main` to send the merged result to the remote

## Step 8: Check your work

- [ ] Open the Source Control **Graph** view (or run `Git: View History`)
- [ ] Find the commit you made on `add-cockroaches`
- [ ] Find the merge commit on `main`
- [ ] Confirm both `<studentid>.md` and `cockroaches.md` exist on `main`

---

## Reflect

- What's the difference between forking and cloning?
- What's the difference between committing and merging?
- Why might branches be useful if you're working with a team, and more than one person is editing the same project?
- What do you think might happen if two people edited the *same line* of a file on two different branches, and then tried to merge?
# Git for Professionals: A Deep, Practical Guide to Git, Branching, Merging, Rebasing, and Merge Conflicts

The video you shared, **“Git for Professionals Tutorial – Tools & Concepts for Mastering Version Control with Git”** from freeCodeCamp, is specifically designed to move beyond the beginner-level `commit`, `push`, and `pull` workflow. Its main sections cover the perfect commit, branching strategies, pull requests, merge conflicts, and merge versus rebase, followed by more advanced Git techniques. The merge-conflict section begins around 24 minutes into the video, followed by merge versus rebase around 33:48. ([YouTube][1])

What follows is a complete Medium-style article that combines those ideas with the deeper Git concepts we discussed earlier. I have deliberately expanded the merge-conflict section substantially, because understanding **why conflicts occur, what Git is actually doing, how to resolve them safely, and how conflicts differ between merge, rebase, cherry-pick, and other operations** is one of the most important steps in moving from beginner Git usage to professional Git usage.

---

## Git Is Not Just a Collection of Commands

When most developers first learn Git, they usually learn a workflow that looks like this:

```text
git add
    ↓
git commit
    ↓
git push
```

Then they learn:

```text
git pull
git branch
git merge
```

This is enough to start working with Git, but it does not give you a strong mental model of what Git actually is.

A professional understanding of Git begins when you stop thinking of Git as a collection of commands and start thinking of it as a **system for maintaining a graph of project history**.

At its core, Git maintains snapshots of your project and relationships between those snapshots. A commit points to a tree representing the project state, while commits also point backward to their parent commits. Branches are references to commits, and `HEAD` identifies where your current checkout is positioned. Once this model becomes clear, operations such as merge, rebase, reset, revert, cherry-pick, stash, and conflict resolution stop feeling like unrelated commands.

The course itself emphasizes this move beyond basic Git usage and focuses on professional workflows such as creating effective commits, choosing branching strategies, handling pull requests, resolving conflicts, and understanding merge versus rebase. ([YouTube][1])

---

# Understanding Git Through a Real Project

Imagine that you are building an AI inference service.

Your repository initially contains:

```text
ai-inference/
├── model.py
├── inference.py
├── config.yaml
├── requirements.txt
└── README.md
```

You initialize Git:

```bash
git init
```

Git creates a `.git` directory.

That `.git` directory is essentially the internal database and metadata area of your repository.

Your actual application files are the **working tree**, while `.git` contains the information Git needs to understand your project's history.

Conceptually, your repository now looks like:

```text
Working Tree
     |
     | Git tracks changes
     v
.git/
     |
     +── objects/
     +── refs/
     +── HEAD
     +── index
     +── logs/
```

The important insight is that Git does not simply keep a folder called "versions".

Instead, Git maintains objects and references that allow it to reconstruct the evolution of your project.

---

# The Four States You Should Understand

A useful mental model is:

```text
Working Tree
      |
      | git add
      v
Staging Area
      |
      | git commit
      v
Local Repository
      |
      | git push
      v
Remote Repository
```

The **working tree** contains the files you are currently editing.

The **staging area**, also called the index, represents what you intend to put into the next commit.

The **local repository** contains your committed Git history.

The **remote repository** is another repository, commonly hosted on GitHub, GitLab, Azure Repos, Bitbucket, or a similar platform.

This explains why `git add` and `git commit` are separate operations.

Suppose you modify three files:

```text
model.py
inference.py
README.md
```

but only want the `model.py` change in the next commit.

You can execute:

```bash
git add model.py
git commit -m "Improve inference performance"
```

Git records only the staged version of `model.py`.

This is why the staging area is so important. It allows you to construct the exact logical snapshot that should become your next commit.

---

# What Is a Git Commit Really?

A commit is more than a timestamped copy of your directory.

Conceptually, a commit contains information similar to:

```text
Commit
 |
 +── Author
 +── Committer
 +── Timestamp
 +── Commit message
 +── Parent commit
 |
 +── Tree
```

The tree describes the state of the repository.

The tree points to file contents represented internally by Git objects called blobs.

Conceptually:

```text
Commit
   |
   v
 Tree
 / | \
/  |  \
v  v   v
Blob Blob Blob
```

For example:

```text
Commit
  |
  v
Tree
  |
  +── model.py      -> blob
  |
  +── inference.py  -> blob
  |
  +── config.yaml   -> blob
```

This object-based architecture is one reason Git can efficiently represent large histories.

---

# Git History Is a Graph

Beginners often imagine Git history like this:

```text
A → B → C → D
```

That is only true for a single linear development path.

Real repositories usually look more like:

```text
A ── B ── C
     \
      D ── E
```

Here, two lines of development diverged from `B`.

Perhaps `main` contains:

```text
A → B → C
```

while your feature branch contains:

```text
A → B → D → E
```

Git therefore represents development as a **directed acyclic graph of commits**.

This graph is the foundation for understanding branching and merging.

---

# A Branch Is Not a Copy of Your Project

This is one of the most important Git concepts.

When you execute:

```bash
git branch feature
```

Git does not duplicate your entire repository.

It creates another reference pointing to a commit.

Suppose you have:

```text
A ── B ── C
         ^
        main
```

After:

```bash
git branch feature
```

you conceptually have:

```text
A ── B ── C
         ^   ^
       main feature
```

Now switch to the feature branch:

```bash
git switch feature
```

and make another commit:

```bash
git commit -m "Add embedding cache"
```

The graph becomes:

```text
A ── B ── C
         \   \
          \   D
           \  ^
            feature

main → C
```

The branch simply moves forward as new commits are created.

---

# HEAD: Where Am I?

`HEAD` is another concept that becomes extremely important when working with advanced Git.

If you are on `feature`, the relationship can be thought of as:

```text
HEAD
 |
 v
feature
 |
 v
D
```

If you switch to `main`:

```text
HEAD
 |
 v
main
 |
 v
C
```

So `HEAD` essentially identifies your current position in the repository's history.

This is why commands involving `HEAD` are so common:

```bash
git log HEAD
git diff HEAD
git reset HEAD~1
```

---

# The Perfect Commit

One of the topics emphasized in the video is the idea of creating effective commits. ([YouTube][1])

A commit should ideally represent one coherent logical change.

Imagine you make all of these modifications at once:

```text
Added Redis caching
Changed API authentication
Fixed README typo
Changed Docker configuration
Refactored logging
Changed database schema
```

and then create:

```bash
git commit -m "Changes"
```

This makes the history difficult to understand.

A better history might be:

```text
Add Redis embedding cache
Add inference request metrics
Refactor structured logging
Update Docker configuration
Fix authentication timeout
```

The benefit becomes obvious when debugging.

Suppose six months later you discover that Redis caching introduced a performance regression.

If the change is isolated into a commit, you can inspect it directly.

Git history becomes not merely storage for code but a **historical explanation of how the system evolved**.

---

# Branching Strategies

Branching becomes useful when multiple lines of development need to happen independently.

A typical workflow might look like:

```text
main
 |
 +── feature/embedding-cache
 |
 +── feature/authentication
 |
 +── bugfix/timeout
```

Each branch can evolve independently.

A feature branch might contain:

```text
A ── B ── C
          \
           D ── E ── F
```

while `main` continues:

```text
A ── B ── C ── G ── H
```

Eventually, the feature must be integrated.

That is where **merge** and **rebase** become important.

---

# Pull Requests Are a Collaboration Layer

A Pull Request is not itself a Git primitive.

It is a collaboration mechanism implemented by platforms such as GitHub and GitLab.

The underlying Git concepts are still:

```text
branches
commits
diffs
merges
rebases
```

A Pull Request adds collaboration features such as code review, automated checks, discussion, approvals, and controlled integration.

A professional workflow often looks like:

```text
Developer
    |
    v
Feature Branch
    |
    v
Commits
    |
    v
Push
    |
    v
Pull Request
    |
    +── Code Review
    +── Tests
    +── Security Scan
    +── Build
    |
    v
Merge
    |
    v
main
```

This is particularly important in production AI systems because changes to model configuration, inference code, dependencies, infrastructure, or deployment configuration should not normally enter production without validation.

---

# Now We Reach the Most Important Part: Merge Conflicts

A **merge conflict occurs when Git cannot automatically determine how to combine two sets of changes**.

This definition is important because many people incorrectly think:

> “A merge conflict means two people edited the same file.”

That is not necessarily true.

Two developers can modify the same file and Git may merge the changes automatically.

Conversely, conflicts can arise in more subtle situations involving renames, deletions, directory structures, binary files, rebases, cherry-picks, and changes whose semantic meaning cannot be safely inferred from text.

Git is fundamentally a tool that understands **changes to files**, not the business meaning of those changes.

---

# A Simple Merge Conflict

Imagine the original code is:

```python
timeout = 30
```

Developer A creates:

```python
timeout = 60
```

Developer B independently creates:

```python
timeout = 120
```

The histories become:

```text
             A
            /
Original
            \
             B
```

Git now has two competing modifications.

When you try to merge them, Git cannot automatically decide:

```text
60
```

or:

```text
120
```

should be the final value.

Therefore:

```text
CONFLICT (content)
```

appears.

Git's documentation describes this situation as a content conflict where the same file has been modified differently on the two sides. Git then leaves conflict information in the affected file and requires the developer to resolve it before the merge can complete. ([Git][2])

---

# What Does a Conflict Marker Mean?

Suppose Git produces:

```text
<<<<<<< HEAD
timeout = 60
=======
timeout = 120
>>>>>>> feature
```

These markers are extremely important.

The first section:

```text
<<<<<<< HEAD
timeout = 60
```

represents one side of the conflict.

The separator:

```text
=======
```

divides the two versions.

The second section:

```text
timeout = 120
```

represents the other side.

The final marker:

```text
>>>>>>> feature
```

identifies the other side of the operation.

Git's documentation shows this same fundamental conflict-marker model when an automatic merge cannot complete. ([Git][2])

---

# Resolving the Conflict

The human must decide what the correct application behavior should be.

Perhaps the correct solution is:

```python
timeout = 90
```

because the actual requirement is between the two competing changes.

You manually edit the file:

```python
timeout = 90
```

and remove the conflict markers.

Then:

```bash
git add model.py
```

This tells Git:

> “I have resolved this file.”

Finally, for a normal merge:

```bash
git commit
```

The Git documentation explicitly describes this workflow: resolve the affected files, update the index with `git add`, and then create the merge commit. ([Git][2])

---

# The Most Important Rule About Conflict Resolution

Never think:

> “Git says conflict, so I should just choose ours.”

or:

> “I'll choose theirs.”

Conflict resolution is fundamentally a **software correctness problem**, not merely a Git problem.

Suppose you have:

```python
max_tokens = 4096
```

on one branch and:

```python
max_tokens = 8192
```

on another.

Git cannot know that increasing the token limit might double GPU memory consumption.

Similarly, if one branch changes:

```python
batch_size = 32
```

and another changes:

```python
batch_size = 8
```

the correct answer depends on system requirements, GPU capacity, latency targets, and workload characteristics.

Therefore, conflict resolution requires understanding the intent behind both changes.

---

# The Major Types of Merge Conflicts

Merge conflicts can occur in several different ways.

The most obvious is a **same-line conflict**.

Suppose both branches change:

```python
timeout = 30
```

into different values.

That produces a direct content conflict.

But there are several other important cases.

---

# Case One: Same Lines Modified Differently

This is the classic conflict.

Original:

```python
timeout = 30
```

Branch A:

```python
timeout = 60
```

Branch B:

```python
timeout = 120
```

Git cannot determine which version should win.

Resolution:

```python
timeout = 90
```

or perhaps one of the two original values, depending on the actual requirement.

---

# Case Two: One Developer Deletes a Line and Another Modifies It

Imagine the original code is:

```python
timeout = 30
retries = 3
```

Developer A removes:

```python
retries = 3
```

Developer B changes it:

```python
retries = 5
```

Now Git must answer:

> Should the line remain with value `5`, or should it be deleted?

This is not necessarily a simple textual decision.

You must understand the intent of the two branches.

---

# Case Three: One Branch Deletes a File While Another Modifies It

Suppose:

```text
config.yaml
```

exists on both branches.

Branch A deletes it because configuration has moved to environment variables.

Branch B modifies it because it adds a new model parameter.

When the histories are combined, Git has a conceptual conflict:

```text
delete file
```

versus:

```text
modify file
```

You must decide whether the file should continue to exist.

---

# Case Four: File Renaming

Suppose one branch changes:

```text
model.py
```

to:

```text
inference_model.py
```

while another branch modifies `model.py`.

Git has to reason about whether the modification should apply to the renamed file.

Modern Git has rename detection mechanisms, but rename-related integration can still require human intervention.

The important lesson is that Git can often infer structural relationships, but it cannot guarantee semantic correctness.

---

# Case Five: Directory and File Conflicts

Imagine one branch contains:

```text
config/
```

while another branch creates:

```text
config
```

as a file.

Now the filesystem itself has conflicting structures.

One side wants:

```text
config/
    model.yaml
```

while the other wants:

```text
config
```

as a regular file.

This requires manual resolution because both structures cannot coexist at the same path.

---

# Case Six: Binary Files

Text files are relatively easy for Git to reason about because Git can display line-level differences.

Binary files are different.

Suppose two branches modify:

```text
model.onnx
```

or:

```text
image.png
```

Git generally cannot perform a meaningful line-based merge.

You may have to choose one version or use an external application-specific merging mechanism.

This is one reason large model artifacts generally should not be treated like ordinary source files in a Git repository.

---

# Case Seven: Dependency Conflicts

Consider:

```text
requirements.txt
```

Branch A:

```text
transformers==4.45.0
```

Branch B:

```text
transformers==4.55.0
```

The textual conflict is easy.

The difficult part is semantic.

Maybe your code depends on an API removed in `4.55.0`.

Or perhaps `4.55.0` fixes a security vulnerability.

Resolving the conflict therefore requires testing the dependency graph.

A correct resolution may involve:

```text
selecting one version
upgrading dependent packages
changing code
updating lock files
running tests
```

This illustrates a central principle:

**A Git conflict can be syntactically resolved but semantically incorrect.**

---

# Case Eight: Configuration Conflicts

Consider:

```yaml
batch_size: 32
```

versus:

```yaml
batch_size: 8
```

Git can resolve the textual difference if there is no conflict, but the resulting application behavior could still be wrong.

This is particularly important in ML infrastructure.

Configuration changes can affect:

```text
GPU memory
CPU utilization
latency
throughput
model quality
cost
autoscaling
```

Therefore, after resolving configuration conflicts, tests should validate behavior rather than merely checking that Git reports a clean working tree.

---

# Case Nine: Generated Files

Generated files can produce noisy conflicts.

For example:

```text
package-lock.json
poetry.lock
generated_client.py
protobuf-generated files
```

Two branches may modify the source configuration independently, producing incompatible generated outputs.

A common strategy is to resolve the underlying source files first and then regenerate the generated artifacts using the canonical build process.

Blindly selecting one generated file may silently discard changes.

---

# Case Ten: Semantic Conflicts

This is perhaps the most dangerous type because Git may not report a conflict at all.

Suppose Branch A changes:

```python
def predict():
    return model.generate()
```

and Branch B changes another part of the application:

```python
def preprocess():
    normalize_input()
```

Git may merge both changes perfectly.

But suppose Branch A changes the model input shape from:

```text
(batch, sequence)
```

to:

```text
(batch, channels, sequence)
```

while Branch B adds preprocessing that still produces the old shape.

Git may perform a clean merge.

The resulting program can nevertheless fail.

This is called a **semantic conflict**.

Git's clean merge does not mean your application is logically correct.

---

# A Critical Distinction: Textual Conflict vs Semantic Conflict

You should therefore distinguish:

```text
Git conflict
```

from:

```text
Application conflict
```

A Git conflict means:

> Git could not automatically construct a textual result.

A semantic conflict means:

> Git constructed a result, but the resulting software behavior may be incorrect.

This is why CI tests are so important.

---

# The Standard Conflict Resolution Workflow

Suppose you're on:

```text
feature/inference-cache
```

and want to integrate the latest `main`.

You might execute:

```bash
git fetch origin
git merge origin/main
```

Git attempts the merge.

If a conflict occurs:

```text
CONFLICT (content): Merge conflict in inference.py
Automatic merge failed; fix conflicts and then commit the result.
```

First inspect:

```bash
git status
```

Git tells you which files remain unresolved.

Then inspect the actual conflict:

```bash
git diff
```

You edit the files.

After resolving:

```bash
git add inference.py
```

Then verify:

```bash
git status
```

Finally:

```bash
git commit
```

The resulting merge commit records the integration.

Git's own documentation follows this general model: conflicting files are left in an unmerged state, the developer resolves them, stages the resolutions, and then commits the result. ([Git][2])

---

# What If You Realize You Made the Wrong Decision?

During a merge, you can abort the operation:

```bash
git merge --abort
```

This returns the repository to the state before the merge started, when Git can safely reconstruct that original state.

This is extremely useful when a conflict becomes too complicated and you want to restart from a clean state.

The important idea is:

```text
Start merge
    ↓
Conflict
    ↓
Try resolving
    ↓
Too complicated?
    ↓
git merge --abort
    ↓
Clean original state
```

---

# Conflict Resolution During Rebase

Now things become slightly different.

Suppose:

```text
A ── B ── C ── F ── G   main
     \
      D ── E             feature
```

You execute:

```bash
git switch feature
git rebase main
```

Git attempts to replay:

```text
D
E
```

on top of:

```text
G
```

Conceptually:

```text
A ── B ── C ── F ── G ── D' ── E'
```

The official Git documentation describes rebase as replaying commits from the current branch onto a new base, effectively transplanting a series of commits onto another starting point. ([Git][3])

If commit `D` causes a conflict, Git stops.

You resolve the conflict.

Then:

```bash
git add <resolved-file>
git rebase --continue
```

If another conflict appears during commit `E`, you resolve that one as well.

Eventually:

```text
D'
E'
```

are recreated on the new base.

---

# The Three Most Important Rebase Conflict Commands

During a conflicted rebase, you should understand these commands:

```bash
git rebase --continue
```

means:

> I resolved the current conflict; continue replaying the commits.

```bash
git rebase --skip
```

means:

> Do not replay the current commit.

This should be used only when you understand that the commit is unnecessary or its change is already represented elsewhere.

And:

```bash
git rebase --abort
```

means:

> Stop the rebase and return to the pre-rebase state.

These behaviors are explicitly documented by Git. ([Git][3])

---

# Why Rebase Conflicts Can Feel Confusing

During a normal merge, you are combining two histories.

During rebase, Git is replaying commits one at a time.

Suppose:

```text
main:
A ── B ── C

feature:
A ── B ── D ── E
```

and `D` changes:

```python
timeout = 30
```

to:

```python
timeout = 60
```

while `C` changed the same line to:

```python
timeout = 45
```

When Git replays `D` onto `C`, it encounters the conflict.

The conflict is therefore not simply:

```text
main vs feature
```

in the intuitive sense.

It is:

```text
new base
   +
replayed patch
```

This is why understanding the rebase model is essential.

---

# Merge Versus Rebase

The fundamental difference can be visualized as follows.

With merge:

```text
A ── B ── C ─────── M
     \             /
      D ── E ─────
```

With rebase:

```text
A ── B ── C ── D' ── E'
```

Merge preserves the original branch structure.

Rebase reconstructs the feature commits on top of a different base.

The official Git documentation describes rebase as transplanting commits onto another starting point, creating new commits such as `A'`, `B'`, and `C'`. ([Git][3])

---

# Why Rebase Rewrites History

Suppose commit `D` has a parent:

```text
B
```

After rebasing, the equivalent commit becomes:

```text
D'
```

whose parent is:

```text
C
```

Because the parent changed, the commit's identity changes.

Therefore:

```text
D != D'
```

even if the source-code change is conceptually identical.

This is why rebasing shared public history can cause problems.

---

# The Golden Rule of Rebase

A practical rule is:

> Rebase work that you control; avoid rewriting commits that other developers are already depending upon.

Suppose you have already pushed:

```text
feature
```

and another developer has based their branch on it.

If you execute:

```bash
git rebase main
git push --force
```

you may replace:

```text
D
E
```

with:

```text
D'
E'
```

and disrupt the other developer's history.

If you genuinely need to update a shared feature branch, use:

```bash
git push --force-with-lease
```

rather than blindly using:

```bash
git push --force
```

because `--force-with-lease` provides a safety check against overwriting unexpected remote updates.

---

# Reset Versus Revert

These commands are often confused.

Git's documentation makes an important distinction: `git reset` moves the branch tip, while `git revert` creates a new commit that reverses the changes introduced by another commit. ([Git][4])

Suppose:

```text
A ── B ── C
```

You discover that `C` is wrong.

Using:

```bash
git revert C
```

creates:

```text
A ── B ── C ── D
```

where `D` reverses `C`.

Using:

```bash
git reset --hard B
```

moves the branch back:

```text
A ── B
```

This distinction is fundamental.

For shared branches such as `main`, reverting is generally safer because it preserves history.

---

# Understanding Reset Modes

`git reset` has multiple modes.

With:

```bash
git reset --soft HEAD~1
```

Git moves the branch pointer backward while keeping your changes staged.

With:

```bash
git reset --mixed HEAD~1
```

Git moves the branch backward and leaves the changes in your working tree unstaged.

With:

```bash
git reset --hard HEAD~1
```

Git moves the branch backward and also updates the working tree to match the target commit.

The official documentation describes these modes in terms of how `HEAD`, the index, and the working tree are updated. ([Git][4])

---

# Cherry-Pick

Sometimes you don't want to merge an entire branch.

Suppose:

```text
main:
A ── B ── C

feature:
A ── B ── D ── E ── F
```

You only need `D`.

You can execute:

```bash
git cherry-pick D
```

Git applies the change introduced by `D` as a new commit on your current branch.

The Git documentation describes cherry-pick as taking the change introduced by an individual commit and attempting to reintroduce it as a new commit on the current branch. ([Git][5])

The resulting graph might become:

```text
A ── B ── C ── D'
```

This is particularly useful for production hotfixes.

---

# Cherry-Pick Can Also Produce Conflicts

Suppose commit `D` changes:

```python
timeout = 30
```

but your current branch already changed that line.

When you execute:

```bash
git cherry-pick D
```

Git may encounter a conflict.

The workflow is conceptually:

```text
git cherry-pick D
       ↓
conflict
       ↓
resolve
       ↓
git add
       ↓
git cherry-pick --continue
```

If you decide the commit shouldn't be applied:

```bash
git cherry-pick --abort
```

So conflict resolution isn't limited to `git merge`.

---

# Stash

Suppose you're halfway through implementing:

```text
feature/embedding-cache
```

and suddenly someone asks you to fix an urgent production issue.

Your working tree contains unfinished changes.

You can temporarily store them:

```bash
git stash
```

Then switch branches:

```bash
git switch main
```

Fix the production issue.

Afterward:

```bash
git switch feature/embedding-cache
git stash pop
```

Your unfinished changes return.

The important point is that stash is a temporary workflow mechanism, not a replacement for proper commits.

---

# Git Fetch Versus Git Pull

These commands are also frequently misunderstood.

When you run:

```bash
git fetch origin
```

Git downloads information from the remote and updates your remote-tracking references.

It does not automatically integrate those changes into your current branch.

For example:

```text
Remote:
A ── B ── C

Local:
A ── B
```

After:

```bash
git fetch
```

you might have:

```text
main       → B
origin/main → C
```

Your current branch has not necessarily changed.

`git pull` performs fetching plus an integration operation, commonly a merge or a rebase depending on configuration and options.

For example:

```bash
git pull --rebase
```

means that Git fetches remote changes and then rebases your local commits on top of them.

---

# Remote-Tracking Branches

A professional Git user should understand the difference between:

```text
main
```

and:

```text
origin/main
```

`main` is your local branch.

`origin/main` is a local reference representing the remote branch as last observed by your repository.

Conceptually:

```text
Your repository

main
 |
 v
B

origin/main
 |
 v
C

Remote repository
 |
 v
C
```

After another developer pushes:

```text
D
```

the actual remote becomes:

```text
C ── D
```

but your local `origin/main` won't know about `D` until:

```bash
git fetch
```

This is one of the reasons `git fetch` is such an important professional command.

---

# Git Reflog: Your Safety Net

Imagine you accidentally run:

```bash
git reset --hard HEAD~5
```

You might think:

> “Those commits are gone.”

Not necessarily.

Git maintains reflogs for local references.

Run:

```bash
git reflog
```

You might see:

```text
a8f31e7 HEAD@{0}: reset: moving to HEAD~5
91b20cd HEAD@{1}: commit: Add inference cache
72ac8aa HEAD@{2}: commit: Add metrics
```

You can often recover the previous state:

```bash
git reset --hard 91b20cd
```

This is one of the most powerful recovery techniques in Git.

---

# Git Bisect

Imagine your application worked last month but is broken now.

Your history contains:

```text
A
B
C
D
E
F
G
H
I
J
```

You know:

```text
A = good
J = bad
```

but you don't know which commit introduced the problem.

`git bisect` performs a binary search through the history.

You mark:

```bash
git bisect start
git bisect bad
git bisect good A
```

Git selects a midpoint.

You test it.

If it works:

```bash
git bisect good
```

If it fails:

```bash
git bisect bad
```

Git repeatedly narrows the range.

Mathematically, instead of checking `N` commits linearly, binary search needs approximately:

$$
\log_2(N)
$$

tests.

For 1024 commits:

$$
\log_2(1024)=10
$$

So you may identify the problematic commit in roughly ten tests rather than testing all 1024 commits.

---

# Git Blame

Suppose you find a strange line:

```python
batch_size = 4
```

You want to know why it exists.

Run:

```bash
git blame inference.py
```

Git can identify the commit that introduced or last modified the line.

Then:

```bash
git show <commit>
```

allows you to inspect the change.

This creates a powerful debugging chain:

```text
Problematic line
       ↓
git blame
       ↓
Commit
       ↓
git show
       ↓
Original change
       ↓
Developer intent
```

---

# Tags and Releases

When your system reaches a production release, you may create:

```bash
git tag -a v1.0.0 -m "Production release 1.0.0"
```

Now:

```text
A ── B ── C ── D
             ^
           v1.0.0
```

This creates a stable reference to the release.

You might later have:

```text
v1.0.0
v1.1.0
v1.2.0
v2.0.0
```

This is especially valuable for ML systems where reproducibility matters.

You want to know exactly which source-code state produced a particular deployed model service.

---

# Git and Machine Learning Projects

Git becomes especially interesting when applied to AI/ML systems.

Consider:

```text
ml-platform/
├── models/
├── inference/
├── training/
├── evaluation/
├── configs/
├── tests/
├── deployment/
├── Dockerfile
├── pyproject.toml
└── README.md
```

Your Git history might contain:

```text
Add embedding service
Add vector database integration
Add model caching
Add batch inference
Add GPU metrics
Add autoscaling configuration
Fix tokenizer compatibility
Upgrade transformers
Add evaluation pipeline
```

But you generally don't want Git itself to become the storage system for enormous datasets and model checkpoints.

Instead, Git should typically track:

```text
source code
configuration
infrastructure definitions
schemas
evaluation logic
deployment manifests
experiment definitions
```

while large artifacts can live in appropriate object storage, model registries, artifact registries, or dataset versioning systems.

---

# Merge Conflicts in an ML System

Consider this situation.

Branch A changes:

```yaml
batch_size: 32
```

Branch B changes:

```yaml
batch_size: 8
```

The Git conflict is trivial.

But the engineering question is not.

Suppose the production GPU only has 16 GB VRAM.

Perhaps:

```text
batch_size = 32
```

causes:

```text
CUDA out of memory
```

while:

```text
batch_size = 8
```

is stable.

Or perhaps Branch A was tested against an A100 while Branch B targets a T4.

Git cannot understand this.

The developer must resolve the conflict using system-level knowledge.

This is why professional Git usage requires more than knowing commands.

---

# How to Resolve Conflicts Correctly

The safest approach is to first understand the **common ancestor**.

Imagine:

```text
             A
            /
Base -------
            \
             B
```

The base represents the last point at which the two branches agreed.

Then ask:

```text
What did A change?
What did B change?
Why did A change it?
Why did B change it?
What should the final system behavior be?
```

Only then should you edit the conflicted file.

This approach is much safer than simply choosing:

```text
ours
```

or:

```text
theirs
```

without understanding the intent.

---

# `ours` and `theirs` Can Be Confusing During Rebase

There is another advanced detail worth understanding.

During a normal merge, people often think:

```text
ours = current branch
theirs = branch being merged
```

That mental model is useful for ordinary merges.

But during rebase, the interpretation can be different because Git is replaying commits onto a new base. The official rebase documentation explicitly notes that the meaning of "ours" and "theirs" is effectively swapped in the rebase context compared with the intuitive merge interpretation. ([Git][3])

Therefore, don't blindly execute:

```bash
git checkout --ours .
```

or:

```bash
git checkout --theirs .
```

during a rebase without first understanding which side represents the rebased series and which represents the new base.

---

# `git status` Is Your Best Friend During Conflicts

When something goes wrong, don't panic.

Run:

```bash
git status
```

Git usually tells you what operation is currently active.

You may see:

```text
You are currently rebasing
```

or:

```text
You have unmerged paths
```

or:

```text
All conflicts fixed but you are still merging
```

The status output tells you what Git expects next.

This is why professional Git usage involves repeatedly using:

```bash
git status
```

rather than trying to remember the repository's state mentally.

---

# A Complete Conflict Resolution Example

Suppose:

```text
main:

A ── B ── C
```

and:

```text
feature:

A ── B ── D
```

`C` changes:

```python
timeout = 30
```

to:

```python
timeout = 60
```

while `D` changes it to:

```python
timeout = 120
```

You execute:

```bash
git switch main
git merge feature
```

Git reports:

```text
CONFLICT (content): Merge conflict in config.py
Automatic merge failed; fix conflicts and then commit the result.
```

You inspect:

```bash
git status
```

Then:

```bash
git diff
```

You see:

```python
<<<<<<< HEAD
timeout = 60
=======
timeout = 120
>>>>>>> feature
```

You determine that the correct production value is:

```python
timeout = 90
```

You edit the file:

```python
timeout = 90
```

Then:

```bash
git add config.py
```

Now:

```bash
git status
```

should show that the conflict has been resolved.

Then:

```bash
git commit
```

creates the merge commit.

Finally, you should run the relevant test suite.

The important workflow is therefore:

```text
Detect
  ↓
Inspect
  ↓
Understand
  ↓
Resolve
  ↓
Stage
  ↓
Verify
  ↓
Test
  ↓
Commit
```

---

# Why Testing After Conflict Resolution Is Mandatory

This deserves special emphasis.

Suppose Git reports:

```text
Merge successful.
```

That does **not** mean:

```text
Application correct.
```

It only means:

```text
Git successfully constructed a repository state.
```

After resolving conflicts, you should run appropriate validation:

```bash
pytest
```

or:

```bash
ruff check .
```

or:

```bash
mypy .
```

or your integration tests.

For an ML system, you might additionally execute:

```text
model loading test
tokenizer compatibility test
inference smoke test
GPU memory test
evaluation regression test
API integration test
```

A conflict resolution should be treated as a code change.

---

# The Three Questions You Should Always Ask During a Conflict

When you encounter a conflict, don't immediately start deleting markers.

First ask:

**What was the common starting state?**

Then:

**What did my branch intentionally change?**

Then:

**What did the other branch intentionally change?**

Finally:

**What should the final behavior be?**

This converts conflict resolution from:

```text
"Which text should I keep?"
```

into:

```text
"What is the correct software behavior?"
```

That is the professional mindset.

---

# Preventing Merge Conflicts

The best conflict is the conflict you never create.

One of the strongest practices is to keep branches relatively short-lived.

Instead of:

```text
feature branch
     |
     | six weeks
     |
     | 400 commits
     v
merge
```

prefer:

```text
main
 |
 +── small feature
 |
 +── review
 |
 +── merge
```

Frequent synchronization with the target branch also reduces divergence.

If your team follows a rebase-oriented workflow, you might periodically execute:

```bash
git fetch origin
git rebase origin/main
```

on your private feature branch.

Alternatively, teams may prefer:

```bash
git fetch origin
git merge origin/main
```

The correct choice depends on the team's workflow.

---

# Keep Commits Small and Logical

Another powerful conflict-prevention mechanism is good commit design.

A commit that changes:

```text
model.py
config.yaml
README.md
Dockerfile
Terraform
database schema
```

all at once is difficult to review and difficult to integrate.

A commit focused on one logical change is much easier to reason about.

This is why the course emphasizes the concept of the **perfect commit** early in the professional Git workflow. ([YouTube][1])

---

# Avoid Mixing Refactoring With Feature Work

Imagine Developer A is implementing:

```text
Redis caching
```

while simultaneously refactoring the entire repository.

Their changes touch:

```text
50 files
```

Developer B is modifying the same system.

Now their feature change becomes much harder to merge.

A cleaner strategy is:

```text
Commit 1:
Refactor inference module

Commit 2:
Add Redis cache
```

This makes the changes easier to review and integrate.

---

# Avoid Unnecessary Formatting Changes

Suppose Developer A changes:

```text
indentation
line endings
formatting
imports
```

across 100 files.

Developer B modifies only:

```text
model.py
```

Now Git may produce enormous diffs.

Formatting changes increase the surface area for conflicts.

Formatting should therefore ideally be automated and standardized.

---

# Use CI as a Second Layer of Protection

A professional repository should not rely solely on developers resolving conflicts correctly.

A Pull Request might trigger:

```text
Unit Tests
     ↓
Integration Tests
     ↓
Static Analysis
     ↓
Security Scan
     ↓
Build
     ↓
Container Scan
     ↓
Deployment Validation
```

For an ML platform:

```text
Code
 ↓
Unit Tests
 ↓
Model Load Test
 ↓
Inference Test
 ↓
Latency Test
 ↓
Evaluation Regression
 ↓
Container Build
 ↓
Deployment
```

This catches semantic problems that Git itself cannot understand.

---

# Git's Three Different Meanings of "Undo"

One of the most important concepts to internalize is that "undo" isn't one operation.

If you want to change what is staged:

```bash
git restore --staged file.py
```

If you want to restore a working-tree file:

```bash
git restore file.py
```

If you want to move a branch backward:

```bash
git reset
```

If you want to create a new commit that reverses an old commit:

```bash
git revert
```

Git's documentation explicitly distinguishes `restore`, `reset`, and `revert`: restore operates on working-tree/index content, reset can move the branch tip, and revert creates a new commit reversing another commit. ([Git][6])

---

# The Professional Git Mental Model

At this point, you can connect almost everything.

Git is fundamentally:

```text
                    Git
                     |
          +----------+----------+
          |                     |
     Object Database        References
          |                     |
    +-----+-----+          +----+----+
    |     |     |          |         |
  blob  tree  commit      branch    tag
                  |
                  v
              Parent(s)
                  |
                  v
             Commit Graph
```

Your working process is:

```text
Working Tree
      |
      | git add
      v
Index
      |
      | git commit
      v
Commit Graph
      |
      | git fetch/push
      v
Remote Repository
```

And integration is:

```text
Feature Branch
      |
      +------------------+
      |                  |
    merge              rebase
      |                  |
      v                  v
Merge Commit        New Commits
      |                  |
      +--------+---------+
               |
               v
             main
```

Conflict resolution happens whenever Git cannot safely construct the required result automatically.

---

# The Most Important Git Commands to Master

You do not need to memorize every Git command.

Instead, understand these conceptual groups.

For inspecting repository state:

```bash
git status
git log
git log --graph --oneline --decorate --all
git diff
git diff --staged
git show
git blame
git reflog
```

For everyday development:

```bash
git add
git commit
git switch
git branch
git stash
```

For integrating branches:

```bash
git merge
git rebase
git cherry-pick
```

For remote collaboration:

```bash
git fetch
git pull
git push
git remote
```

For correcting history:

```bash
git reset
git restore
git revert
git rebase -i
```

For debugging:

```bash
git bisect
git blame
git reflog
git show
```

For releases:

```bash
git tag
```

The goal isn't command memorization.

The goal is knowing:

> **Which part of Git's state does this command modify?**

---

# The Entire Git Workflow in One Picture

A professional workflow can now be understood as:

```text
                         REMOTE REPOSITORY
                                |
                                | fetch
                                v
                       origin/main
                                |
                                v
                             main
                              |
                              |
                    +---------+---------+
                    |                   |
                    |                   |
              feature branch       bugfix branch
                    |                   |
                    v                   v
                 commits             commits
                    |                   |
                    +---------+---------+
                              |
                              v
                     merge / rebase /
                       cherry-pick
                              |
                              v
                         integration
                              |
                              v
                         Pull Request
                              |
                  +-----------+-----------+
                  |                       |
               CI/CD                 Code Review
                  |                       |
                  +-----------+-----------+
                              |
                              v
                            main
                              |
                              v
                           Release
                              |
                              v
                           v1.0.0
                              |
                              v
                         Production
```

When conflicts appear, the flow temporarily becomes:

```text
Integration
     |
     v
Conflict
     |
     v
git status
     |
     v
git diff
     |
     v
Understand both changes
     |
     v
Manually resolve
     |
     v
git add
     |
     v
Continue merge/rebase/cherry-pick
     |
     v
Run tests
     |
     v
Commit
```

That is the professional Git workflow.

---

# Final Perspective

The biggest mistake when learning Git is to memorize commands without understanding the underlying model.

You should instead think about Git in terms of **states, snapshots, references, and a commit graph**.

A branch is a reference.

A commit is a historical snapshot with ancestry.

`HEAD` identifies your current position.

The staging area lets you construct the next snapshot.

A merge combines histories.

A rebase reconstructs commits on top of another base.

A cherry-pick reapplies an individual commit's change.

A reset moves references and can alter local history.

A revert creates a new commit that reverses an earlier change.

A reflog records reference movements and can often rescue mistakes.

A merge conflict means Git cannot automatically determine the correct integration result.

And perhaps most importantly, **resolving a conflict is not simply choosing "ours" or "theirs."** It is determining the correct final behavior of the software after understanding what both branches were trying to accomplish.

That distinction becomes especially important in AI/ML engineering. A conflict involving `batch_size`, model versions, tokenizer behavior, inference configuration, GPU allocation, dependency versions, or deployment manifests may be textually simple but operationally significant. Git can tell you that two pieces of history disagree; it cannot tell you which configuration is safe for your production inference system.

The professional Git mindset is therefore:

```text
Git tells me what changed.
Git tells me where histories diverged.
Git helps me combine those histories.
But I, as the engineer, must determine whether
the resulting system is actually correct.
```

That is the point at which Git stops being merely a command-line tool and becomes an engineering discipline.

([YouTube][1])

[1]: https://www.youtube.com/watch?v=Uszj_k0DGsg&utm_source=chatgpt.com "Git for Professionals Tutorial - Tools & Concepts for Mastering Version Control with Git - YouTube"
[2]: https://git-scm.com/docs/user-manual?utm_source=chatgpt.com "Git - user-manual Documentation"
[3]: https://git-scm.com/docs/git-rebase?utm_source=chatgpt.com "Git - git-rebase Documentation"
[4]: https://git-scm.com/docs/git-reset?utm_source=chatgpt.com "Git - git-reset Documentation"
[5]: https://git-scm.com/book/en/v2/Appendix-C%3A-Git-Commands-Patching.html?utm_source=chatgpt.com "Git - Patching"
[6]: https://git-scm.com/docs/git?utm_source=chatgpt.com "Git - git Documentation"

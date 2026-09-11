# Git: A Deep Technical Guide to Version Control, Branching, Merging, and Conflict Resolution

Git is often introduced as a tool for saving versions of source code, but that description significantly undersells what Git actually provides. Git is a distributed version-control system designed around immutable objects, references, snapshots, and a directed acyclic graph of project history. Understanding these foundations changes the way developers use Git. Commands such as `commit`, `branch`, `merge`, `rebase`, `reset`, `revert`, and `cherry-pick` stop being isolated commands to memorize and instead become operations that manipulate a well-defined model of repository state.

This distinction becomes particularly important in collaborative software engineering. When several developers work simultaneously on the same codebase, their changes inevitably diverge. Git provides mechanisms for maintaining these independent lines of development and eventually integrating them. When Git cannot determine how changes should be combined automatically, a merge conflict occurs. Resolving such a conflict correctly requires considerably more than choosing one side of a file; it requires understanding the intent of the changes and validating the resulting system behavior.

## Understanding Git as a Version-Control System

Consider a software project containing an inference service:

```text
inference-service/
├── src/
│   ├── model.py
│   ├── inference.py
│   └── preprocessing.py
├── tests/
├── config/
│   └── production.yaml
├── Dockerfile
└── pyproject.toml
```

As development progresses, different versions of this project need to be preserved. Git represents this evolution through commits. A commit describes a particular state of the project and maintains a relationship with its parent commit.

A simple history therefore looks like:

```text
A ── B ── C ── D
```

Commit `A` represents the initial state, `B` introduces the next logical change, and subsequent commits continue the evolution of the repository.

However, real development rarely remains linear. When a developer creates a feature branch, the history becomes a graph:

```text
A ── B ── C
      \
       D ── E
```

The two branches share the history represented by `A` and `B`, but they subsequently evolve independently. Git's ability to represent this graph is fundamental to branching, merging, rebasing, and conflict resolution.

## The Working Tree, Index, and Repository

Git operates across several distinct states. The files that the developer currently sees and modifies constitute the working tree. The staging area, technically called the index, represents the content selected for the next commit. The Git repository stores the historical objects and references.

The resulting workflow can be visualized as:

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

Suppose a developer modifies three files:

```text
model.py
inference.py
README.md
```

but only the model implementation belongs in the next logical change. The developer can stage only `model.py`:

```bash
git add model.py
```

The subsequent commit therefore captures the intended change rather than every modification currently present in the working directory.

This is one of Git's most important design decisions. The staging area allows developers to construct precise, logically coherent commits.

## Commits and Git's Object Model

A Git repository is fundamentally an object database. Git stores several types of objects, including blobs, trees, commits, and annotated tags.

A simplified representation is:

```text
Commit
  |
  +── metadata
  |
  +── parent
  |
  +── tree
        |
        +── model.py      → blob
        +── inference.py  → blob
        +── config.yaml   → blob
```

A blob represents file contents. A tree represents directory structure and references other trees or blobs. A commit references a tree representing a project snapshot and also references its parent commit or commits.

This object model explains why Git history is naturally represented as a graph rather than as a sequence of copied directories.

## Branches as References

A Git branch is not an independent copy of the repository. It is essentially a movable reference to a commit.

Suppose the repository contains:

```text
A ── B ── C
         ^
        main
```

Creating a feature branch results in another reference pointing to the same commit:

```text
A ── B ── C
         ^   ^
       main feature
```

When development continues on the feature branch:

```text
A ── B ── C
          \
           D ── E
                ^
              feature
```

The `main` reference remains at `C`, while `feature` moves forward to `E`.

This makes branching inexpensive and explains why Git can support large numbers of short-lived branches without physically duplicating the entire project.

## HEAD and Repository Position

`HEAD` identifies the developer's current position within the repository. When working on a normal branch, the relationship can be represented as:

```text
HEAD
 |
 v
feature
 |
 v
E
```

Switching to `main` changes the reference:

```text
HEAD
 |
 v
main
 |
 v
C
```

A detached HEAD occurs when `HEAD` points directly to a commit rather than through a branch reference. This is useful when inspecting historical states or experimenting with previous versions, although commits created in such a state should generally be attached to a branch if they need to be retained.

## Why Merge Conflicts Exist

A merge conflict occurs when Git cannot automatically construct a correct combined result from two divergent lines of development.

Consider the following common ancestor:

```text
timeout = 30
```

Developer A changes it to:

```text
timeout = 60
```

while Developer B independently changes it to:

```text
timeout = 120
```

The repository history becomes:

```text
             A
            /
Base -------
            \
             B
```

Git knows that both changes originated from the same base, but it cannot determine whether the correct final value should be `60`, `120`, or some third value such as `90`.

The conflict is therefore not a failure of Git. It is an indication that the available information is insufficient to determine the intended semantic result automatically.

## Three-Way Merging

Git's merge algorithm can be understood using three versions of the relevant state: the common ancestor, the current branch, and the branch being integrated.

Conceptually:

```text
             Common Ancestor
                  |
          +-------+-------+
          |               |
          v               v
       Ours            Theirs
          \               /
           \             /
            \           /
              Merge
```

The common ancestor establishes the baseline. Git examines how each branch changed relative to that baseline and attempts to combine those changes.

If the changes affect independent portions of the file, Git can frequently combine them automatically.

For example, suppose the original file contains:

```python
timeout = 30
retries = 3
```

One branch changes:

```python
timeout = 60
```

while another changes:

```python
retries = 5
```

The final result can safely become:

```python
timeout = 60
retries = 5
```

because the changes affect independent regions.

A conflict occurs when the changes overlap in a way that prevents Git from determining the intended result.

## Major Categories of Merge Conflicts

The most obvious case occurs when two branches modify the same lines differently. However, conflicts can also occur when one branch deletes a line while another modifies it, when one branch deletes a file while another modifies it, or when branches perform incompatible renames.

File-system structure can also create conflicts. One branch may create a directory while another creates a file with the same path. Binary files present another challenge because traditional line-based merging is not applicable.

Dependency files are another frequent source of integration problems. Consider:

```text
Branch A:
transformers==4.45.0

Branch B:
transformers==4.55.0
```

Resolving the textual conflict is trivial. Determining the correct dependency version may not be. One version may be required for compatibility with an existing model, while another may contain an important security fix.

The most dangerous conflicts are semantic conflicts. Git can successfully merge two changes even though the resulting application is logically incorrect.

For example, one branch might change an inference API from:

```text
(batch, sequence)
```

to:

```text
(batch, channels, sequence)
```

while another branch introduces preprocessing that still produces the original shape. Git may report a completely clean merge even though the application now fails at runtime.

Therefore, a clean Git merge does not guarantee a correct software merge.

## Resolving a Merge Conflict

Suppose Git reports:

```text
CONFLICT (content): Merge conflict in inference.py
Automatic merge failed; fix conflicts and then commit the result.
```

The first step is not to edit the file immediately. The developer should inspect the repository state:

```bash
git status
```

This identifies the files that remain unresolved.

The conflicting file may contain markers such as:

```python
<<<<<<< HEAD
timeout = 60
=======
timeout = 120
>>>>>>> feature
```

These markers identify the competing versions.

The correct resolution is determined by engineering intent. Suppose analysis shows that the service should use a dynamically configured timeout. The developer may replace the conflicting section with:

```python
timeout = config.inference_timeout
```

The conflict markers must then be removed.

Once the file is correct, it is staged:

```bash
git add inference.py
```

The merge can then be completed:

```bash
git commit
```

However, staging the file only tells Git that the textual conflict has been resolved. It does not prove that the implementation is correct.

The developer should therefore run the appropriate validation suite:

```bash
pytest
```

and, depending on the project:

```bash
ruff check .
```

```bash
mypy .
```

Additional integration, performance, model-loading, and deployment tests may be necessary for an AI/ML system.

## Aborting a Merge

Sometimes a conflict is sufficiently complicated that continuing is not the safest option.

A merge can be abandoned with:

```bash
git merge --abort
```

This is useful when the developer wants to return to the state that existed before the merge began and approach the integration differently.

The important distinction is that aborting the merge does not solve the conflict. It simply restores the repository to a known state.

## Merge Conflicts During Rebase

Rebase produces a different style of integration problem.

Suppose:

```text
A ── B ── C
      \
       D ── E
```

and `main` advances to:

```text
A ── B ── C ── F ── G
      \
       D ── E
```

Rebasing the feature branch onto `G` asks Git to replay the feature commits on top of the new base:

```text
A ── B ── C ── F ── G ── D' ── E'
```

If Git cannot replay `D`, the rebase stops.

After resolving the conflict:

```bash
git add <resolved-file>
git rebase --continue
```

If the current commit should not be replayed:

```bash
git rebase --skip
```

If the entire operation should be abandoned:

```bash
git rebase --abort
```

The conceptual difference is important. A merge combines two histories into a new history, whereas a rebase reconstructs commits on top of another base.

## Merge Versus Rebase

Merge preserves the historical topology:

```text
A ── B ── C ───── M
      \           /
       D ── E ───
```

Rebase produces a linearized history:

```text
A ── B ── C ── D' ── E'
```

Neither approach is universally correct. Merge is valuable when preserving the exact branching history is important. Rebase is useful when a clean linear history improves readability and the commits being rewritten are under the developer's control.

The critical operational consideration is that rebasing changes commit identities. Consequently, rewriting shared history can disrupt developers who have already based work on the original commits.

## Reset and Revert

Git provides multiple mechanisms for undoing work, and they operate at different levels.

`git reset` can move a branch reference backward. For example:

```bash
git reset --soft HEAD~1
```

moves the branch while preserving the changes in the staging area.

A mixed reset:

```bash
git reset HEAD~1
```

moves the branch and leaves the changes in the working tree.

A hard reset:

```bash
git reset --hard HEAD~1
```

also changes the working tree to match the target commit and can therefore discard uncommitted changes.

`git revert` follows a fundamentally different model. Instead of removing a historical commit, it creates a new commit that reverses the earlier change:

```text
A ── B ── C ── D
             ^
          original

D reverses C
```

This makes revert particularly appropriate for shared branches because the existing history remains intact.

## Recovering From Mistakes With Reflog

Git provides a powerful local recovery mechanism called the reflog.

Suppose a developer accidentally performs a destructive reset. The normal `git log` may no longer show the commits that were previously reachable from the branch.

The reflog can reveal movements of the local references:

```bash
git reflog
```

A previous commit may appear in the output:

```text
91b20cd HEAD@{1}: commit: Add inference cache
```

The developer can then recover the previous state by moving the branch back to that commit.

This makes reflog an important safety mechanism when experimenting with reset, rebase, and other history-rewriting operations.

## Cherry-Picking Individual Changes

Sometimes an entire branch should not be integrated, but one particular commit is useful.

Suppose:

```text
main:
A ── B ── C

feature:
A ── B ── D ── E
```

If `D` contains an important production fix, it can be applied to `main` with:

```bash
git cherry-pick D
```

Git creates a new commit containing the change introduced by `D`.

Cherry-picking is useful for hotfixes, release branches, backports, and selectively moving changes between branches. It can also produce conflicts when the target branch has diverged from the context expected by the selected commit.

## Git as Part of a Production Engineering Workflow

Git becomes significantly more valuable when integrated into an engineering delivery pipeline.

A production-oriented workflow can look like:

```text
Developer
    |
    v
Feature Branch
    |
    v
Logical Commits
    |
    v
Pull Request
    |
    +---- Code Review
    |
    +---- Unit Tests
    |
    +---- Integration Tests
    |
    +---- Security Scanning
    |
    +---- Build Validation
    |
    +---- ML Evaluation
    |
    v
Merge
    |
    v
Release
    |
    v
Deployment
    |
    v
Observability
```

For AI/ML systems, validation should extend beyond ordinary unit tests. Changes involving model versions, tokenizers, inference parameters, batch sizes, GPU configuration, dependencies, and deployment manifests can produce failures that cannot be detected through textual Git analysis.

## Git and AI/ML Engineering

Consider an inference platform containing:

```text
ml-platform/
├── training/
├── inference/
├── evaluation/
├── models/
├── configs/
├── tests/
├── deployment/
├── Dockerfile
└── pyproject.toml
```

A Git commit should generally track source code, configuration, infrastructure definitions, evaluation logic, and reproducible build information.

Large datasets and model artifacts should generally be managed through systems designed for artifact and dataset management rather than treating Git as a massive binary-storage system.

The distinction is particularly important for reproducibility. A production deployment should ideally allow engineers to determine which source revision, configuration, model artifact, and dependency environment produced a particular deployment.

## The Core Mental Model

The entire system can ultimately be reduced to a few concepts:

```text
Working Tree
      |
      | add
      v
Index
      |
      | commit
      v
Commit Graph
      |
      +── branches
      +── tags
      +── HEAD
      |
      v
Integration
   /       \
merge     rebase
   |         |
   +----+----+
        |
        v
     Validated
      History
```

Once this model is understood, Git commands become operations on known pieces of state.

A branch creates or moves a reference. A commit records a snapshot and its ancestry. A merge combines divergent histories. A rebase reconstructs commits against another base. A reset changes where a reference points. A revert introduces a new inverse change. Cherry-pick reapplies a particular commit. Reflog records local reference movement. A merge conflict indicates that Git cannot safely determine the intended integration result automatically.

The most important lesson is that Git determines **how histories differ**, but the engineer determines **what the final system should mean**.

That distinction is what separates basic Git usage from professional version-control practice.

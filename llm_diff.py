import csv
from pydriller import Repository

BUG_KEYWORDS = [
    "fixed", "bug", "fixes", "fix"
]

def is_bug_fix_commit(message):
    if not message:
        return False
    msg_lower = message.lower()
    return any(keyword in msg_lower for keyword in BUG_KEYWORDS)

repo_path = "https://github.com/langchain-ai/langchain"  

with open("bug_fixes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow([
        "Hash", "Message", "Hashes of parents", "Is a merge commit?",
        "Filename", "Source Code (before)", "Source Code (current)", "Diff"
    ])
    print("Starting")
    for commit in Repository(repo_path).traverse_commits():
        print("Starting")
        print(
            'The commit {} has been modified by {}, '
            'committed by {} in date {}'.format(
                commit.hash,
                commit.author.name,
                commit.committer.name,
                commit.committer_date
            )
        )
        if is_bug_fix_commit(commit.msg):
            for mod in commit.modified_files:
                writer.writerow([
                    commit.hash,
                    (commit.msg or "").strip(),
                    " | ".join(commit.parents) if commit.parents else "",
                    "Yes" if len(commit.parents) > 1 else "No",
                    mod.filename or mod.new_path or mod.old_path or "",
                    mod.source_code_before or "",
                    mod.source_code or "",
                    mod.diff or ""
                ])

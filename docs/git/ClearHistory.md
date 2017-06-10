## 删除相关记录

git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch `path-to-your-remove-file`' --prune-empty --tag-name-filter cat -- --all

## 提交到远端

git push origin --force --all

## 其它客户端拉取

git pull --rebase

## GC

git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin

git reflog expire --expire=now --all

git gc --prune=now

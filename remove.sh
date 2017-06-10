declare -x FILE_NAME
declare -x REPLY

while [ "true" ]
do
    echo -n "Enter name:"
    read FILE_NAME
	if [ "$FILE_NAME" = "exit" ]
	then
		break
	fi
    git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch "$FILE_NAME"' --prune-empty --tag-name-filter cat -- --all
    echo -n "continue?(Y/N):"
    read REPLY
    if [ "$REPLY" = "Y" ] || [ "$REPLY" = "y" ]
    then
        git push origin --force --all
        git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
        git reflog expire --expire=now --all
        git gc --prune=now
    else
        git pull --rebase
    fi
done

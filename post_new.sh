if [ -z $1 ]; then
    echo "Usage $0 <file name>"
    exit 1
fi

URL="./_drafts/$1.md"
if [ -f $URL ]; then
    echo "File $1 exists!"
    rm $URL
    exit 2
fi

CUR_DATE=$(date +"%Y-%m-%d %T %z")
echo "---" > $URL
echo "layout: page" >> $URL
echo "title: $1" >> $URL
echo "date: $CUR_DATE" >> $URL
echo "mdate: $CUR_DATE" >> $URL
echo "---" >> $URL

if [ -z $1 ]; then
    echo "$(ls ./_drafts)"
    exit 0
fi

URL="./_drafts/$1.md"
if [ ! -f $URL ]; then
    echo "File $1 does not exist!"
    exit 2
fi

CUR_DATE=$(date +"%Y-%m-%d %T %z")
CUR_DATE_SIMPLE=$(date +"%Y-%m-%d" --date="$CUR_DATE")
sed -i "s/date: .*/date: $CUR_DATE/g" $URL
sed -i "s/mdate: .*/mdate: $CUR_DATE/g" $URL
mv $URL "./_posts/$CUR_DATE_SIMPLE-$1.md"

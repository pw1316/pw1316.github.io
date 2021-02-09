if [ -z $1 ]; then
    echo "$(ls ./_posts)"
    exit 0
fi

if [ ! -f $1 ]; then
    echo "File $1 does not exist!"
    exit 2
fi

CUR_DATE=$(date +"%Y-%m-%d %T %z")
sed -i "s/mdate: .*/mdate: $CUR_DATE/g" $1

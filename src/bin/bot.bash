
# This line sets the working directory to the directory containing this file
# So other scripts can be called from here
cd "$(dirname "${BASH_SOURCE[0]}")"

myName=$1
myTeam=$2
myIndex=$3

while true; do
    read packet

    echo '{"controls": { "throttle": 1 } }'
done


# This line sets the working directory to the directory containing this file
# So other scripts can be called from here
cd "$(dirname "${BASH_SOURCE[0]}")"

myName=$1
myTeam=$2
myIndex=$3

while true; do
    read packet

    ballX=$(echo "$packet" | sed -E -e "s/^.*ball\.location\.x=([^ ]*).*$/\1/g")
    ballY=$(echo "$packet" | sed -E -e "s/^.*ball\.location\.y=([^ ]*).*$/\1/g")

    mePosX=$(echo "$packet" | sed -E -e "s/^.*cars\.$myIndex\.location\.x=([^ ]*).*$/\1/g")
    mePosY=$(echo "$packet" | sed -E -e "s/^.*cars\.$myIndex\.location\.y=([^ ]*).*$/\1/g")

    meVelX=$(echo "$packet" | sed -E -e "s/^.*cars\.$myIndex\.velocity\.x=([^ ]*).*$/\1/g")
    meVelY=$(echo "$packet" | sed -E -e "s/^.*cars\.$myIndex\.velocity\.y=([^ ]*).*$/\1/g")

    # Find me to ball
    meToBallX=$((ballX-mePosX))
    meToBallY=$((ballY-mePosY))

    # Dot product of me to ball and (me velocity rotated 90 deg)
    dotX=$((meToBallX*meVelY))
    dotY=$((meToBallY*meVelX))
    dot=$((dotX-dotY))

    # Try to avoid orbits by using some handbrake
    xsq=$((meToBallX*meToBallX)) 
    ysq=$((meToBallY*meToBallY))
    dsq=$((xsq+ysq))
    hb="false"
    if [[ $dsq -lt 160000 ]]; then
        hb="true"
    fi

    # Steer should be the sign of the dot
    if [[ "$dot" == -* ]]; then
        steer="1"
    else
        steer="-1"
    fi
    echo "{\"controls\": { \"throttle\": 1, \"boost\": true, \"steer\": $steer, \"handbrake\": $hb }, \"log\": \"\" }"
    
done


# This line sets the working directory to the directory containing this file
# So other scripts can be called from here
cd "$(dirname "${BASH_SOURCE[0]}")"

myName=$1
myTeam=$2
myIndex=$3

locxMatch="cars.$myIndex.location.x=*"
locyMatch="cars.$myIndex.location.y=*"
velxMatch="cars.$myIndex.velocity.x=*"
velyMatch="cars.$myIndex.velocity.y=*"

while true; do
    read packet

    # Read values out of packet
    for val in $packet; do
        case $val in
            ball.location.x=*)
                ballX=${val#*=}
                ;;
            ball.location.y=*)
                ballY=${val#*=}
                ;;
            $locxMatch)
                mePosX=${val#*=}
                ;;
            $locyMatch)
                mePosY=${val#*=}
                ;;
            $velxMatch)
                meVelX=${val#*=}
                ;;
            $velyMatch)
                meVelY=${val#*=}
                ;;
        esac
    done

    # Find me to ball
    meToBallX=$((ballX-mePosX))
    meToBallY=$((ballY-mePosY))

    # Dot product of me to ball and (me velocity rotated 90 deg)
    dotX=$((meToBallX*meVelY))
    dotY=$((meToBallY*meVelX))
    dot=$((dotX-dotY))

    # Try to use some handbrake when close
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

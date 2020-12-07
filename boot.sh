if [[ $(pidof python run.py) ]];
then
    echo "run.py is already streaming!";
else
    echo "run.py is *NOT YET* running, so we'll start it up!";
    cd /home/pi/RobotKitLib/pikitlib/run.py
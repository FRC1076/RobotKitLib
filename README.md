* robot.py - robot-specific implementation of the typical FRC robot functions   (resident on Pi)
* run.py - the frc-like robot runtime that calls the entry points in robot.py  (resident on Pi)
* pikitlib.py - our replacement for (but look-alike) for wpilib functions that are robot specific.   (resident on Pi and laptop)
* driverstation.py - resident on the laptop.   Reads controls, maybe displays dashboard, enables/disables and sends control/commands to the robot.
* <>.py - other files needs to be integrated into the library.     (should not really be visible at the top layer, but they are there now for expediency)

Note for Windows users - In order to run create_archive.sh (and by extension, deploy.py), you will need to install a bash terminal such as Git Bash (https://git-scm.com/downloads, make sure to select download for Windows) and run the file from there.

The Freenove 4WD Raspberry Pi - based robot kit looks like a promising platform for software training.   This kits costs about $70, but requires a number of other components to be fully functional.
  * $35 Raspberry Pi 3B+
  * $10 32G SD-Card
  * $12 4 x 3.7V Lithium Ion Cells
  * $10 LI battery charger

I think it can also serve as a platform for design/mechanical and electrical to do some nice custom projects.

One limitation that we discovered right away is the software architecture seems very limiting for what we want to do with robot programming.   But, fortunately, everything is written in python, so fixing it up is certainly an option.

So we have kicked off a software project to make it programmable using the same robot.py kind of architecture that we are accustomed to.   This requires:
  * A driverstation application - at a minimum, this supports changing robot modes and driving or operating the robot using an XboxController.
  * A driver dashboard that can display information about the robot state (this could be Shuffleboard)
  * A replacement for the wpilib components that we all know and love.
    * XboxController object - receives the joystick state via NetworkTables from the driverstation and makes "button-pressed" and axis controller values visible using the same wpilib interface.
    * Motor controller objects, Speed Controller, and Drivetrains.
    * New sensor components and on-robot treats that will need object interfaces.

The task of creating this environment should be excellent training for returning students, and should help them understand a little what has maybe been "magic" before.


# RobotICP Assembly Documentation

# Software Testing

- On assembly run each file ending with [Lib.py](http://lib.py) to ensure that component is operating correctly
- Calibrate Variables depending on physical location of each component

    ### LinearRailLib.py

    ```python
    self.steps_per_syringe = 50000
    self.first_pos = 3600 * 5
    ```

    First change steps per syringe for the distance in number of steps between each syringe

    Secod first_pos is the number of steps to align the first syringe with the actuator

    ### ServoLib.py

    Change the duty cycle depending on starting angle and finishing angle of all press and relsease, depends on the mounting position

    ### PrinterLib.py

    ```python
    self.vialPickupPos = [70,103,6]
    self.tipPickupPos = [51,103,6]
    self.vialDropoffPos = [[25,50,40], 
                            [45,50,40], 
                            [75,50,40], 
                            [95,50,40], 
                            [95,74,40]]
    self.vialAcidDropoffPos = [[0,31,0], 
                            [25,31,0], 
                            [51,31,0], 
                            [73,31,0], 
                            [73,61,0]]

    self.dumpPos = [0,70,48]
    ```

    Change all of these coordinates depending on where they are located on the printer bed, Use Repetier to quickly find the coordinates of the components

    ### [PumpLib.py](http://pumplib.py)

    ```python
    self.dispense(40)
    ```

    Change the number in this for the amount of dead volume in the system to fill the pipes with adic
from enum import Enum
import picar
from picar import front_wheels,back_wheels
import time
import logging
from vlogging import VisualRecord

# from tensorflow.python.platform.tf_logging import log

class RobotState(Enum):
    Initial = 0
    MovingForward = 1
    TurningRight = 2
    TurningLeft = 3
    Stop = 4
    PreparedToTurnRight = 5
    PrepartedToTurnLeft = 6
 
class NeuralNetWorkRead(Enum):
    Unknown = -1
    Stop = 0
    Right = 1
    Left = 2
    Up = 3

class RobotRunner():
    def __init__(self, TimeToSteer = 6, LogInfo = False,forwardSpeed = 40,turnSpeed = 35, confidenceNeeded = 0.95):
        picar.setup()
        self.bw = back_wheels.Back_Wheels()
        self.fw = front_wheels.Front_Wheels()
        self.PreviousState = RobotState.Initial
        self.State = RobotState.Initial
        self.NNState = NeuralNetWorkRead.Unknown
        self.distance = 0
        self.confidence = 0
        self.confidenceNeeded = confidenceNeeded
        self.lastTime = time.time()
        self.curTime = time.time()
        self.timeDif = 0
        self.distanceToTurn = 35
        self.TimeToSteer = TimeToSteer
        self.FolderName = time.strftime("%Y%m%d-%H%M%S")
        self.LogInfo = LogInfo
        self.count = 0
        self.forwardSpeed = forwardSpeed
        self.turnSpeed = turnSpeed
        if(LogInfo):
            self.logger = logging.getLogger('./' + self.FolderName +'/logs.txt')
            fh = logging.FileHandler(self.FolderName + '.html',mode = "w")
            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(fh)
            

    def Update(self,NNState,distance,confidence,imageRead = None):
        self.count +=1
        self.NNState = NNState
        self.distance = distance
        self.confidence = confidence
        self.timeDif = self.curTime - self.lastTime
        if(self.LogInfo and imageRead is not None and self.count % 2 == 0):
            logText = f"Count :{self.count} State : {self.State} NN : {self.NNState} conf : {self.confidence} dist : {self.distance} timeElapsed : {self.timeDif}"
            self.logger.info(VisualRecord(logText,imageRead,str(self.count)))
    
    def countTimeInState(self,changedState : bool):
        self.curTime = time.time()
        if(changedState):
            self.lastTime = self.curTime
        self.timeDif = self.lastTime - self.curTime

    
    def PrintState(self):
        print(f'State : {self.State} NN : {self.NNState} conf : {self.confidence} dist : {self.distance} timeElapsed : {self.timeDif}')
    
    def Conf(self):
        return self.confidence >= self.confidenceNeed

    def UpdateState(self):
        self.PrintState()
        self.PreviousState = self.State
        if(self.State == RobotState.Initial or self.State == RobotState.Stop):
            if(self.NNState == NeuralNetWorkRead.Up and self.Conf()):
                self.State = RobotState.MovingForward
                print('changed to')
                self.PrintState()
        elif(self.State == RobotState.MovingForward):
            if(self.NNState == NeuralNetWorkRead.Stop and self.Conf() and self.distance < 20):
                self.State = RobotState.Stop
                print('changed to')
                self.PrintState()
            elif(self.NNState == NeuralNetWorkRead.Right and self.Conf()):
                self.State = RobotState.PreparedToTurnRight
                print('changed to')
                self.PrintState()
            elif(self.NNState == NeuralNetWorkRead.Left and self.Conf()):
                self.State = RobotState.PrepartedToTurnLeft
                print('changed to')
                self.PrintState()
            elif(self.distance < 10):
                self.State = RobotState.Stop
                print('changed to')
                self.PrintState()
        elif(self.State == RobotState.TurningRight or self.State == RobotState.TurningLeft):
            if(self.timeDif > self.TimeToSteer):
                self.State = RobotState.MovingForward
                print('changed to')
                self.PrintState()
        elif(self.State == RobotState.PrepartedToTurnLeft):
            if(self.NNState == NeuralNetWorkRead.Right and self.Conf()) :
                self.State = RobotState.PreparedToTurnRight
            elif(self.distance < self.distanceToTurn):
                self.State = RobotState.TurningLeft
                print('changed to')
                self.PrintState()
        elif(self.State == RobotState.PreparedToTurnRight):
            if(self.NNState == NeuralNetWorkRead.Left and self.Conf()) :
                self.State = RobotState.PreparedToTurnRight
            elif(self.distance < self.distanceToTurn):
                self.State = RobotState.TurningRight
                print('changed to')
                self.PrintState()
        self.countTimeInState(self.PreviousState != self.State)

    def RunState (self):
        if(self.State == RobotState.Initial or self.State == RobotState.Stop):
            self.bw.speed = 0
            self.fw.turn(90)
            self.bw.stop()
        elif(self.State == RobotState.MovingForward or self.State == RobotState.PreparedToTurnRight or self.State == RobotState.PrepartedToTurnLeft):
            self.fw.turn(90)
            self.bw.speed = self.forwardSpeed
            self.bw.backward()
        elif(self.State == RobotState.TurningLeft):
            self.fw.turn(45)
            self.bw.speed = self.turnSpeed
            self.bw.backward()
        elif(self.State == RobotState.TurningRight):
            self.fw.turn(45 + 90)
            self.bw.speed = self.turnSpeed
            self.bw.backward()
        

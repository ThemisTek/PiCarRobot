from enum import Enum
import picar
from picar import front_wheels,back_wheels


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
    def __init__(self):
        picar.setup()
        self.bw = back_wheels.Back_Wheels()
        self.fw = front_wheels.Front_Wheels()
        self.State = RobotState.Initial
        self.NNState = NeuralNetWorkRead.Unknown
        self.distance = 0
        self.confidence = 0
        self.confidenceNeed = 1

    def Update(self,NNState,distance,confidence):
        self.NNState = NNState
        self.distance = distance
        self.confidence = confidence
    
    def PrintState(self):
        print(f'State : {self.State} NN : {self.NNState} conf : {self.confidence} dist : {self.distance}')
    
    def Conf(self):
        return self.confidence >= self.confidenceNeed

    def UpdateState(self):
        self.PrintState()
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
            if(self.NNState == NeuralNetWorkRead.Stop and self.Conf()):
                self.State = RobotState.Stop
            elif(self.distance > 45):
                self.State = RobotState.MovingForward
                print('changed to')
                self.PrintState()
        elif(self.State == RobotState.PrepartedToTurnLeft):
            if(self.NNState == NeuralNetWorkRead.Right and self.Conf()) :
                self.State = RobotState.PreparedToTurnRight
            elif(self.distance < 25):
                self.State = RobotState.TurningLeft
                print('changed to')
                self.PrintState()
        elif(self.State == RobotState.PreparedToTurnRight):
            if(self.NNState == NeuralNetWorkRead.Left and self.Conf()) :
                self.State = RobotState.PreparedToTurnRight
            elif(self.distance < 25):
                self.State = RobotState.TurningRight
                print('changed to')
                self.PrintState()

    def RunState (self):
        if(self.State == RobotState.Initial or self.State == RobotState.Stop):
            self.bw.speed = 0
            self.bw.stop()
        elif(self.State == RobotState.MovingForward or self.State == RobotState.PreparedToTurnRight or self.State == RobotState.PrepartedToTurnLeft):
            self.fw.turn(90)
            self.bw.speed = 45
            self.bw.backward()
        elif(self.State == RobotState.TurningLeft):
            self.fw.turn(45)
            self.bw.speed = 35
            self.bw.backward()
        elif(self.State == RobotState.TurningRight):
            self.fw.turn(45 + 90)
            self.bw.speed = 35
            self.bw.backward()
        
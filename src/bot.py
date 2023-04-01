import json
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.messages.flat.QuickChatSelection import QuickChatSelection
from rlbot.utils.structures.game_data_struct import GameTickPacket

import subprocess
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

class MyBot(BaseAgent):

    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        # Create the bash subprocess
        self.bash = subprocess.Popen(
            [f"{os.getenv('ProgramFiles')}\\Git\\bin\\sh.exe", "-c", f"{dir_path}\\bin\\bot.bash {name} {team} {index}".replace("\\", "/")],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

    def initialize_agent(self):
        # Set up information about the boost pads now that the game is active and the info is available
        pass

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        """
        This function will be called by the framework many times per second. This is where you can
        see the motion of the ball, etc. and return controls to drive your car.
        """
        dict_packet = dict_from_packet(packet)
        self.bash.stdin.write((json.dumps(dict_packet) + "\n").encode("utf-8"))
        bash_output = self.bash.stdout.readline().decode()
        bash_controller = decode_output(bash_output)
        return bash_controller
    
def dict_from_packet(packet: GameTickPacket) -> dict:
    return {
        "ball": {
            "velocity": {
                "x": packet.game_ball.physics.velocity.x,
                "y": packet.game_ball.physics.velocity.y,
                "z": packet.game_ball.physics.velocity.z
            },
            "location": {
                "x": packet.game_ball.physics.location.x,
                "y": packet.game_ball.physics.location.y,
                "z": packet.game_ball.physics.location.z
            }
        },
        "cars": [
            {
                "velocity": {
                    "x": car.physics.velocity.x,
                    "y": car.physics.velocity.y,
                    "z": car.physics.velocity.z,
                },
                "location": {
                    "x": car.physics.location.x,
                    "y": car.physics.location.y,
                    "z": car.physics.location.z,
                },
                "rotation": {
                    "yaw": car.physics.rotation.yaw,
                    "pitch": car.physics.rotation.pitch,
                    "roll": car.physics.rotation.roll,
                }
            }
            for car in packet.game_cars
        ]
    }

def decode_output(output: str) -> SimpleControllerState:
    outjson = json.loads(output)
    return SimpleControllerState(
        steer=float(outjson["controls"].get("steer", 0)),
        throttle=float(outjson["controls"].get("throttle", 0)),
        pitch=float(outjson["controls"].get("pitch", 0)),
        yaw=float(outjson["controls"].get("yaw", 0)),
        roll=float(outjson["controls"].get("roll", 0)),
        jump=bool(outjson["controls"].get("jump", False)),
        boost=bool(outjson["controls"].get("boost", False)),
        handbrake=bool(outjson["controls"].get("handbrake", False))
    )

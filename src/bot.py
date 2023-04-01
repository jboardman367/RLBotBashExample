import json
from time import perf_counter
from typing import Any, List, Tuple, Union
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
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
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
        mangled_input = " ".join((i[0] + "=" + str(i[1]) for i in mangle_names(dict_packet)))
        tick = perf_counter()
        self.bash.stdin.write((mangled_input + "\n").encode("utf-8"))
        tock = perf_counter()
        print(f"input: {tock - tick}")  # >0.04 seconds atm
        tick = tock
        bash_output = self.bash.stdout.readline().decode()
        tock = perf_counter()
        print(f"output: {tock - tick}")  # >0.4 seconds atm
        bash_controller = decode_output(bash_output)
        return bash_controller
    
def dict_from_packet(packet: GameTickPacket) -> dict:
    return {
        "ball": {
            "velocity": {
                "x": int(packet.game_ball.physics.velocity.x),
                "y": int(packet.game_ball.physics.velocity.y),
                "z": int(packet.game_ball.physics.velocity.z),
            },
            "location": {
                "x": int(packet.game_ball.physics.location.x),
                "y": int(packet.game_ball.physics.location.y),
                "z": int(packet.game_ball.physics.location.z),
            }
        },
        "cars": [
            {
                "velocity": {
                    "x": int(car.physics.velocity.x),
                    "y": int(car.physics.velocity.y),
                    "z": int(car.physics.velocity.z),
                },
                "location": {
                    "x": int(car.physics.location.x),
                    "y": int(car.physics.location.y),
                    "z": int(car.physics.location.z),
                },
                "rotation": {
                    "yaw": int(car.physics.rotation.yaw),
                    "pitch": int(car.physics.rotation.pitch),
                    "roll": int(car.physics.rotation.roll),
                }
            }
            for car in packet.game_cars
        ]
    }

def decode_output(output: str) -> SimpleControllerState:
    outjson = json.loads(output)
    print(outjson.get("log", ""))
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

def mangle_names(input: Union[list, dict]) -> List[Tuple[str, Any]]:
    def mangle_names_step(step: Any) -> List[Tuple[List[str], Any]]:
        if isinstance(step, dict):
            arr = []
            for key in step:
                for pair in mangle_names_step(step[key]):
                    pair[0].append(key)
                    arr.append(pair)
            return arr
        elif isinstance(step, list):
            arr = []
            for i in range(len(step)):
                for pair in mangle_names_step(step[i]):
                    pair[0].append(str(i))
                    arr.append(pair)
            return arr
        else:
            return [([], step)]
    sets = mangle_names_step(input)
    return [
        (".".join(reversed(s[0])), s[1])
        for s in sets
    ]
# RLBotBashExample
Example of a Bash bot using the RLBot framework.
Based off the [python example](https://github.com/RLBot/RLBotPythonExample)

## Requirements
This bot assumes git bash is installed to the default location

## Changing the bot

- Bot behavior is controlled by `src/bin/bot.bash`
- Bot appearance is controlled by `src/appearance.cfg`

## Interface details

### Input

Input is supplied as a space-delimited list of key-value pairs seperated by `=`.

The key-value pairs are generated from name-mangling the following JSON to a fully-qualified
dot-seperated key for each value. e.g. key-value pair for the x velocity of the car at index 2
is `cars.2.velocity.x=412`

```json
// All numbers are provided as integers.
{
    "ball": {
        "location": {
            "x": 0,
            "y": 0,
            "z": 0
        },
        "velocity": {
            "x": 0,
            "y": 0,
            "z": 0
        }
    },
    "cars": [
        {
            "location": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            "velocity": {
                "x": 0,
                "y": 0,
                "z": 0
            },
            // Rotation components are scaled by 100 before rounding
            "rotation": {
                "yaw": 0,
                "pitch": 0,
                "roll": 0
            }
        },
        ...
    ]
}
```

### Output

Output should be returned by outputting a string to `stdout`, typically with `echo`.
The string should follow the below JSON format

```json
{
    "controls": {
        // All fields are optional and default to 0 or false
        "steer": 0.0,
        "throttle": 0.0,
        "pitch": 0.0,
        "yaw": 0.0,
        "roll": 0.0,
        "jump": false,
        "boost": false,
        "handbrake": false
    },
    // Optional, the string will be logged to the RLBot console.
    "log": ""
}

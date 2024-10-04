import gymnasium as gym
import numpy as np
import zmq

# Initialize ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)

# Bind the server socket to port 5555
socket.bind("tcp://localhost:5555")

# Initialize the CarRacing environment
env = gym.make("CarRacing-v2", render_mode="human")
observation, info = env.reset()

# Define discrete actions
discrete_actions = [
    np.array([0.0, 0.0, 0.0]),  # No action
    np.array([-1.0, 0.0, 0.0]),  # Steer left
    np.array([1.0, 0.0, 0.0]),  # Steer right
    np.array([0.0, 1.0, 0.0]),  # Accelerate
    np.array([0.0, 0.0, 1.0]),  # Brake
    np.array([-1.0, 1.0, 0.0]),  # Steer left + Accelerate
    np.array([1.0, 1.0, 0.0]),  # Steer right + Accelerate
    np.array([-1.0, 0.0, 1.0]),  # Steer left + Brake
    np.array([1.0, 0.0, 1.0]),  # Steer right + Brake
]

# Server loop to process incoming requests
while True:
    # Wait for the next request from the client
    message = socket.recv_json()

    if not isinstance(message, dict):
        msg = "Expected message to be a dictionary"
        raise TypeError(msg)

    if message["command"] == "reset":
        observation, info = env.reset()
        socket.send_json({"observation": observation.tolist()})

    elif message["command"] == "step":
        action_index = message["action"]
        if isinstance(action_index, int) and 0 <= action_index < len(discrete_actions):
            action = discrete_actions[action_index]
            observation, reward, done, truncated, info = env.step(action)
            socket.send_json(
                {"observation": observation.tolist(), "reward": reward, "done": done, "truncated": truncated}
            )
        else:
            msg = "Invalid action index received"
            raise ValueError(msg)

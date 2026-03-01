import time


def log_decision(input_text: str, agent_name: str, layer: str):
    print({
        "input": input_text,
        "agent": agent_name,
        "layer": layer,
        "timestamp": time.time()
    })

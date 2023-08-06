import sys
import os

currentPath = os.path.dirname(os.path.realpath(__file__))
parentPath = os.path.dirname(currentPath)
sys.path.append(parentPath)

from hanabi_learning_environment.agents.simple_agent import SimpleAgent

from badagent import Bad_Agent
from runner import Runner


if __name__ == '__main__':
    
    runner = Runner()
    runner.Run()

    flags = {'players': 2, 'num_episodes': 1, 'agent_class': 'HatAgent'}

    agent1 = SimpleAgent({'players': flags['players']}, 'Agent1')
    agent2 = SimpleAgent({'players': flags['players']}, 'Agent2')

    agenten = [agent1, agent2]

    for agent in agenten:
        agent.SayHello();
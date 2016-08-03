import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import pandas as pd
class QLearnAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(QLearnAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.Qdict = dict()
        #self.Qdict  = pd.DataFrame()
        self.state        = None   
        self.new_waypoint = None
        self.newState     = None
        self.action       = None
        self.alpha       = 0.9
        self.gamma       = 0.2
        self.epsilon     = 0.01
        self.reward      = 0
        self.totalReward = 0

    def getQ(self, state, action): # build up a state/action matrix
        #key = (tuple(state.items()),action)
        key = (state,action)
        return self.Qdict.get(key, 0.0)

    def MaxQ(self, state): # based on the action, get the maximized Q
        Q = [self.getQ(state,act) for act in Environment.valid_actions]
        return max(Q)
    
    def getAction(self, state): # when Q is maximized, get the action
        if random.random() < self.epsilon:
            action = random.choice(Environment.valid_actions)
        else:
            Q = [self.getQ(state,act) for act in Environment.valid_actions]
            good_act = []
            if Q.count(max(Q)) > 1: # if good option is more than 1
                #good_act = [i for i in range(len(Environment.valid_actions)) if Q[i] == max(Q)]
                for i in range(len(Environment.valid_actions)):
                    if Q[i] == max(Q):
                        good_act.append(i)
                index = random.choice(good_act) #random pick one as action
            else:
                index = Q.index(max(Q))
            action = Environment.valid_actions[index]
        return action

    def Qlearn(self, state, action, reward, newState):
        key = (state,action)
        #key = (tuple(state.items()),action)
        if not self.Qdict.has_key(key):
            self.Qdict[key] = 0.0
        else:   
            self.Qdict[key] = (1 - self.alpha) * self.Qdict[key] + self.alpha * (reward + self.gamma * self.MaxQ(newState))

    def reset(self, destination=None):

        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.state       = None
        self.newState    = None
        self.action      = None
        self.next_waypoint = None
        self.totalReward = 0 
        self.reward      = 0

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.newState = inputs
        self.newState['next_waypoint'] = self.next_waypoint
        self.newState = tuple(self.newState.items())
        # TODO: Select action according to your policy
        newAction = self.getAction(self.newState)
        
        # Execute action and get reward
        newReward = self.env.act(self, newAction)

        if self.env.done == True:
            print "total steps ", t
            print "total rewards ", self.totalReward

        # TODO: Learn policy based on state, action, reward
        if self.reward != None:
            self.Qlearn(self.state, self.action, self.reward, self.newState)
        # set the state to newState
        self.state = self.newState
        # set the reward to newReward
        self.reward = newReward
        # set action to action for newState
        self.action = newAction
        self.totalReward += newReward
        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, self.action, self.reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(QLearnAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.001, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()

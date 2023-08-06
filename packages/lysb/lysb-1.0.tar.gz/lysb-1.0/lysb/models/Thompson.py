import numpy as np
import matplotlib.pyplot as plt
from ..templates.Bandits import *

class Thompson_arm(Bandit_arm):
    """This class is responsible for simulating individual bandit hands running the Thompson's algorithm.
    """
    
    
    def __init__(self):

        self.N = 0
        self.alpha = 0
        self.beta = 1
        self.rewards = []
        self.mu = 0
        
    def pull(self):
        """Simulates the Thompson bandit hand pull.
        """
        precision = np.random.gamma(self.alpha, 1/self.beta)
        if precision == 0 or self.N == 0: precision = 0.001
        estimated_variance = 1/precision
        return np.random.normal( self.mu, np.sqrt(estimated_variance))

    
    def update(self,reward):        
        """Updates the parameters of Thomposon Bandit

        Parameters
        ----------
        reward : float
            The reward value of the selected bandit.

        Returns
        -------
        None

        """
        self.alpha = self.alpha + 1/2     
        self.beta= self.beta + ((self.N/(self.N + 1)) * (((reward - self.mu)**2)/2))

        self.v_0 = self.beta / (self.alpha + 1)      

        self.rewards.append(reward)
        self.N += 1
        self.mu = np.mean(self.rewards) 


class Thompson(Bandit):
    """Main Thompson bandit implementation that is trained on real-time input for decision making.
    """
    
    def __init__(self, num_bandits, num_features, alpha):
        
        self.bandits = [Thompson_arm() for i in range(num_bandits)]
        self.alpha = alpha
        self.last_pull = None
        self.last_context = []
        self.reward_collector = []
        
    def ask(self,context): 
        """Returns the best choice bandit per given context.

        Parameters
        ----------
        context : list
            corresponds to the features of the user providing the context for the bandits.
            

        Returns
        -------
        last_pull: int
            The id of the last pulled bandit.
        """
        
        self.last_pull = np.argmax([bandit.pull() for bandit in self.bandits])
        self.last_context = context
        
        return self.last_pull
    
    def update(self,reward):
        """Updates the parameters of Thompson bandits.

        Parameters
        ----------
        reward : float
            The reward value of the selected bandit.
            

        Returns
        -------
        None

        """
        assert ((self.last_pull != None) and  (len(self.last_context) != 0))
        self.bandits[self.last_pull].update(reward)
        self.last_pull = None
        self.last_context = []
        if len(self.reward_collector)==0:
            self.reward_collector.append(reward)
        else:
            self.reward_collector.append(self.reward_collector[-1]+reward)
        
    def plot(self):
        """Plots the performance of the model.
        """
        fig = plt.figure(figsize = (10, 5))

        plt.plot([i for i in range(len(self.reward_collector))], self.reward_collector,label=f"{self.__class__.__name__}") # plot cumsum per bandit.

        plt.legend()
        plt.xlabel("Timestep")
        plt.ylabel("Log Cummulative Reward")
        plt.title("Log Commulative Reward of thompson Over Time")
        plt.yscale("log")
        plt.show()  


class thompson_test_experiment_manager(Bandit_Experiment_Manager):
    """This class is responsible for running singular Thompson bandit experiments.
    """
    
    def __init__(self, user_contexts, bandit_contexts, num_iterations):
        
        self.user_contexts = user_contexts
        self.bandit_contexts = bandit_contexts
        self.num_iterations = num_iterations
        self.bandits = [Thompson_arm() for i in range(len(self.bandit_contexts))]
        self.reward_matrix = self.user_contexts @ self.bandit_contexts.T
        self.optimal_reward_per_user  = np.max(self.reward_matrix, axis=1)
        
        self.reward_per_user = [[] for i in self.user_contexts]
        self.num_optimal = 0

        self.experiment_indicator = False
        
    def experiment(self):
        """Performs the experiments and collects the metrics.
        """
        self.experiment_indicator = True
        
        
        for iter_ in range(self.num_iterations):
            for user in range(len(self.user_contexts)):
                
                current_context = self.user_contexts[user]
                chosen_bandit = np.argmax([bandit.pull() for bandit in self.bandits])
                reward = self.reward_matrix[user][chosen_bandit]
                self.reward_per_user[user].append(reward)
                
                if self.optimal_reward_per_user[user] == reward: self.num_optimal+=1
                    
                
                self.bandits[chosen_bandit].update(reward)
        
        print("Number of optimal choices made:",self.num_optimal)
        
        per_user_optimal_reward_estimate = [np.mean(bandit.rewards) for bandit in self.bandits]
                
        return np.array(per_user_optimal_reward_estimate)


    def plot(self):
        """Plots the performance of the model.
        """
        assert self.experiment_indicator == True
        
        fig = plt.figure(figsize = (10, 5))

        plt.subplot(1,2,1)
        for it in range(len(self.reward_per_user)):
            plt.plot([i for i in range(len(self.reward_per_user[it]))], np.cumsum(self.reward_per_user[it]),label=f"user{it}") # plot cumsum per bandit.
            
        plt.legend()
        plt.xlabel("Timestep")
        plt.ylabel("Log Cummulative Reward")
        plt.title("Log Commulative Reward of LinUCB Over Time")
        plt.yscale("log")

        plt.subplot(1,2,2)
        plt.bar(["Optimal", "Non-optimal"],[self.num_optimal,self.num_iterations*len(self.user_contexts)-self.num_optimal],label="Thompson")
        plt.legend()
        plt.ylabel("#optimal choices")
        plt.title("Number of optimal choices during the experiment")

        plt.show() 
        
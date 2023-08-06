import numpy as np
import matplotlib.pyplot as plt
from ..templates.Bandits import *


class linucb_arm(Bandit_arm):
    """This class is responsible for simulating individual bandit hands running the LinUCB algorithm.
    """
    
    
    def __init__(self, num_features, alpha):
        
        self.num_features=num_features
        self.alpha = alpha
        self.A = np.identity(num_features)
        self.b = np.zeros([num_features,1])
        
    def pull(self, context):
        """Simulates the LinUCB bandit hand pull.

        Parameters
        ----------
        context : list
            corresponds to the features of the user providing the context for the bandits.

        Returns
        -------
        reward_ucb: float
            The returned reward of the selected bandit.

        """
        context=context.reshape(-1,1) # transforming context into column vector for mathematical consistency
        A_inv = np.linalg.inv(self.A)
        theta = A_inv@self.b
        reward_ucb = theta.T@context + self.alpha * np.sqrt(context.T @ A_inv @ context)
        
        return reward_ucb
    
    def update(self,context,reward):
        """Updates the parameters of LinUCB

        Parameters
        ----------
        context : list
            corresponds to the features of the user providing the context for the bandits.
            
        reward : float
            The reward value of the selected bandit.

        Returns
        -------
        None

        """
        context = context.reshape(-1,1)
        self.A=self.A+context@context.T
        self.b=self.b+reward*context


class linUCB(Bandit):
    """Main LinUCB implementation that is trained on real-time input for decision making.
    """
    
    def __init__(self, num_bandits, num_features, alpha):
        
        self.bandits = [linucb_arm(num_features,alpha) for i in range(num_bandits)]
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
        
        self.last_pull = np.argmax([bandit.pull(context) for bandit in self.bandits])
        self.last_context = context
        
        return self.last_pull
    
    def update(self,reward):
        """Updates the parameters of LinUCB bandits.

        Parameters
        ----------
        reward : float
            The reward value of the selected bandit.
            

        Returns
        -------
        None

        """
        assert ((self.last_pull != None) and  (len(self.last_context) != 0))
        self.bandits[self.last_pull].update(self.last_context,reward)
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
        plt.title("Log Commulative Reward of LinUCB Over Time")
        plt.yscale("log")
        plt.show()  


class linucb_test_experiment_manager(Bandit_Experiment_Manager):
    """This class is responsible for running singular LinUCB experiments.
    """
    
    def __init__(self, user_contexts, bandit_contexts, num_iterations, alpha):
        
        self.user_contexts = user_contexts
        self.bandit_contexts = bandit_contexts
        self.num_iterations = num_iterations
        self.bandits = [linucb_arm(len(self.user_contexts[0]),alpha) for i in range(len(self.bandit_contexts))]
        self.reward_matrix = self.user_contexts @ self.bandit_contexts.T
        self.optimal_reward_per_user  = np.max(self.reward_matrix, axis=1)
        
        self.reward_per_user = [[] for i in self.user_contexts]
        self.num_optimal=0
        self.experiment_indicator = False
        
    def experiment(self):
        """Performs the experiments and collects the metrics.
        """
        self.experiment_indicator = True
        
        for iter_ in range(self.num_iterations):
            for user in range(len(self.user_contexts)):
                
                current_context = self.user_contexts[user]
                chosen_bandit = np.argmax([bandit.pull(current_context) for bandit in self.bandits])
                reward = self.reward_matrix[user][chosen_bandit]
                self.reward_per_user[user].append(reward)
                
                if self.optimal_reward_per_user[user] == reward: self.num_optimal+=1
                    
                
                self.bandits[chosen_bandit].update(current_context,reward)
        
        print("Number of optimal choices made:",self.num_optimal)
        
        per_user_optimal_reward_estimate = []
        for user in range(len(self.user_contexts)):
                current_context = self.user_contexts[user]
                per_user_optimal_reward_estimate.append(np.max([bandit.pull(current_context) for bandit in self.bandits]))
                
        return np.array(per_user_optimal_reward_estimate)
    
    def plot(self):
        """Plots the performance of the model.
        """
        assert self.experiment_indicator==True
        
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
        plt.bar(["Optimal", "Non-optimal"],[self.num_optimal,self.num_iterations*len(self.user_contexts)-self.num_optimal],label=f"LinUCB")
        plt.legend()
        plt.ylabel("#optimal choices")
        plt.title("Number of optimal choices during the experiment")

        plt.show() 
        
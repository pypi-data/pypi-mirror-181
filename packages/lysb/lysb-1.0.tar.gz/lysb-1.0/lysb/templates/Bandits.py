from abc import ABC, abstractmethod



class Bandit_arm(ABC):
    """This abstract class is responsible for simulating individual bandit hands running the given algorithm.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def pull(self):
        """Simulates the bandit hand pulls.
        """
        pass

    @abstractmethod
    def update(self,reward):
        """Updates the parameters of given Bandit

        Parameters
        ----------
        reward : float
            The reward value of the selected bandit.

        Returns
        -------
        None

        """
        pass


class Bandit(ABC):
    """Main bandit implementation that is trained on real-time input for decision making.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def ask(self, context):
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def plot(self):
        """ """
        pass

class Bandit_Experiment_Manager(ABC):
    """This abstract class is responsible for running singular bandit experiments.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def experiment(self):
        """Performs the experiments and collects the metrics.
        """
        pass

    @abstractmethod
    def plot(self):
        """Plots the performance of the model.
        """
        pass
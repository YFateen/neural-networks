import numpy as np

import backend
import nn


class Model(object):
    """Base model class for the different applications"""

    def __init__(self):
        self.get_data_and_monitor = None
        self.learning_rate = 0.0

    def run(self, x, y=None):
        raise NotImplementedError("Model.run must be overriden by subclasses")

    def train(self):
        """
        Train the model.

        `get_data_and_monitor` will yield data points one at a time. In between
        yielding data points, it will also monitor performance, draw graphics,
        and assist with automated grading. The model (self) is passed as an
        argument to `get_data_and_monitor`, which allows the monitoring code to
        evaluate the model on examples from the validation set.
        """
        for x, y in self.get_data_and_monitor(self):
            graph = self.run(x, y)
            graph.backprop()
            graph.step(self.learning_rate)


class RegressionModel(Model):
    """
    TODO: Question 4 - [Application] Regression

    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """

    def __init__(self):
        Model.__init__(self)
        self.get_data_and_monitor = backend.get_data_and_monitor_regression

        # Remember to set self.learning_rate!
        # You may use any learning rate that works well for your architecture
        "*** YOUR CODE HERE ***"
        self.learning_rate = .025
        self.hiddenLayerSize = 50

        self.W1 = nn.Variable(1, self.hiddenLayerSize)
        self.b1 = nn.Variable(self.hiddenLayerSize)
        self.W2 = nn.Variable(self.hiddenLayerSize, 1)
        self.b2 = nn.Variable(1)

    def run(self, x, y=None):
        """
        TODO: Question 4 - [Application] Regression

        Runs the model for a batch of examples.

        The correct outputs `y` are known during training, but not at test time.
        If correct outputs `y` are provided, this method must construct and
        return a nn.Graph for computing the training loss. If `y` is None, this
        method must instead return predicted y-values.

        Inputs:
            x: a (batch_size x 1) numpy array
            y: a (batch_size x 1) numpy array, or None
        Output:
            (if y is not None) A nn.Graph instance, where the last added node is
                the loss
            (if y is None) A (batch_size x 1) numpy array of predicted y-values

        Note: DO NOT call backprop() or step() inside this method!
        """
        "*** YOUR CODE HERE ***"
        theGraph = nn.Graph([self.W1, self.b1, self.W2, self.b2])
        xNode = nn.Input(theGraph, x)

        # f(x) = relu(x * W1 + b1) * W2 + b2
        xW1 = nn.MatrixMultiply(theGraph, xNode, self.W1)
        xW1pB = nn.MatrixVectorAdd(theGraph, xW1, self.b1)
        relu = nn.ReLU(theGraph, xW1pB)
        reluW2 = nn.MatrixMultiply(theGraph, relu, self.W2)
        fx = nn.MatrixVectorAdd(theGraph, reluW2, self.b2)

        if y is not None:
            # At training time, the correct output `y` is known.
            # Here, you should construct a loss node, and return the nn.Graph
            # that the node belongs to. The loss node must be the last node
            # added to the graph.
            "*** YOUR CODE HERE ***"
            yNode = nn.Input(theGraph, y)
            nn.SquareLoss(theGraph, yNode, fx)
            return theGraph
        else:
            # At test time, the correct output is unknown.
            # You should instead return your model's prediction as a numpy array
            "*** YOUR CODE HERE ***"
            return theGraph.get_output(fx)


class OddRegressionModel(Model):
    """
    TODO: Question 5 - [Application] OddRegression

    A neural network model for approximating a function that maps from real
    numbers to real numbers.

    Unlike RegressionModel, the OddRegressionModel must be structurally
    constrained to represent an odd function, i.e. it must always satisfy the
    property f(x) = -f(-x) at all points during training.
    """

    def __init__(self):
        Model.__init__(self)
        self.get_data_and_monitor = backend.get_data_and_monitor_regression

        # Remember to set self.learning_rate!
        # You may use any learning rate that works well for your architecture
        "*** YOUR CODE HERE ***"
        self.learning_rate = .050
        self.hiddenLayerSize = 100

        self.W1 = nn.Variable(1, self.hiddenLayerSize)
        self.b1 = nn.Variable(self.hiddenLayerSize)
        self.W2 = nn.Variable(self.hiddenLayerSize, 1)
        self.b2 = nn.Variable(1)

    def run(self, x, y=None):
        """
        TODO: Question 5 - [Application] OddRegression

        Runs the model for a batch of examples.

        The correct outputs `y` are known during training, but not at test time.
        If correct outputs `y` are provided, this method must construct and
        return a nn.Graph for computing the training loss. If `y` is None, this
        method must instead return predicted y-values.

        Inputs:
            x: a (batch_size x 1) numpy array
            y: a (batch_size x 1) numpy array, or None
        Output:
            (if y is not None) A nn.Graph instance, where the last added node is
                the loss
            (if y is None) A (batch_size x 1) numpy array of predicted y-values

        Note: DO NOT call backprop() or step() inside this method!
        """
        "*** YOUR CODE HERE ***"

        theGraph = nn.Graph([self.W1, self.b1, self.W2, self.b2])
        xNode = nn.Input(theGraph, x)
        neg_xNode = nn.Input(theGraph, -x)
        negMat = nn.Input(theGraph, np.matrix([-1.0]))

        # f(x) = relu(x * W2 + b1) * W2 + b2
        xW1 = nn.MatrixMultiply(theGraph, xNode, self.W1)
        xW1pB = nn.MatrixVectorAdd(theGraph, xW1, self.b1)
        relu = nn.ReLU(theGraph, xW1pB)
        reluW2 = nn.MatrixMultiply(theGraph, relu, self.W2)
        W2b2 = nn.MatrixVectorAdd(theGraph, reluW2, self.b2)

        # -f(-x) = -1 *(relu(-x * W2 + b1) * W2 + b2)
        neg_xW1 = nn.MatrixMultiply(theGraph, neg_xNode, self.W1)
        neg_xW1pB = nn.MatrixVectorAdd(theGraph, neg_xW1, self.b1)
        neg_relu = nn.ReLU(theGraph, neg_xW1pB)
        neg_reluW2 = nn.MatrixMultiply(theGraph, neg_relu, self.W2)
        neg_W2b2 = nn.MatrixVectorAdd(theGraph, neg_reluW2, self.b2)
        neg_neg = nn.MatrixMultiply(theGraph, neg_W2b2, negMat)

        final = nn.MatrixVectorAdd(theGraph, W2b2, neg_neg)

        if y is not None:
            # At training time, the correct output `y` is known.
            # Here, you should construct a loss node, and return the nn.Graph
            # that the node belongs to. The loss node must be the last node
            # added to the graph.
            "*** YOUR CODE HERE ***"
            yNode = nn.Input(theGraph, y)
            nn.SquareLoss(theGraph, yNode, final)
            return theGraph
        else:
            # At test time, the correct output is unknown.
            # You should instead return your model's prediction as a numpy array
            "*** YOUR CODE HERE ***"
            return theGraph.get_output(final)


class DigitClassificationModel(Model):
    """
    TODO: Question 6 - [Application] Digit Classification

    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """

    def __init__(self):
        Model.__init__(self)
        self.get_data_and_monitor = backend.get_data_and_monitor_digit_classification

        # Remember to set self.learning_rate!
        # You may use any learning rate that works well for your architecture
        "*** YOUR CODE HERE ***"
        self.learning_rate = .7
        self.hiddenLayerSize = 260

        self.W1 = nn.Variable(784, self.hiddenLayerSize)
        self.b1 = nn.Variable(self.hiddenLayerSize)
        self.W2 = nn.Variable(self.hiddenLayerSize, 10)
        self.b2 = nn.Variable(10)

    def run(self, x, y=None):
        """
        TODO: Question 6 - [Application] Digit Classification

        Runs the model for a batch of examples.

        The correct labels are known during training, but not at test time.
        When correct labels are available, `y` is a (batch_size x 10) numpy
        array. Each row in the array is a one-hot vector encoding the correct
        class.

        Your model should predict a (batch_size x 10) numpy array of scores,
        where higher scores correspond to greater probability of the image
        belonging to a particular class. You should use `nn.SoftmaxLoss` as your
        training loss.

        Inputs:
            x: a (batch_size x 784) numpy array
            y: a (batch_size x 10) numpy array, or None
        Output:
            (if y is not None) A nn.Graph instance, where the last added node is
                the loss
            (if y is None) A (batch_size x 10) numpy array of scores (aka logits)
        """
        "*** YOUR CODE HERE ***"
        theGraph = nn.Graph([self.W1, self.b1, self.W2, self.b2])
        xNode = nn.Input(theGraph, x)

        # f(x) = relu(x * W1 + b1) * W2 + b2
        xW1 = nn.MatrixMultiply(theGraph, xNode, self.W1)
        xW1pB = nn.MatrixVectorAdd(theGraph, xW1, self.b1)
        relu = nn.ReLU(theGraph, xW1pB)
        reluW2 = nn.MatrixMultiply(theGraph, relu, self.W2)
        fx = nn.MatrixVectorAdd(theGraph, reluW2, self.b2)

        if y is not None:
            "*** YOUR CODE HERE ***"
            yNode = nn.Input(theGraph, y)
            nn.SoftmaxLoss(theGraph, fx, yNode)
            return theGraph

        else:
            "*** YOUR CODE HERE ***"
            return theGraph.get_output(fx)


class DeepQModel(Model):
    """
    TODO: Question 7 - [Application] Reinforcement Learning

    A model that uses a Deep Q-value Network (DQN) to approximate Q(s,a) as part
    of reinforcement learning.

    (We recommend that you implement the RegressionModel before working on this
    part of the project.)
    """

    def __init__(self):
        Model.__init__(self)
        self.get_data_and_monitor = backend.get_data_and_monitor_rl

        self.num_actions = 2
        self.state_size = 4

        # Remember to set self.learning_rate!
        # You may use any learning rate that works well for your architecture
        "*** YOUR CODE HERE ***"
        self.learning_rate = .015
        self.hiddenLayerSize = 60

        self.W1 = nn.Variable(self.state_size, self.hiddenLayerSize)
        self.b1 = nn.Variable(self.hiddenLayerSize)
        self.W2 = nn.Variable(self.hiddenLayerSize, self.num_actions)
        self.b2 = nn.Variable(self.num_actions)

    def run(self, states, Q_target=None):
        """
        TODO: Question 7 - [Application] Reinforcement Learning

        Runs the DQN for a batch of states.

        The DQN takes the state and computes Q-values for all possible actions
        that can be taken. That is, if there are two actions, the network takes
        as input the state s and computes the vector [Q(s, a_1), Q(s, a_2)]

        When Q_target == None, return the matrix of Q-values currently computed
        by the network for the input states.

        When Q_target is passed, it will contain the Q-values which the network
        should be producing for the current states. You must return a nn.Graph
        which computes the training loss between your current Q-value
        predictions and these target values, using nn.SquareLoss.

        Inputs:
            states: a (batch_size x 4) numpy array
            Q_target: a (batch_size x 2) numpy array, or None
        Output:
            (if Q_target is not None) A nn.Graph instance, where the last added
                node is the loss
            (if Q_target is None) A (batch_size x 2) numpy array of Q-value
                scores, for the two actions
        """
        "*** YOUR CODE HERE ***"
        theGraph = nn.Graph([self.W1, self.b1, self.W2, self.b2])
        sNode = nn.Input(theGraph, states)

        # f(x) = relu(x * W1 + b1) * W2 + b2
        xW1 = nn.MatrixMultiply(theGraph, sNode, self.W1)
        xW1pB = nn.MatrixVectorAdd(theGraph, xW1, self.b1)
        relu = nn.ReLU(theGraph, xW1pB)
        reluW2 = nn.MatrixMultiply(theGraph, relu, self.W2)
        fx = nn.MatrixVectorAdd(theGraph, reluW2, self.b2)

        if Q_target is not None:
            "*** YOUR CODE HERE ***"
            qNode = nn.Input(theGraph, Q_target)
            nn.SquareLoss(theGraph, qNode, fx)
            return theGraph
        else:
            "*** YOUR CODE HERE ***"
            return theGraph.get_output(fx)

    def get_action(self, state, eps):
        """
        Select an action for a single state using epsilon-greedy.

        Inputs:
            state: a (1 x 4) numpy array
            eps: a float, epsilon to use in epsilon greedy
        Output:
            the index of the action to take (either 0 or 1, for 2 actions)
        """
        if np.random.rand() < eps:
            return np.random.choice(self.num_actions)
        else:
            scores = self.run(state)
            return int(np.argmax(scores))


class LanguageIDModel(Model):
    """
    TODO: Question 8 - [Application] Language Identification

    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """

    def __init__(self):
        Model.__init__(self)
        self.get_data_and_monitor = backend.get_data_and_monitor_lang_id

        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Remember to set self.learning_rate!
        # You may use any learning rate that works well for your architecture
        "*** YOUR CODE HERE ***"
        self.learning_rate = .0025
        self.hiddenLayerSize = 200

        self.W0 = nn.Variable(len(self.languages), self.num_chars)
        self.W1 = nn.Variable(self.num_chars, self.hiddenLayerSize)
        self.b1 = nn.Variable(self.hiddenLayerSize)
        self.W2 = nn.Variable(self.hiddenLayerSize, len(self.languages))
        self.b2 = nn.Variable(1)

    def run(self, xs, y=None):
        """
        TODO: Question 8 - [Application] Language Identification

        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        (batch_size x self.num_chars) numpy array, where every row in the array
        is a one-hot vector encoding of a character. For example, if we have a
        batch of 8 three-letter words where the last word is "cat", we will have
        xs[1][7,0] == 1. Here the index 0 reflects the fact that the letter "a"
        is the inital (0th) letter of our combined alphabet for this task.

        The correct labels are known during training, but not at test time.
        When correct labels are available, `y` is a (batch_size x 5) numpy
        array. Each row in the array is a one-hot vector encoding the correct
        class.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node that represents a (batch_size x hidden_size)
        array, for your choice of hidden_size. It should then calculate a
        (batch_size x 5) numpy array of scores, where higher scores correspond
        to greater probability of the word originating from a particular
        language. You should use `nn.SoftmaxLoss` as your training loss.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a (batch_size x self.num_chars) numpy array
            y: a (batch_size x 5) numpy array, or None
        Output:
            (if y is not None) A nn.Graph instance, where the last added node is
                the loss
            (if y is None) A (batch_size x 5) numpy array of scores (aka logits)

        Hint: you may use the batch_size variable in your code
        """
        batch_size = xs[0].shape[0]

        "*** YOUR CODE HERE ***"
        hNode = nn.Variable(batch_size, 5)
        theGraph = nn.Graph([self.W0, self.W1, self.b1, self.W2, self.b2, hNode])
        for x in xs:
            # f(x) = relu((x+ (h * W0)) * W1 + b1) * W2 + b2
            hW0 = nn.MatrixMultiply(theGraph, hNode, self.W0)
            xNode = nn.Input(theGraph, x)
            hx = nn.Add(theGraph, hW0, xNode)
            xW1 = nn.MatrixMultiply(theGraph, hx, self.W1)
            xW1pB = nn.MatrixVectorAdd(theGraph, xW1, self.b1)
            relu = nn.ReLU(theGraph, xW1pB)
            reluW2 = nn.MatrixMultiply(theGraph, relu, self.W2)
            hNode = nn.MatrixVectorAdd(theGraph, reluW2, self.b2)

        if y is not None:
            "*** YOUR CODE HERE ***"
            yNode = nn.Input(theGraph, y)
            nn.SoftmaxLoss(theGraph, hNode, yNode)
            return theGraph
        else:
            "*** YOUR CODE HERE ***"
            return theGraph.get_output(hNode)

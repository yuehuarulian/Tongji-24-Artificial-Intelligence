import nn
from backend import Dataset
class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(x, self.get_weights()) # features 1*c weight 1*c

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        score = nn.as_scalar(self.run(x))
        return 1 if score>=0 else -1

    def train(self, dataset:Dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        batch_size = 1
        while True:
            finish = True
            for X, y in dataset.iterate_once(batch_size):
                y_pre = self.get_prediction(X)
                if y_pre != nn.as_scalar(y):
                    finish = False
                    self.w.update(X, nn.as_scalar(y))
            if finish:
                break

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        self.learning_rate = 0.01
        self.batch_size = 10
        self.h1 = 256
        self.h2 = 512
        "*** YOUR CODE HERE ***"
        self.W1 = nn.Parameter(1, self.h1) # 1*50
        self.b1 = nn.Parameter(1, self.h1) # 1*50
        self.W2 = nn.Parameter(self.h1, self.h2) # 50*20
        self.b2 = nn.Parameter(1, self.h2) # 1*20
        self.W3 = nn.Parameter(self.h2, 1) # 20*1
        self.b3 = nn.Parameter(1, 1)     # 1*1
        # function: f(x) = ReLU(x * W1 + b1) * W2 + b2     x:batch_size*1

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        layer1 = nn.AddBias(nn.Linear(x, self.W1), self.b1) # b*1 1*50 1*50 -> b*50
        relu1 = nn.ReLU(layer1)

        layer2 = nn.AddBias(nn.Linear(relu1, self.W2), self.b2) # b*50 50*20 1*20 -> b*20
        relu2 = nn.ReLU(layer2)

        prediction = nn.AddBias(nn.Linear(relu2, self.W3), self.b3) # b*20 20*1 1*1 -> b*1
        return prediction

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            for X, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(X,y)
                g_W1, g_b1, g_W2, g_b2, g_W3, g_b3 = nn.gradients(loss, [self.W1, self.b1, self.W2, self.b2, self.W3, self.b3])
                self.W1.update(g_W1, -self.learning_rate)
                self.b1.update(g_b1, -self.learning_rate)
                self.W2.update(g_W2, -self.learning_rate)
                self.b2.update(g_b2, -self.learning_rate)
                self.W3.update(g_W3, -self.learning_rate)
                self.b3.update(g_b3, -self.learning_rate)
            if loss.data < 0.0001:
                print(loss.data)
                break

class DigitClassificationModel(object):
    """
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
        # Initialize your model parameters here
        self.learning_rate = 0.02
        self.batch_size = 100
        self.h1 = 128
        self.h2 = 64
        self.figure = 10
        "*** YOUR CODE HERE ***"
        self.W1 = nn.Parameter(28*28, self.h1) # 784*128
        self.b1 = nn.Parameter(1, self.h1) # 1*128
        self.W2 = nn.Parameter(self.h1, self.h2) # 128*32
        self.b2 = nn.Parameter(1, self.h2) # 1*32
        self.W3 = nn.Parameter(self.h2, self.figure) # 32*10
        self.b3 = nn.Parameter(1, self.figure)     # 1*10
        # function: f(x) = ReLU(x * W1 + b1) * W2 + b2     x:batch_size*1

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        layer1 = nn.AddBias(nn.Linear(x, self.W1), self.b1) # b*1 1*50 1*50 -> b*50
        relu1 = nn.ReLU(layer1)

        layer2 = nn.AddBias(nn.Linear(relu1, self.W2), self.b2) # b*50 50*20 1*20 -> b*20
        relu2 = nn.ReLU(layer2)

        prediction = nn.AddBias(nn.Linear(relu2, self.W3), self.b3) # b*20 20*1 1*1 -> b*1
        return prediction

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SoftmaxLoss(self.run(x), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            for X, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(X,y)
                g_W1, g_b1, g_W2, g_b2, g_W3, g_b3 = nn.gradients(loss, [self.W1, self.b1, self.W2, self.b2, self.W3, self.b3])
                self.W1.update(g_W1, -self.learning_rate)
                self.b1.update(g_b1, -self.learning_rate)
                self.W2.update(g_W2, -self.learning_rate)
                self.b2.update(g_b2, -self.learning_rate)
                self.W3.update(g_W3, -self.learning_rate)
                self.b3.update(g_b3, -self.learning_rate)
                if dataset.get_validation_accuracy() >= 0.98:
                    return

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        """
        i = input size = 784 (because every input has 784 pixels)
        h = hidden layer size (variable, should test different values between 10 and 400)
        o = output size = 10 (because we classify for numbers 0 through 9)
        b = batch size (Hyperparameter, should evenly divide dataset (here 200))
        """
        self.figure = 5
        self.h = 200
        self.batch_size = 200
        self.learning_rate = 0.1
        """
        function: h_1(x) = ReLU([x * W])                      (batch_size,47)*(47*h) -> (batch_size,h)
        function: h_i(x) = ReLu([x * W] + [h_i * W_hidden])   (batch_size,47)*(47*h)+(batch_size,h)*(h,h) -> (batch_size,h)
        x  has dimensions   b x i
        W  has dimensions   i x h
        ==> h_1 = [x * W] has dimensions: b x h
        """
        self.W = nn.Parameter(self.num_chars, self.h)
        self.W_hidden = nn.Parameter(self.h, self.h)
        self.W_output = nn.Parameter(self.h, self.figure)

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        L = len(xs)
        for i in range(L):
            if i == 0:
                h = nn.ReLU(nn.Linear(xs[i], self.W))
            else:
                h = nn.ReLU(nn.Add(nn.Linear(xs[i], self.W), nn.Linear(h, self.W_hidden)))
        return nn.Linear(h, self.W_output)

    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(xs), y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        while True:
            for x, y in dataset.iterate_once(self.batch_size):
                loss = self.get_loss(x, y)
                g_W, g_W_hidden, g_W_output = nn.gradients(loss, [self.W, self.W_hidden, self.W_output])
                self.W.update(g_W, -self.learning_rate)
                self.W_hidden.update(g_W_hidden, -self.learning_rate)
                self.W_output.update(g_W_output, -self.learning_rate)
            if dataset.get_validation_accuracy() > 0.84:
                break

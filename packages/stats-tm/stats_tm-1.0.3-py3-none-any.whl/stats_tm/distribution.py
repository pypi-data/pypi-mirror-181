# %%
import math
import mpmath
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# %%
# Create a custom theme and set it as default
pio.templates["custom"] = pio.templates["plotly_white"]
pio.templates["custom"].layout.margin = {"b": 25, "l": 25, "r": 25, "t": 50}
pio.templates["custom"].layout.width = 800
pio.templates["custom"].layout.height = 600
pio.templates["custom"].layout.autosize = False
pio.templates["custom"].layout.font.update(
    {"family": "Arial", "size": 12, "color": "#707070"}
)
pio.templates["custom"].layout.title.update(
    {
        "xref": "container",
        "yref": "container",
        "font_size": 16,
        "y": 0.95,
        "font_color": "#353535",
        "x": 0.5,
    }
)
pio.templates["custom"].layout.xaxis.update(
    {"showline": True, "linecolor": "lightgray", "title_font_size": 14}
)
pio.templates["custom"].layout.yaxis.update(
    {"showline": True, "linecolor": "lightgray", "title_font_size": 14}
)
pio.templates["custom"].layout.colorway = [
    "#1F77B4",
    "#FF7F0E",
    "#54A24B",
    "#D62728",
    "#C355FA",
    "#8C564B",
    "#E377C2",
    "#7F7F7F",
    "#FFE323",
    "#17BECF",
]
pio.templates.default = "custom"

# %%
class _DiscreteDist:
    def __init__(self, calc_x_limit: "function", calc_pmf: "function"):
        """Base class of discrete distributions for plotting the probability distribution

        Args:
            calc_x_limit (function): function to calculate the x-axis upper limit
            calc_pmf (function): function to calculate the probability mass function
        """
        # Set the x and y values for the probability distribution
        x_limit = calc_x_limit()
        x_vals = [x for x in range(x_limit + 1)]
        y_vals = [calc_pmf(x, plot=False) for x in x_vals]
        self._x_vals = np.array(x_vals)
        self._y_vals = np.array(y_vals)

    def plot_dist(
        self, x_vals: "array-like", y_vals: "array-like", labels: dict, title: str
    ):
        """Plot the probability distribution for a discrete distribution

        Args:
            x_vals (array-like): values of the x-axis
            y_vals (array-like): values of the y-axis
            labels (dict): dictionary of labels for the x and y axes
            title (str): title of the plot

        Returns:
            plotly.graph_objects.Figure: plot of the distribution
        """
        fig = px.bar(x=x_vals, y=y_vals, labels=labels, title=title,)
        fig.update_traces(hovertemplate="P(K = %{x}) = %{y:.5f}<extra></extra>")
        return fig
    
    def _plot_pmf(self, x_vals: "array-like", pmf: float, k: int):
        """Plot the probability distribution for a discrete distribution along with its probability mass function at k highlighted

        Args:
            x_vals (array-like): values of the x-axis
            pmf (float): probability mass function at k
            k (int): number of successes

        Returns:
            plotly.graph_objects.Figure: plot of the distribution with the probability mass function at k highlighted
        """
        fig = self.plot_dist()
        fig.layout.title.text += ", <span style='color:#FF7F0E'><b>P(K = {}) = {:.5f}</b></span>".format(
            k, pmf
        )
        # Highlight the probability mass function at k
        k_index = np.where(x_vals == k)[0]
        colors = np.array(["#1F77B4"] * x_vals.shape[0])
        colors[k_index] = ["#FF7F0E"]
        fig.data[0].marker.color = colors
        return fig

    def _plot_cum_p(self, x_vals: "array-like", cum_p: float, k: int):
        """Plot the probability distribution for a discrete distribution along with its cumulative probability at k highlighted

        Args:
            x_vals (array-like): values of the x-axis
            cum_p (float): cumulative probability, P(K <= k)
            k (int): number of successes

        Returns:
            plotly.graph_objects.Figure: plot of the distribution with cumulative probability at k highlighted
        """
        fig = self.plot_dist()
        fig.layout.title.text += ", <span style='color:#FF7F0E'><b>P(K <= {}) = {:.5f}</b></span>".format(
            k, cum_p
        )
        # Highlight the cumulative probability at k
        k_index = np.where(x_vals <= k)[0]
        colors = np.array(["#1F77B4"] * x_vals.shape[0])
        colors[k_index] = ["#FF7F0E"]
        fig.data[0].marker.color = colors
        return fig


    def __repr__(self):
        """Returns the representation of the class

        Returns:
            str: representation of the class
        """
        return "Base class for discrete distribution"


# %%
class BinomialDist(_DiscreteDist):
    def __init__(self, n: int, p: float):
        """Binomial distribution class for plotting probability distribution and calculating probability mass function/ cumulative probability

        Args:
            n (int): number of trials
            p (float): probability of success

        Raises:
            AssertionError: probability of success (p) must be between 0 and 1
            AssertionError: number of trials (n) must be greater than 0
        """
        if p < 0 or p > 1:
            raise AssertionError("probability of success (p) must be between 0 and 1")
        elif n <= 0:
            raise AssertionError("number of trials (n) must be greater than 0")
        self._n = n
        self._p = p
        # Set the x and y values for the probability distribution
        super().__init__(self._calc_x_limit, self.calc_pmf)

    @property
    def n(self):
        """Get the number of trials for the binomial distribution

        Returns:
            int: number of trials for the binomial distribution
        """
        return self._n

    @n.setter
    def n(self, new_n: int):
        """Set a new number of trials for the binomial distribution

        Args:
            new_n (int): new number of trials for the binomial distribution

        Raises:
            AssertionError: the new number of trials (new_n) must be greater than 0
        """
        if new_n <= 0:
            raise AssertionError(
                "the new number of trials (new_n) must be greater than 0"
            )
        self._n = new_n
        # Set the x and y values for the probability distribution
        super().__init__(self._calc_x_limit, self.calc_pmf)

    @property
    def p(self):
        """Get the probability of success for the binomial distribution

        Returns:
            float: probability of success for the binomial distribution
        """
        return self._p

    @p.setter
    def p(self, new_p: float):
        """Set a new probability of success for the binomial distribution

        Args:
            new_p (float): new probability of success for the binomial distribution

        Raises:
            AssertionError: the new probability of success (new_p) must be between 0 and 1
        """
        if new_p < 0 or new_p > 1:
            raise AssertionError(
                "the new probability of success (new_p) must be between 0 and 1"
            )
        self._p = new_p
        # Set the x and y values for the probability distribution
        super().__init__(self._calc_x_limit, self.calc_pmf)
        
    def plot_dist(self):
        """Plot the probability distribution for a binomial distribution

        Returns:
            plotly.graph_objects.Figure: plot of the distribution
        """
        labels = {"x": "Number of Successes", "y": "Probability"}
        title = "Probability Mass Function for Binomial Distribution<br>n = {}, p = {}".format(
            self._n, self._p
        )
        fig = super().plot_dist(self._x_vals, self._y_vals, labels, title)
        return fig
    
    def calc_pmf(self, k: int, plot=True):
        """Calculate the probability mass function for a binomial distribution and optionally plot the distribution

        Args:
            k (int): number of successes
            plot (bool, optional): if True, return a plot of the distribution with probability mass funtion at k highlighted. Defaults to True.

        Raises:
            AssertionError: the number of successes (k) should be between 0 and n

        Returns:
            plotly.graph_objects.Figure or float: plot of the distribution with probability mass function at k highlighted or probability mass function at k 
        """
        n = self._n
        p = self._p
        if k < 0 or k > n:
            raise AssertionError(
                "the number of successes (k) should be between 0 and {} (n)".format(n)
            )
        pmf = math.comb(n, k) * pow(p, k) * pow((1 - p), (n - k))
        if plot == False:
            return pmf
        elif plot == True:
            fig = super()._plot_pmf(self._x_vals, pmf, k)
            return fig

    def _calc_x_limit(self):
        """Calculate the upper x-axis limit for the distribution

        Returns:
            int: x-axis limit
        """
        return self._n

    def calc_cum_p(self, k: int, plot=True):
        """Calculate the cumulative probability for a binomial distribution and optionally plot the distribution

        Args:
            k (int): number of successes
            plot (bool, optional): if True, return a plot of the distribution with cumulative probability at k highlighted. Defaults to True.

        Raises:
            AssertionError: the number of successes (k) should be between 0 and n

        Returns:
            plotly.graph_objects.Figure or float: plot of the distribution with cumulative probability at k highlighted or cumulative probability at k
        """
        x_vals = self._x_vals
        y_vals = self._y_vals
        n = self._n
        if k < 0 or k > n:
            raise AssertionError(
                "the number of successes (k) should be between 0 and {} (n)".format(n)
            )
        cum_p = np.cumsum(y_vals)[len(x_vals[x_vals <= k]) - 1]
        if plot == False:
            return cum_p
        elif plot == True:
            fig = super()._plot_cum_p(x_vals, cum_p, k)
            return fig

    def __repr__(self):
        """Returns the representation of the class

        Returns:
            str: representation of the class
        """
        return "Binomial distribution with number of trials (n) = {} and probability of success (p) = {}".format(
            self._n, self._p
        )


# %%


class PoissonDist(_DiscreteDist):
    def __init__(self, lambda_: int):
        """Poisson distribution class for plotting probability distribution and calculating probability mass function/ cumulative probability

        Args:
            lambda_ (int): rate of occurences

        Raises:
            AssertionError: the rate of occurences (lambda_) must be greater than 0
        """
        if lambda_ <= 0:
            raise AssertionError(
                "the rate of occurences (lambda_) must be greater than 0"
            )
        self._lambda = lambda_
        # Set the x and y values for the probability distribution
        super().__init__(self._calc_x_limit, self.calc_pmf)

    @property
    def lambda_(self):
        """Get the rate of occurences for the poisson distribution

        Returns:
            int: rate of occurences for the poisson distribution
        """
        return self._lambda

    @lambda_.setter
    def lambda_(self, new_lambda: int):
        """Set a new rate of occurences for the poisson distribution

        Args:
            new_lambda (int): new rate of occurences for the poisson distribution

        Raises:
            AssertionError: the new rate of occurences (new_lambda) must be greater than 0
        """
        if new_lambda <= 0:
            raise AssertionError(
                "the new rate of occurences (new_lambda) must be greater than 0"
            )
        self._lambda = new_lambda
        # Set the x and y values for the probability distribution
        super().__init__(self._calc_x_limit, self.calc_pmf)
    
    def plot_dist(self):
        """Plot the probability distribution for a poisson distribution

        Returns:
            plotly.graph_objects.Figure: plot of the distribution
        """
        labels = {"x": "Number of Occurences", "y": "Probability"}
        title = "Probability Mass Function for Poisson Distribution<br>λ = {}".format(
            self._lambda
        )
        fig = super().plot_dist(self._x_vals, self._y_vals, labels, title)
        fig.update_layout(margin_b=80)
        fig.add_annotation(
            xref="paper",
            yref="paper",
            x=0,
            y=-0.23,
            font_size=12,
            font_color="lightgray",
            showarrow=False,
            text="The upper limit for the x axis is bound by K with a PMF > 0.001",
        )
        return fig

    def calc_pmf(self, k: int, plot=True):
        """Calculate the probability mass function for a poisson distribution and optionally plot the distribution

        Args:
            k (int): number of occurences
            plot (bool, optional): if True, return a plot of the distribution with probability mass funtion at k highlighted. Defaults to True.

        Raises:
            AssertionError: the number of occurences (k) should be greater than or equal to 0

        Returns:
            plotly.graph_objects.Figure or float: plot of the distribution with probability mass function at k highlighted or probability mass function at k
        """
        lambda_ = self._lambda
        if k < 0:
            raise AssertionError(
                "the number of occurences (k) should be greater than or equal to 0"
            )
        pmf = pow(lambda_, k) * pow(math.e, -1 * lambda_) / math.factorial(k)
        if plot == False:
            return pmf
        elif plot == True:
            fig = super()._plot_pmf(self._x_vals, pmf, k)
            return fig

    def _calc_x_limit(self):
        """Calculate the upper x-axis limit for the distribution

        Returns:
            int: x-axis limit
        """
        k = self._lambda
        # Only include k with a probability mass function greater than 0.001 in the x-axis
        while self.calc_pmf(k, plot=False) > 0.001:
            k += 1
        return k - 1

    def calc_cum_p(self, k: int, plot=True):
        """Calculate the cumulative probability for a poisson distribution and optionally plot the distribution

        Args:
            k (int): number of occurences
            plot (bool, optional): if True, return a plot of the distribution with cumulative probability at k highlighted. Defaults to True.

        Raises:
            AssertionError: the number of occurences (k) should be greater than or equal to 0

        Returns:
            plotly.graph_objects.Figure or float: plot of the distribution with cumulative probability at k highlighted or cumulative probability at k
        """
        if k < 0:
            raise AssertionError(
                "the number of occurences (k) should be greater than or equal to 0"
            )
            
        # if k is greater than the self._x_vals, new x_vals and y_vals need to be calculated to get the cumulative probability
        if k <= self._x_vals.max():
            x_vals = self._x_vals
            y_vals = self._y_vals
        elif k > self._x_vals.max():
            x_vals = [x for x in range(k + 1)]
            y_vals = [self.calc_pmf(x, plot=False) for x in x_vals]
            x_vals = np.array(x_vals)
            y_vals = np.array(y_vals)
        cum_p = np.cumsum(y_vals)[len(x_vals[x_vals <= k]) - 1]
        
        if plot == False:
            return cum_p
        elif plot == True:
            fig = super()._plot_cum_p(x_vals, cum_p, k)
            return fig

    def __repr__(self):
        """Returns the representation of the class

        Returns:
            str: representation of the class
        """
        return "Poisson distribution with rate of occurence (λ) = {}".format(
            self._lambda
        )


# %%
class _ContinuousDist:
    def __init__(self, calc_x_limit: "function", calc_pdf: "function"):
        """Base class of continuous distribution for plotting the probability distribution
        
        Args:
            calc_x_limit (function): function to calculate the x-axis lower and upper limit
            calc_pdf (function): function to calculate the probability density function
        """
        # Set the x and y values for the probability distribution
        x_lim1, x_lim2 = self._calc_x_limit()
        self._x_vals = np.arange(x_lim1, x_lim2, 0.001)
        self._y_vals = np.array([self.calc_pdf(x, plot=False) for x in self._x_vals])

    def plot_dist(self, x_vals: "array-like", y_vals: "array-like", title: str):
        """Plot the probability distribution for a continuous distribution

        Args:
            x_vals (array-like): values of x-axis
            y_vals (array-like): values of y-axis
            title (str): title of the plot

        Returns:
            plotly.graph_objects.Figure: plot of the distribution
        """
        fig = px.line(
            x=x_vals, y=y_vals, labels={"y": "Probability Density"}, title=title
        )
        fig.update_yaxes(rangemode="tozero")
        fig.update_traces(hovertemplate="F(x = %{x}) = %{y:.5f}<extra></extra>")
        return fig
    
    def _plot_pdf(self, x: float, pdf: float):
        """Plot the probability distribution for a continuous distribution along with its probability density function at x highlighted

        Args:
            x (float): value of x
            pdf (float): probability density function at x

        Returns:
            plotly.graph_objects.Figure: plot of the distribution with the probability density function at x highlighted
        """
        fig = self.plot_dist()
        fig.layout.title.text += ", <span style='color:#FF7F0E'><b>F(x = {}) = {:.5f}</b></span>".format(
            x, pdf
        )
        # Mark the probability density function at x
        fig.add_scatter(
            x=[x],
            y=[pdf],
            mode="markers",
            marker_size=10,
            marker_color="rgba(255, 127, 14, 1)",
            showlegend=False,
        )
        fig.update_traces(hovertemplate="F(x = %{x}) = %{y:.5f}<extra></extra>")
        return fig

    def _plot_cum_p(
        self,
        x_vals: "array-like",
        y_vals: "array-like",
        cum_p: "float",
        x: float,
        pdf: float,
    ):
        """Calculate the cumulative probability for a continuous distribution and optionally plot the distribution

        Args:
            x_vals (array-like): values of x-axis
            y_vals (array-like): values of y-axis
            x (float): x value
            pdf (float): probability density function at x
            plot (bool): if True, return a plot of the distribution with cumulative probability at x highlighted

        Returns:
            plotly.graph_objects.Figure or float: plot of the distribution with cumulative probability at x highlighted or cumulative probability at x
        """
        fig = self.plot_dist()
        fig.layout.title.text += ", <span style='color:#FF7F0E'><b>P(X < {}) = {:.5f}</b></span>".format(
            x, cum_p
        )
        # Highlight the cumulative probability at x (area under the curve to the left of x)
        fig.add_scatter(
            x=x_vals[x_vals < x],
            y=y_vals,
            fill="tozeroy",
            mode="none",
            fillcolor="rgba(255, 127, 14, 0.4)",
            showlegend=False,
        )
        # Add a vertical line at x
        fig.add_shape(type="line", x0=x, y0=0, x1=x, y1=pdf, line_width=0.4)
        fig.update_traces(hovertemplate="F(x = %{x}) = %{y:.5f}<extra></extra>")
        return fig

    def __repr__(self):
        """Returns the string representation of the class

        Returns:
            str: representation of the class
        """
        return "Base class for continuous distribution"


# %%
class NormalDist(_ContinuousDist):
    def __init__(self, mu: float, sigma: float):
        """Normal distribution class for plotting probability distribution and calculating probability density function/ cumulative probability

        Args:
            mu (float): mean of the distribution
            sigma (float): standard deviation of the distribution
        
        Raises:
            AssertionError: the standard deviation must be greater than 0
        """
        if sigma < 0:
            raise AssertionError("the standard deviation must be greater than 0")
        self._mu = mu
        self._sigma = sigma
        # Set the x and y values for the probability distribution
        super().__init__(self._calc_x_limit, self.calc_pdf)

    @property
    def mu(self):
        """Get the mean of the normal distribution

        Returns:
            float: mean of the normal distribution
        """
        return self._mu

    @mu.setter
    def mu(self, new_mu: float):
        """Set a new mean for the normal distribution

        Args:
            new_mu (float): new mean of the normal distribution
        """
        self._mu = new_mu
        # Set the x and y values for the probability distribution
        super().__init__(self._calc_x_limit, self.calc_pdf)

    @property
    def sigma(self):
        """Get the standard deviation of the normal distribution

        Returns:
            float: standard deviation of the normal distribution
        """
        return self._sigma

    @sigma.setter
    def sigma(self, new_sigma):
        """Set a new standard deviation for the normal distribution

        Args:
            new_sigma (float): new standard deviation of the normal distribution
        
        Raises:
            AssertionError: the new standard deviation must be greater than 0
        """
        if new_sigma < 0:
            raise AssertionError("the new standard deviation must be greater than 0")
        self._sigma = new_sigma
        # Set the x and y values for the probability distribution
        super().__init__(self._calc_x_limit, self.calc_pdf)
    
    def plot_dist(self):
        """Plot the probability distribution for a normal distribution

        Returns:
            plotly.graph_objects.Figure: plot of the distribution
        """
        title = "Probability Density Function for Normal Distribution<br>µ = {}, σ = {}".format(
            self._mu, self._sigma
        )
        fig = super().plot_dist(self._x_vals, self._y_vals, title)
        return fig

    def calc_pdf(self, x: float, plot=True):
        """Calculate the probability density function for a normal distribution and optionally plot the distribution

        Args:
            x (float): value of x
            plot (bool, optional): if True, return a plot of the distribution with probability density function at x highlighted. Defaults to True.

        Returns:
            plotly.graph_objects.Figure or float: plot of the distribution with probability density function at x highlighted or probability density function at x
        """
        sigma = self._sigma
        mu = self._mu
        pdf = (1 / (math.sqrt(2 * math.pi) * sigma)) * math.pow(
            math.e, (-1 / 2 * math.pow((x - mu) / sigma, 2))
        )
        if plot == False:
            return pdf
        elif plot == True:
            fig = super()._plot_pdf(x, pdf)
            return fig

    def _calc_x_limit(self):
        """Calculate the x limit for the distribution

        Returns:
            float: x-axis limit
        """
        # Set the x-axis limit to 4.5 standard deviations away from the mean (as they will cover most of the distribution)
        x_lim1 = self._mu - (4.5 * self._sigma)
        x_lim2 = self._mu + (4.5 * self._sigma)
        return (x_lim1, x_lim2)

    def calc_cum_p(self, x: float, plot=True):
        """Calculate the cumulative probability for a normal distribution and optionally plot the distribution

        Args:
            x (float): value of x
            plot (bool, optional): if True, return a plot of the distribution with cumulative probability at x highlighted. Defaults to True.

        Returns:
            plotly.graph_objects.Figure or float: plot of the distribution with cumulative probability at x highlighted or cumulative probability at x
        """
        pdf = self.calc_pdf(x, plot=False)
        cum_p = (1 + math.erf((x - self._mu) / (self._sigma * math.sqrt(2)))) / 2
        if plot == False:
            return cum_p
        elif plot == True:
            fig = super()._plot_cum_p(self._x_vals, self._y_vals, cum_p, x, pdf)
            return fig

    def __repr__(self):
        """Returns the string representation of the class

        Returns:
            str: representation of the class
        """
        return "Normal distribution with mean (µ) = {} and standard deviation (σ) = {}".format(
            self._mu, self._sigma
        )


# %%
class StudentsTDist(_ContinuousDist):
    def __init__(self, v: int):
        """Student's t distribution class for plotting probability distribution and calculating probability density function/ cumulative probability

        Args:
            v (int): degree of freedom of the distribution

        Raises:
            AssertionError: the degree of freedom (v) must be greater than 0
        """
        if v < 1:
            raise AssertionError("the degree of freedom (v) must be greater than 0")
        self._v = v
        # Set the x and y values for the probability distribution
        super().__init__(self._calc_x_limit, self.calc_pdf)

    @property
    def v(self):
        """Get the degree of freedom of the Student's t distribution

        Returns:
            int: degree of freedom of the Student's t distribution
        """
        return self._v

    @v.setter
    def v(self, new_v):
        """Set a new degree of freedom for the Student's t distribution

        Args:
            new_v (int): new degree of freedom of the Student's t distribution

        Raises:
            AssertionError: the new degree of freedom (new_v) must be greater than 0
        """
        if new_v < 1:
            raise AssertionError(
                "the new degree of freedom (new_v) must be greater than 0"
            )
        self._v = new_v
        # Set the x and y values for the probability distribution
        super().__init__(self._calc_x_limit, self.calc_pdf)
        
    def plot_dist(self):
        """Plot the probability distribution for a Student's t distribution

        Returns:
            plotly.graph_objects.Figure: plot of the distribution
        """
        title = "Probability Density Function for Student's T Distribution<br>v = {}".format(
            self._v
        )
        fig = super().plot_dist(self._x_vals, self._y_vals, title)
        return fig

    def calc_pdf(self, x: float, plot=True):
        """Calculate the probability density function for a Student's t distribution and optionally plot the distribution

        Args:
            x (float): value of x
            plot (bool, optional): if True, return a plot of the distribution with probability density function at x highlighted. Defaults to True.

        Returns:
            plotly.graph_objects.Figure or float: plot of the distribution with probability density function at x highlighted or probability density function at x
        """
        v = self._v
        pdf = (
            math.gamma((v + 1) / 2)
            / (math.gamma(v / 2) * math.sqrt(v * math.pi))
            * math.pow((1 + (x * x / v)), -(v + 1) / 2)
        )
        if plot == False:
            return pdf
        elif plot == True:
            fig = super()._plot_pdf(x, pdf)
            return fig

    def _calc_x_limit(self):
        """Calculate the x limit for the distribution

        Returns:
            float: x-axis limit
        """
        x = 0
        # Only include x with a probability density function greater than 0.001 in the x-axis, unless the x-axis limit is smaller than 4.5
        while self.calc_pdf(x, plot=False) > 0.001:
            x += 0.5
        if x < 4.5:
            return 4.5
        else:
            return (-x, x)

    def calc_cum_p(self, x: float, plot=True):
        """Calculate the cumulative probability for a Student's t distribution and optionally plot the distribution

        Args:
            x (float): value of x
            plot (bool, optional): if True, return a plot of the distribution with cumulative probability at x highlighted. Defaults to True.
        Returns:
            plotly.graph_objects.Figure or float: plot of the distribution with cumulative probability at x highlighted or cumulative probability at x
        """
        pdf = self.calc_pdf(x, plot=False)
        v = self._v
        cum_p = float(
            (1 / 2)
            + x
            * math.gamma((v + 1) / 2)
            / (math.sqrt(math.pi * v) * math.gamma(v / 2))
            * mpmath.hyp2f1((1 / 2), (v + 1) / 2, (3 / 2), -(x * x / v))
        )
        if plot == False:
            return cum_p
        elif plot == True:
            fig = super()._plot_cum_p(self._x_vals, self._y_vals, cum_p, x, pdf)
            return fig

    def __repr__(self):
        """Returns the representation of the class

        Returns:
            str: representation of the class
        """
        return "Student's T distribution with degree of freedom (v) = {}".format(
            self._v
        )


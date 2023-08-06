"""Main module."""

import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import pandas as pd

class Bass_Model:
    """
    This model is the interpretation of the Bass model that is used to predict the market shares of various newly introduced and mature products. For calculations I used the popular OLS method. 
    """
    def __init__(self, filename=None):
        """
        Initializing the class to get the Bass Model
        Parameters
        ----------
        filename : CSV file with two columns, first: time, next: values without header
        Returns
        -------
        None
        """
        if filename is None:
            print('Error: must input filename.')
        try:
            if filename[-3:] == 'csv':
                delimiter = ','
            else:
                delimiter = '\t'
            self.data = np.genfromtxt(filename, delimiter=delimiter)
        except OSError:
            print('Error: file not found. Please input valid filename.')

        try:
            self.response = self.data[:, 1]
            self.time = range(1, len(self.response) + 1)
            self.title = filename[:-4]

        except IndexError:

            print('Error: incorrect file format. Please provide either csv or txt.')


        self.sales = None
        self.sales_forecast = None
        self.cumsales = None
        self.cumsales_forecast=None
        self.mod = None
        self.cum_sales_squared = None
        self.res = None
        self.pars = None
        self.m = None
        self.p = None
        self.q = None

    def __bass_f__(self, p, q, t):

        """
        calculating f(x)
        Parameters
        ----------
        p : int
            coefficient of innovation
        p : int
            coefficient of imitation
        t: int
            time 
        Returns
        -------
        f(x)
        """

        return (np.exp((p + q) * t) * p * (p + q) ** 2) / ((p * np.exp((p + q) * t) + q) ** 2)

    
    def __repr__(self):
        """
        dunder method __repr__ for representation of the class 
        Returns
        -------
        class representation
        """
        return f'(Running Bass Model on "{self.title}" data)'
    
    def __str__(self):
        """
        dunder method __str__ for representation of the class while trying to stringify
        Returns
        -------
        class representation while trying to stringify
        """
        return f'(String version of Bass Model on "{self.title}" data)'


    def fit(self):
        """
        fiting the data to the Bass Model OLS regression
        Returns
        -------
        float
            the coeficient estimation from the OLS regression
        """
        self.sales = self.response
        self.cumsales = np.cumsum(self.sales)
        self.cum_sales_squared = self.cumsales ** 2 #cumulative sales column for later plots
        list_of_tuples = list(zip(self.sales, self.cumsales, self.cum_sales_squared))
        df = pd.DataFrame(list_of_tuples,
                          columns=['sales', 'cumsales', 'cum_sales_squared'])
        self.mod = smf.ols(formula='sales ~ cumsales + cum_sales_squared', data=df)
        self.res = self.mod.fit()
        self.pars = self.res.params
        return self.pars

    def predict(self):
        """
        Getting the maximum number of adopters, coefficient of innovation, and coefficient of imitation
        Returns
        -------
        float
            the maximum number of adopters, coefficient of innovation and coefficient of imitation
        """
        m1 = (-self.pars['cumsales'] + np.sqrt(
            self.pars['cumsales'] ** 2 - 4 * self.pars['Intercept'] * self.pars['cum_sales_squared'])) / (
                     2 * self.pars['cum_sales_squared'])
        m2 = (-self.pars['cumsales'] - np.sqrt(
            self.pars['cumsales'] ** 2 - 4 * self.pars['Intercept'] * self.pars['cum_sales_squared'])) / (
                     2 * self.pars['cum_sales_squared'])
        self.m = max(m1, m2) #max potential
        self.p = self.pars['Intercept'] / self.m #innovation
        self.q = -self.m * self.pars['cum_sales_squared'] #imitation
        self.sales_forecast = self.m * self.__bass_f__(self.p, self.q, self.time)
        return self.m, self.p, self.q

    def plot_pdf(self):
        """
        PDF visualization of the predicted sales and actual sales
        Returns
        -------
        scatterplot of actual sales and regression of predicted sales
        """
        plt.plot(self.time, self.sales, 'o', color='green', label='Actual Sales')
        plt.plot(self.time, self.sales_forecast, color='yellowgreen', label='Sales Forecast')
        plt.ylabel('Sales')
        plt.xlabel('Time')
        plt.title("Bass Model for Product Sales")
        plt.legend()
        plt.show()

    def plot_cdf(self):
        """
        CDF visualization of the predicted sales
        Returns
        -------
        Regression of cumulative predicted sales
        """
        self.cumsales_forecast = np.cumsum(self.sales_forecast)
        plt.plot(self.time, self.cumsales_forecast, label='CProb', color='green')
        plt.legend(loc='best')
        plt.xlabel('Time')
        plt.ylabel('Cumulative Sales')
        plt.title('Cumulative Probability Density Over Time')
        plt.show()

    def summary(self):
        """
        Friendly summary of our coefficient of imitation, innovation, and the maximum number of adopters
        Returns
        -------
        None
        """
        print(self.res.summary())
        print('=' * 70)

        print('\n{:<24}{:<10.5f}'.format('Coefficient of Innovation (p): ', self.p))

        print('\n{:<24}{:<10.5f}'.format('Coefficient of Imitation (q): ', self.q))

        print('\n{:<24}{:<10.2f}'.format('Max. Adopters (m): ', self.m))

        print('=' * 70)

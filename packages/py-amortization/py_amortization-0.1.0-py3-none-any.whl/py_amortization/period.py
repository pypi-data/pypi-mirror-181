from math import log

from .base import AmortizationBase


class AmortizationPeriod(AmortizationBase):
    def __init__(self, principal: float, annual_interest_rate: float) -> None:
        """Instantiate a instace with pricipal and
        annual_interest_rate or APR for calculation of EMI period for
        different EMI amounts

        :param principal: Princcipal amount
        :type principal: float

        :param annual_interest_rate: Annual Interest Rate / APR
        :type annual_interest_rate: float
        """
        super().__init__(principal, annual_interest_rate)

    def get_period(self, payment_frequency_per_year: int, amount: float) -> int:
        """Get Amortization period given period frequency in a year and EMI amount 

        :param payment_frequency_per_year: expected maximum number of payments in a year
        :type payment_frequency_per_year: int

        :param amount: monthly payment amount
        :type amount: float

        :return: number of payments
        :rtype: int
        """
        adjusted_interest = self.annual_interest_rate / payment_frequency_per_year
        return round(log(
            amount / (amount - adjusted_interest * self.principal), 1 + adjusted_interest
        ))

    def exec_function(self, **kwargs):
        return self.get_period(**kwargs)

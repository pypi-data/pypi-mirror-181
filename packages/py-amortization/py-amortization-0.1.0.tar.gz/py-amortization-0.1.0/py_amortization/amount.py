from .base import AmortizationBase


class AmortizationAmount(AmortizationBase):
    def __init__(self, principal: float, annual_interest_rate: float) -> None:
        """Instantiate a instace with pricipal and
        annual_interest_rate or APR for calculation of EMI amount for
        different periods

        :param principal: Princcipal amount
        :type principal: float

        :param annual_interest_rate: Annual Interest Rate / APR
        :type annual_interest_rate: float
        """
        super().__init__(principal, annual_interest_rate)

    def get_amount(self, payment_frequency_per_year: int, period: int) -> float:
        """Get Amortization amount given period frequency in a year and period

        :param payment_frequency_per_year: expected maximum number of payments in a year
        :type payment_frequency_per_year: int

        :param period: number of payments
        :type period: int

        :return: monthly payment amount
        :rtype: float
        """
        adjusted_interest = self.annual_interest_rate / payment_frequency_per_year
        x = (1 + adjusted_interest) ** period
        return round(self.principal * (adjusted_interest * x) / (x - 1), 2)

    def exec_function(self, **kwargs):
        return self.get_amount(**kwargs)
from typing import Any, Iterator, Tuple

from .amount import AmortizationAmount
from .base import AmortizationBase


class AmortizationSchedule(AmortizationBase):
    def __init__(self, principal: float, annual_interest_rate: float) -> None:
        """Instantiate a instace with pricipal and
        annual_interest_rate or APR for calculation of amortization schdeules for
        different periods

        :param principal: Princcipal amount
        :type principal: float

        :param annual_interest_rate: Annual Interest Rate / APR
        :type annual_interest_rate: float
        """
        super().__init__(principal, annual_interest_rate)

    def get_schedule(
        self, payment_frequency_per_year: int, period: int, as_dict=True
    ) -> 'Iterator[Tuple[int, float, float, float, float]] | Iterator[dict[str, Any]]':
        """Get Amortization schedule given period frequency in a year and period

        :param payment_frequency_per_year: expected maximum number of payments in a year
        :type payment_frequency_per_year: int

        :param period: number of payments
        :type period: int

        :param as_dict: return as dict or tuple, defaults to True
        :type as_dict: bool, optional

        :yield: amortization schedule
        :rtype: Iterator[Tuple[int, float, float, float, float]] | Iterator[dict[str, Any]]
        """
        amortization_amount = AmortizationAmount(
            self.principal, self.annual_interest_rate
        ).get_amount(payment_frequency_per_year, period)
        adjusted_interest = self.annual_interest_rate / payment_frequency_per_year
        balance = self.principal
        for number in range(1, period + 1):
            interest = round(balance * adjusted_interest, 2)
            if number < period:
                principal = round(amortization_amount - interest, 2)
                balance = round(balance - principal, 2)
            else:
                principal, amortization_amount, balance = balance, round(balance + interest, 2), 0

            if as_dict:
                yield {
                    'number': number,
                    'amount': amortization_amount,
                    'interest': interest,
                    'principal': principal,
                    'balance': balance
                }
            else:
                yield number, amortization_amount, interest, principal, balance

    def exec_function(self, **kwargs):
        if kwargs.pop('as_iter', True):
            return self.get_schedule(**kwargs)
        return list(self.get_schedule(**kwargs))
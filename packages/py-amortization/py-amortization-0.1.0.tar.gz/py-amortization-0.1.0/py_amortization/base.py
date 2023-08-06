from .payment_frequency import PaymentFrequency as PF


class AmortizationBase:
    def __init__(self, principal: float, annual_interest_rate: float) -> None:
        self.principal = principal
        self.annual_interest_rate = annual_interest_rate

    def exec_function(self, **kwargs):...

    def monthly(self, **kwargs):
        return self.exec_function(payment_frequency_per_year=PF.MONHTLY, **kwargs)

    def semi_monthly(self, **kwargs):
        return self.exec_function(payment_frequency_per_year=PF.SEMI_MONHTLY, **kwargs)

    def bi_monthly(self, **kwargs):
        return self.exec_function(payment_frequency_per_year=PF.BI_MONTHLY, **kwargs)

    def quarterly(self, **kwargs):
        return self.exec_function(payment_frequency_per_year=PF.QUARTERLY, **kwargs)

    def annual(self, **kwargs):
        return self.exec_function(payment_frequency_per_year=PF.ANNUAL, **kwargs)

    def semi_annual(self, **kwargs):
        return self.exec_function(payment_frequency_per_year=PF.SEMI_ANNUAL, **kwargs)

    def weekly(self, **kwargs):
        return self.exec_function(payment_frequency_per_year=PF.WEEKLY, **kwargs)

    def bi_weekly(self, **kwargs):
        return self.exec_function(payment_frequency_per_year=PF.BI_WEEKLY, **kwargs)

    def daily(self, **kwargs):
        return self.exec_function(payment_frequency_per_year=PF.DAILY, **kwargs)
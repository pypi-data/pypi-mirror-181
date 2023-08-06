# py-amortization

Python library for calculating amortizations and generating amortization schedules

## Installation

```bash
pip install py-amortization
```

## Usage

### Python

#### Amortization Amount

```python
from py_amortization import AmortizationAmount
amo_amount = AmortizationAmount(1000, 3)

# amortization amount in case of monthly payment for the period of 12 months
amo_amount.monthly(period=12)

# amortization amount in case of weekly payment for the period of 10 weeks
amo_amount.weekly(period=10)
```

#### Amortization Period

```python
from py_amortization import AmortizationPeriod
amo_period = AmortizationPeriod(1000, 3)

# amortization period in case of monthly payment for amount of 100 per month
amo_period.monthly(amount=100)

# amortization period in case of weekly payment for amount of 100 per week
amo_period.weekly(amount=100)
```

### Amortization Schedule

```python
from py_amortization import AmortizationSchedule
amo_schedule = AmortizationSchedule(1000, 3)

# amortization schedule in case of monthly payment for the period of 12 months
amo_schedule.monthly(period=12)

# amortization schedule in case of weekly payment for for the period of 10 weeks
amo_schedule.weekly(period=10)
```

### frequency types available
    - monthly
    - semi_monthly
    - bi_monthly
    - quarterly
    - annual
    - semi_annual
    - weekly
    - bi_weekly
    - daily


## 0.1.0 (December 13, 2022)
- initital deployment
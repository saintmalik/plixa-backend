from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.money import Money
from djmoney.models.validators import MinMoneyValidator, MaxMoneyValidator
from djmoney.models.fields import MoneyField


class AcceptablePayment(models.TextChoices):
    FULL = "full"
    HALF = "half"
    QUARTER = "quarter"


class ClusterStatus(models.TextChoices):
    OFFLINE = "offline"
    ONLINE = "online"


class Cluster(models.Model):
    """Cluster is a representation of payment collections by an individual or an organization."""

    # TODO: Associate clusters to the individual or organizations that own them.
    name = models.CharField(max_length=128, help_text="the name of the payment cluster")
    description = models.TextField(
        help_text="additional information about what bills the cluster is trying to collect"
    )
    amount = MoneyField(
        _("amount"),
        max_digits=9,
        decimal_places=2,
        default_currency="NGN",
        default=0.00,
        validators=[
            MinMoneyValidator(limit_value=0.00),
            MaxMoneyValidator(limit_value=999.99),
        ],
        help_text="the price tag the cluster aims to charge it's target audience",
    )
    min_acceptable_payment = models.CharField(
        max_length=10,
        choices=AcceptablePayment.choices,
        help_text=(
            "the minimum acceptable amount an audience can pay to the cluster. e.g. "
            "if a cluster charges ₦5,000 from it's target audience and it's `min_acceptable_payment` is "
            "`AcceptablePayment.HALF`, an audience can pay a minimum of ₦2,500"
        ),
    )
    status = models.CharField(
        max_length=10,
        choices=ClusterStatus.choices,
        default=ClusterStatus.OFFLINE,
        help_text=(
            "this shows the state of the cluster and does not need to be modified directly. "
            "clusters are offline by default hence, the cannot accept hence they need to be "
            "deployed with changes it's state from `ClusterStatus.OFFLINE` to `ClusterStatus.ONLINE`"
        ),
    )
    expires_at = models.DateTimeField(
        null=True,
        help_text="if provided, specifies when a cluster should go offline, hence stop accepting payments.",
    )
    metadata = models.JSONField(
        default=dict, help_text="additional information which may be required"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Withdrawal(models.Model):
    """Withdrawal is a representation of withdrawals made by an organization from a cluster as the name implies."""

    cluster = models.ForeignKey(Cluster, on_delete=models.DO_NOTHING)
    reference = models.CharField(max)
    # TODO: Associate clusters to the individual or organizations that own them.
    # beneficiary
    amount = MoneyField(
        _("withdrawal amount"),
        max_digits=9,
        decimal_places=2,
        default_currency="NGN",
        default=0.00,
        validators=[
            MinMoneyValidator(limit_value=0.00),
            MaxMoneyValidator(limit_value=999.99),
        ],
        help_text="the price tag the cluster aims to charge it's target audience",
    )
    metadata = models.JSONField(
        default=dict, help_text="additional information which may be required"
    )
    created_at = models.DateTimeField()


class TransactionStatus(models.TextChoices):
    """TransactionStatus presents all the possible states a Transaction can be in."""

    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"


class Transaction(models.Model):
    """Transaction is a representation of transactions made to a cluster."""

    reference = models.CharField()
    email = models.EmailField()
    amount = MoneyField(
        _("transaction amount"),
        max_digits=9,
        decimal_places=2,
        default_currency="NGN",
        default=0.00,
        validators=[
            MinMoneyValidator(limit_value=0.00),
            MaxMoneyValidator(limit_value=999.99),
        ],
        help_text="the price tag the cluster aims to charge it's target audience",
    )
    status = models.CharField()
    metadata = models.JSONField(
        default=dict, help_text="additional information which may be required"
    )
    created_at = models.DateTimeField()

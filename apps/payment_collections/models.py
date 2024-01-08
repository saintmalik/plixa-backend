import uuid

from django.contrib.auth import get_user_model
from django.db import models


class AcceptablePayment(models.TextChoices):
    FULL = "full"
    HALF = "half"
    QUARTER = "quarter"


class PaymentCollectionStatus(models.TextChoices):
    OFFLINE = "offline"
    ONLINE = "online"


class PaymentCollection(models.Model):
    """Payment collection is a representation of payment collections by an individual or an organization."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="payment_collections"
    )
    name = models.CharField(
        max_length=128, help_text="the name of the payment collection"
    )
    description = models.TextField(
        help_text="additional information about what bills the payment collection is trying to collect"
    )
    amount = models.IntegerField(
        help_text=(
            "the price tag the payment collections aims to charge it's target audience in the "
            "currency's smallest denomination. e.g. If a payment collection accepts NGN, the"
            " amount is expected to be in kobo"
        ),
    )
    min_acceptable_payment = models.CharField(
        max_length=10,
        choices=AcceptablePayment.choices,
        help_text=(
            "the minimum acceptable amount an audience can pay to the payment_collections. e.g. "
            "if a payment_collections charges ₦5,000 from it's target audience and it's `min_acceptable_payment` is "
            "`AcceptablePayment.HALF`, an audience can pay a minimum of ₦2,500"
        ),
    )
    status = models.CharField(
        max_length=10,
        choices=PaymentCollectionStatus.choices,
        default=PaymentCollectionStatus.OFFLINE,
        help_text=(
            "this shows the state of the payment_collections and does not need to be modified directly. "
            "clusters are offline by default hence, the cannot accept hence they need to be "
            "deployed with changes it's state from `ClusterStatus.OFFLINE` to `ClusterStatus.ONLINE`"
        ),
    )
    expires_at = models.DateTimeField(
        null=True,
        help_text="if provided, specifies when a payment_collections should go offline, hence stop accepting payments.",
    )
    metadata = models.JSONField(
        default=dict, help_text="additional information which may be required"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Withdrawal(models.Model):
    """
    Withdrawal is a representation of withdrawals made by an organization
    from a payment_collections as the name implies.
    """

    cluster = models.ForeignKey(PaymentCollection, on_delete=models.DO_NOTHING)
    reference = models.CharField(max)
    # TODO: Associate clusters to the individual or organizations that own them.
    beneficiary = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="withdrawals"
    )
    amount = models.IntegerField(
        help_text=(
            "the amount the owner of a payment collection wishes to withdraw from the collection in the "
            "currency's smallest denomination. e.g. If a payment collection accepts NGN, the"
            " amount is expected to be in kobo"
        ),
    )
    metadata = models.JSONField(
        default=dict, help_text="additional information which may be required"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class TransactionStatus(models.TextChoices):
    """TransactionStatus presents all the possible states a Transaction can be in."""

    PENDING = "pending"
    SUCCESSFUL = "successful"
    FAILED = "failed"


class Transaction(models.Model):
    """Transaction is a representation of transactions made to a payment_collections."""

    reference = models.CharField()
    email = models.EmailField()
    amount = models.IntegerField(
        help_text=(
            "the amount the transaction processes in the "
            "currency's smallest denomination. e.g. If a payment collection accepts NGN, the"
            " amount is expected to be in kobo"
        ),
    )
    status = models.CharField()
    metadata = models.JSONField(
        default=dict, help_text="additional information which may be required"
    )
    created_at = models.DateTimeField(auto_now_add=True)

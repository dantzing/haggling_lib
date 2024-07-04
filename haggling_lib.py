from dataclasses import dataclass
from typing import Optional, Dict
from enum import Enum


class OfferState(Enum):
    START = 0
    NEW = 1
    ACCEPTED = 2
    CANCELLED = 3

@dataclass
class OfferDetails:
    user_id_buyer: str
    user_id_seller: str
    product: str
    quantity: int
    price: float

@dataclass
class OfferUpdate:
    quantity: Optional[int]
    price: Optional[float]

class OfferManager:
    state: OfferState = OfferState.START

    def submit(self, offer: OfferDetails) -> None:
        """

        :param offer:
        :return: None
        """
        # state must be start
        pass
    def accept(self, user_id: str) -> None:
        # state must be awaiting user_id
        pass

    def cancel(self, user_id: str) -> None:
        # any state except start
        pass

    def propose_update(self, user_id: str, update: OfferUpdate) -> None:
        # state must be awaiting the user submitting the update
        pass

    def withdraw(self, user_id: str) -> None:
        # state must be awaiting the other person
        pass

    def update_private_date(self, user_id: str, private_data: Dict) -> None:
        # always allowed
        pass

"""
operations

submit
accept
cancel
propose_update
withdraw
update_private_data

can a single user have multiple offers on a single product at one time?
no, doesn't make sense, offer key is buyer, seller, product
but it would be simpler, otherwise submitting new bid on existing has to be mapped
to propose update

After submission, product detail is implicit, OfferManager manages
only one initial offer, all subsequent actions are for the same product

can you change the product during the haggling?
"""
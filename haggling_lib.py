from dataclasses import dataclass
from typing import Optional, Dict, List
from enum import Enum


class OfferState(Enum):
    START = 0
    WAITING_BUYER = 1
    WAITING_SELLER = 2
    WITHDRAWN_BUYER = 3
    WITHDRAWN_SELLER = 4
    ACCEPTED = 5
    CANCELLED = 6


class UserType(Enum):
    BUYER = 1
    SELLER = 2


@dataclass
class OfferDetails:
    user_id_buyer: str
    user_id_seller: str
    product: str
    quantity: int
    price: float


@dataclass
class OfferUpdate:
    quantity: Optional[int] = None
    price: Optional[float] = None


class OfferManager:
    _state: OfferState = OfferState.START
    _offer: OfferDetails = None

    @property
    def state(self) -> OfferState:
        return self._state

    def submit(self, offer: OfferDetails) -> None:
        self._validate_state([OfferState.START], True)
        self._offer = offer
        self._state = OfferState.WAITING_SELLER

    def accept(self, user_id: str) -> None:
        # state must be awaiting user_id
        user_type = self._find_user_type(user_id)
        if user_type == UserType.SELLER:
            self._validate_state([OfferState.WAITING_SELLER], True)
        else:
            self._validate_state([OfferState.WAITING_BUYER], True)
        self._state = OfferState.ACCEPTED

    def cancel(self, user_id: str) -> None:
        self._validate_state([OfferState.START], False)
        self._state = OfferState.CANCELLED

    def propose_update(self, user_id: str, update: OfferUpdate) -> None:
        user_type = self._find_user_type(user_id)
        allowed_states = None
        if user_type == UserType.SELLER:
            allowed_states = \
                [OfferState.WAITING_SELLER, OfferState.WITHDRAWN_SELLER]
        else:
            allowed_states = \
                [OfferState.WAITING_BUYER, OfferState.WITHDRAWN_BUYER]
        self._validate_state(allowed_states, True)
        self._offer.price = update.price if update.price is not None \
            else self._offer.price
        self._offer.quantity = update.quantity if update.quantity is not None \
            else self._offer.quantity
        if user_type == UserType.SELLER:
            self._state = OfferState.WAITING_BUYER
        else:
            self._state = OfferState.WAITING_SELLER

    def withdraw(self, user_id: str) -> None:
        # state must be awaiting the other person
        user_type = self._find_user_type(user_id)
        if user_type == UserType.SELLER:
            self._validate_state([OfferState.WAITING_BUYER], True)
            self._state = OfferState.WITHDRAWN_SELLER
        else:
            self._validate_state([OfferState.WAITING_SELLER], True)
            self._state = OfferState.WITHDRAWN_BUYER

    def update_private_data(self, user_id: str, private_data: Dict) -> None:
        # always allowed
        pass

    def _validate_state(self, states: List[OfferState], flag: bool) -> None:
        valid = False
        if flag:
            valid = self._state in states
        else:
            valid = self._state not in states
        if not valid:
            raise ValueError(f'self._state={self._state} states={states} \
                flag={flag}')

    def _find_user_type(self, user_id: str) -> UserType:
        if user_id == self._offer.user_id_buyer:
            return UserType.BUYER
        elif user_id == self._offer.user_id_seller:
            return UserType.SELLER
        else:
            raise ValueError(f'user_id {user_id} not recognised')

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
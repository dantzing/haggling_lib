import haggling_lib as hl
import pytest


class TestHagglingLib:
    def test_successful_purchase(self):
        manager = hl.OfferManager()
        manager.submit(hl.OfferDetails('superman', 'batman', 'batmobile', 5, 500))
        manager.accept('batman')
        assert manager.state == hl.OfferState.ACCEPTED

    def test_counteroffer(self):
        manager = hl.OfferManager()
        manager.submit(hl.OfferDetails('superman', 'batman', 'batmobile', 5, 500))
        manager.propose_update('batman', hl.OfferUpdate(price=550))
        manager.accept('superman')
        assert manager.state == hl.OfferState.ACCEPTED

    def test_withdrawn_offer(self):
        manager = hl.OfferManager()
        manager.submit(hl.OfferDetails('superman', 'batman', 'batmobile', 5, 500))
        manager.withdraw('superman')
        manager.propose_update('superman', hl.OfferUpdate(price=450))
        manager.accept('batman')
        assert manager.state == hl.OfferState.ACCEPTED

    def test_invalid_action(self):
        manager = hl.OfferManager()
        manager.submit(hl.OfferDetails('superman', 'batman', 'batmobile', 5, 500))
        with pytest.raises(ValueError):
            manager.propose_update('superman', hl.OfferUpdate(price=450))

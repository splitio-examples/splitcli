from experiment.event_result import EventResult
from tests.experiment_tests.tracking_client import TrackingClient

import itertools
import pytest

def test_probability():
    sample = 1000
    base_client = TrackingClient()
    comp_client = TrackingClient()
    (base, comp) = EventResult("test", {}, sample).probability(0.5, 10).generators()

    for i in range(sample):
        base.events(base_client, f"off_{i}", i)
        comp.events(comp_client, f"on_{i}", i)

    assert base_client.rate_mean(sample) == 0.5
    assert base_client.count_mean(sample) == 0.5
    assert base_client.sum_mean(sample) == 0.0
    assert base_client.average_mean(sample) == 0.0

    assert comp_client.rate_mean(sample) == 0.55
    assert comp_client.count_mean(sample) == 0.55
    assert comp_client.sum_mean(sample) == 0.0
    assert comp_client.average_mean(sample) == 0.0

def test_count():
    sample = 1000
    base_client = TrackingClient()
    comp_client = TrackingClient()
    (base, comp) = EventResult("test", {}, sample).count(4, 25, 0.5).generators()
    
    for i in range(sample):
        base.events(base_client, i, i)
        comp.events(comp_client, i, i)

    assert base_client.rate_mean(sample) == 1.0
    assert base_client.count_mean(sample) == pytest.approx(4.0, rel=0.05)
    assert base_client.sum_mean(sample) == 0.0
    assert base_client.average_mean(sample) == 0.0

    assert comp_client.rate_mean(sample) == 1.0
    assert comp_client.count_mean(sample) == pytest.approx(5.0, rel=0.05)
    assert comp_client.sum_mean(sample) == 0.0
    assert comp_client.average_mean(sample) == 0.0

def test_count_prob():
    sample = 1000
    base_client = TrackingClient()
    comp_client = TrackingClient()
    (base, comp) = EventResult("test", {}, sample).probability(0.5, 10).count(4, 25, 0.5).generators()
    
    for i in range(sample):
        base.events(base_client, i, i)
        comp.events(comp_client, i, i)

    assert base_client.rate_mean(sample) == 0.5
    assert base_client.count_mean(sample) == pytest.approx(4.0, rel=0.05)
    assert base_client.sum_mean(sample) == 0.0
    assert base_client.average_mean(sample) == 0.0

    assert comp_client.rate_mean(sample) == 0.55
    assert comp_client.count_mean(sample) == pytest.approx(5.0, rel=0.05)
    assert comp_client.sum_mean(sample) == 0.0
    assert comp_client.average_mean(sample) == 0.0

def test_count_error():
    sample = 10000
    base_client = TrackingClient()
    comp_client = TrackingClient()
    (base, comp) = EventResult("test", {}, sample).probability(.02,40).count(1.5, 10, .9).value(0,0,1).generators()
    
    for i in range(sample):
        base.events(base_client, i, i)
        comp.events(comp_client, i, i)
    
    print(base.count_supplier.__dict__)
    print(comp.count_supplier.__dict__)

    print(base.count_supplier.idealNextForMean())
    print(base.count_supplier.sampleInterval())

    assert base_client.rate_mean(sample) == 0.02
    assert base_client.count_mean(sample) == pytest.approx(1.5, rel=0.05)
    assert base_client.sum_mean(sample) == 0.0
    assert base_client.average_mean(sample) == 0.0

    assert comp_client.rate_mean(sample) == 0.028
    assert comp_client.count_mean(sample) == pytest.approx(1.65, rel=0.05)
    assert comp_client.sum_mean(sample) == 0.0
    assert comp_client.average_mean(sample) == 0.0
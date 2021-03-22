from experiment.event_result import EventResult
from tests.experiment_tests.tracking_client import TrackingClient

import itertools
import pytest

def test_probability():
    sample = 10
    base_client = TrackingClient()
    comp_client = TrackingClient()
    
    result = EventResult("test", {}, sample).probability(.10, .5, 0.5)
    result.track_base(base_client)
    result.track_comp(comp_client)

    assert base_client.rate_mean(sample) == 0.5
    assert base_client.count_mean(sample) == 0.5
    assert base_client.sum_mean(sample) == 0.0
    assert base_client.average_mean(sample) == 0.0

    assert comp_client.rate_mean(sample) == 0.55
    assert comp_client.count_mean(sample) == 0.55
    assert comp_client.sum_mean(sample) == 0.0
    assert comp_client.average_mean(sample) == 0.0

def test_count():
    sample = 100
    base_client = TrackingClient()
    comp_client = TrackingClient()
    
    result = EventResult("test", {}, sample).count(.25, 0.2, 100)
    result.track_base(base_client)
    result.track_comp(comp_client)

    print({"variance": base_client.count_variance(sample)})

    assert base_client.rate_mean(sample) == 1.0
    assert base_client.count_mean(sample) == pytest.approx(4.0, rel=0.05)
    assert base_client.count_variance(sample) == 0
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
    
    result = EventResult("test", {}, sample).probability(.50, .5, 0.5).count(.25, 0.005, 100)
    result.track_base(base_client)
    result.track_comp(comp_client)
    
    print({"variance": base_client.count_variance(sample)})

    assert base_client.rate_mean(sample) == 0.5
    assert base_client.count_mean(sample) == pytest.approx(4.0, rel=0.05)
    assert base_client.sum_mean(sample) == 0.0
    assert base_client.average_mean(sample) == 0.0

    assert comp_client.rate_mean(sample) == 0.55
    assert comp_client.count_mean(sample) == pytest.approx(5.0, rel=0.05)
    assert comp_client.sum_mean(sample) == 0.0
    assert comp_client.average_mean(sample) == 0.0

# def test_count_error():
#     sample = 10000
#     base_client = TrackingClient()
#     comp_client = TrackingClient()
    
#     result = EventResult("test", {}, sample).probability(.4, 1, .02).count(.10, .9, 1.5).value(0,1,0)
#     result.track_base(base_client)
#     result.track_comp(comp_client)

#     assert base_client.rate_mean(sample) == 0.02
#     assert base_client.count_mean(sample) == pytest.approx(1.5, rel=0.05)
#     assert base_client.sum_mean(sample) == 0.0
#     assert base_client.average_mean(sample) == 0.0

#     assert comp_client.rate_mean(sample) == 0.028
#     assert comp_client.count_mean(sample) == pytest.approx(1.65, rel=0.05)
#     assert comp_client.sum_mean(sample) == 0.0
#     assert comp_client.average_mean(sample) == 0.0
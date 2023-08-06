import numpy as np
import pytest

from eerily.generators.utils.noises import LogNormalNoise


@pytest.mark.parametrize(
    "mu,std,expected",
    [
        (
            1,
            0.3,
            [
                2.978486018476435,
                1.9897415742703028,
                3.4046268976160845,
                3.604450799108567,
                1.5139005158889947,
                1.8392284222498556,
                2.824558646174046,
                2.4722464279201573,
                2.704615215288275,
                2.10451875643865,
            ],
        )
    ],
)
def test_lognormal_noise(mu, std, expected):
    seed = 42
    lnn = LogNormalNoise(mu=mu, std=std, seed=seed)

    length = 10
    values = np.array([next(lnn) for _ in range(length)])
    expected = np.array(expected)

    np.testing.assert_allclose(values, expected)

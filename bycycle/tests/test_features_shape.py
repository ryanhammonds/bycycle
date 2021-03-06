"""Tests the cycle-by-cycle shape feature computation function."""

import numpy as np
import pytest

from bycycle.cyclepoints import find_extrema, find_zerox
from bycycle.features import compute_shape_features, compute_samples

###################################################################################################
###################################################################################################


@pytest.mark.parametrize("find_extrema_kwargs",
    [
        None,
        pytest.param({'first_extrema': 'peak'}, marks=pytest.mark.xfail)
    ]
)
@pytest.mark.parametrize("center_extrema",
    [
        'peak',
        'trough',
        pytest.param(None, marks=pytest.mark.xfail)
    ]
)
@pytest.mark.parametrize("return_samples", [True, False])
def test_compute_shape_features(sim_args, find_extrema_kwargs, center_extrema, return_samples):

    sig = sim_args['sig']
    fs = sim_args['fs']
    f_range = sim_args['f_range']

    if return_samples:

        df_shapes, df_samples = \
            compute_shape_features(sig, fs, f_range, center_extrema=center_extrema,
                                   find_extrema_kwargs=find_extrema_kwargs,
                                   hilbert_increase_n=False, return_samples=return_samples)

        assert len(df_shapes) == len(df_samples)

    else:

        df_shapes = compute_shape_features(sig, fs, f_range, center_extrema=center_extrema,
                                           find_extrema_kwargs=find_extrema_kwargs,
                                           hilbert_increase_n=False,
                                           return_samples=return_samples)

    # Assert that np.nan isn't dataframe(s), with the exception of the first and last row
    for idx, row in df_shapes.iterrows():

        assert not np.isnan(row[1:-1]).any()

        if return_samples:

            assert not np.isnan(df_samples.iloc[idx]).any()

    # Check inverted signal gives appropriately opposite data
    extrema_opp = 'trough' if center_extrema == 'peak' else 'peak'

    df_opp = compute_shape_features(-sig, fs, f_range, center_extrema=extrema_opp,
                                    find_extrema_kwargs=find_extrema_kwargs,
                                    hilbert_increase_n=False,
                                    return_samples=False)

    cols_peak = ['time_peak', 'time_rise', 'volt_rise',
                 'volt_amp', 'period', 'time_rdsym', 'time_ptsym']
    cols_trough = ['time_trough', 'time_decay', 'volt_decay',
                   'volt_amp', 'period', 'time_rdsym', 'time_ptsym']

    df_opp['time_rdsym'] = 1 - df_opp['time_rdsym']
    df_opp['time_ptsym'] = 1 - df_opp['time_ptsym']


    for idx, col in enumerate(cols_peak):

        if center_extrema == 'peak':
            np.testing.assert_allclose(df_shapes.loc[:, col], df_opp.loc[:, cols_trough[idx]])
        else:
            np.testing.assert_allclose(df_opp.loc[:, col], df_shapes.loc[:, cols_trough[idx]])


def test_compute_samples(sim_args):

    sig = sim_args['sig']
    fs = sim_args['fs']
    f_range = sim_args['f_range']

    ps, ts = find_extrema(sig, fs, f_range)
    rises, decays = find_zerox(sig, ps, ts)

    df_samples = compute_samples(ps, ts, decays, rises)

    assert (df_samples['sample_peak'] == ps[1:]).all()
    assert (df_samples['sample_zerox_decay'] == decays[1:]).all()
    assert (df_samples['sample_zerox_rise'] == rises).all()
    assert (df_samples['sample_last_trough'] == ts[:-1]).all()
    assert (df_samples['sample_next_trough'] == ts[1:]).all()

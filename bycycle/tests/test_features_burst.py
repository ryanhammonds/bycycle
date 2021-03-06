"""Tests the cycle-by-cycle burst feature computation function."""

import numpy as np
import pytest

from bycycle.features import compute_burst_features

###################################################################################################
###################################################################################################


@pytest.mark.parametrize("dual_thresh", [True, False])
@pytest.mark.parametrize("center_e", ['peak', 'trough'])
def test_compute_burst_features(sim_args, dual_thresh, center_e):

    sig = sim_args['sig']
    df_shape_features = sim_args['df_shapes']
    df_samples = sim_args['df_samples']

    if center_e == 'trough':

        # Swap column names (fixture is peak centered)
        rename_dict = {'sample_peak': 'sample_trough',
                       'sample_zerox_decay': 'sample_zerox_rise',
                       'sample_zerox_rise': 'sample_zerox_decay',
                       'sample_last_trough': 'sample_last_peak',
                       'sample_next_trough': 'sample_next_peak'}

        df_samples.rename(columns=rename_dict, inplace=True)

    if dual_thresh:

        # Use dual threshold burst detecion.
        dual_threshold_kwargs = {'fs': sim_args['fs'], 'f_range': sim_args['f_range']}

        df_burst_features = compute_burst_features(df_shape_features, df_samples, sig,
                                                   dual_threshold_kwargs=dual_threshold_kwargs)

        burst_fraction = df_burst_features['burst_fraction']

        assert np.nan not in burst_fraction

        assert np.all((burst_fraction >= 0) & (burst_fraction <= 1))

    else:

        # Use consistency burst detection
        df_burst_features = compute_burst_features(df_shape_features, df_samples,
                                                   sig, dual_threshold_kwargs=None)

        amplitude_fraction = df_burst_features['amplitude_fraction'].values[1:-1]
        amplitude_consistency = df_burst_features['amplitude_consistency'].values[1:-1]
        period_consistency = df_burst_features['period_consistency'].values[1:-1]
        monotonicity = df_burst_features['monotonicity'].values[1:-1]

        assert np.all((amplitude_fraction >= 0) & (amplitude_fraction <= 1))
        assert np.all((amplitude_consistency >= 0) & (amplitude_consistency <= 1))
        assert np.all((period_consistency >= 0) & (period_consistency <= 1))
        assert np.all((monotonicity >= 0) & (monotonicity <= 1))

    assert len(df_shape_features) == len(df_burst_features)

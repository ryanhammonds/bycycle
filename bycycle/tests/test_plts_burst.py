"""Tests plotting bursts."""

import numpy as np
import pytest

from bycycle.burst import detect_bursts_cycles
from bycycle.plts import plot_burst_detect_param, plot_burst_detect_summary
from bycycle.tests.utils import plot_test
from bycycle.tests.settings import TEST_PLOTS_PATH

###################################################################################################
###################################################################################################

@plot_test
@pytest.mark.parametrize("interp", [True, False])
def test_plot_burst_detect_param(sim_args, interp):

    df_samples = sim_args['df_samples']
    df_features = sim_args['df_features']
    sig = sim_args['sig']
    fs = sim_args['fs']

    thresh = np.nanmin(df_features['amplitude_consistency'].values) + 0.1

    plot_burst_detect_param(df_features, df_samples, sig, fs, 'amplitude_consistency',
                            thresh, interp=interp, save_fig=True,
                            file_path=TEST_PLOTS_PATH, file_name='test_plot_burst_detect_param')


@plot_test
@pytest.mark.parametrize("plot_only_result", [True, False])
def test_plot_burst_detect_summary(sim_args, plot_only_result):

    burst_detection_kwargs = {'amplitude_fraction_threshold': 1.1,
                              'amplitude_consistency_threshold': .5,
                              'period_consistency_threshold': .5,
                              'monotonicity_threshold': .8,
                              'n_cycles_min': 3}

    df_samples = sim_args['df_samples']
    df_features = sim_args['df_features']
    sig = sim_args['sig']
    fs = sim_args['fs']

    df_features = detect_bursts_cycles(df_features, **burst_detection_kwargs)

    plot_burst_detect_summary(df_features, df_samples, sig, fs, burst_detection_kwargs,
                              plot_only_result=plot_only_result,
                              save_fig=True, file_path=TEST_PLOTS_PATH,
                              file_name='test_plot_burst_detect_summary')

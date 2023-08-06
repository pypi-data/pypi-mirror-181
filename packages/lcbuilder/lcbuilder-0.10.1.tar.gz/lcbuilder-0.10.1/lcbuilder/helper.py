from math import floor, ceil

import foldedleastsquares
import numpy as np
from foldedleastsquares import DefaultTransitTemplateGenerator
from lcbuilder import constants
from scipy import stats


class LcbuilderHelper:
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def compute_t0s(time, period, t0, duration):
        last_time = time[len(time) - 1]
        first_time = time[0]
        num_of_transits_back = int(floor(((t0 - first_time) / period)))
        transits_lists_back = t0 - period * np.arange(num_of_transits_back, 0,
                                                      -1) if num_of_transits_back > 0 else np.array([])
        num_of_transits = int(ceil(((last_time - t0) / period)))
        transit_lists = t0 + period * np.arange(0, num_of_transits)
        transit_lists = np.append(transits_lists_back, transit_lists)
        plot_range = duration * 2
        transits_in_data = [
            time[(transit > time - plot_range) & (transit < time + plot_range)] for
            transit in transit_lists]
        transit_t0s_list = transit_lists[[len(transits_in_data_set) > 0 for transits_in_data_set in transits_in_data]]
        return transit_t0s_list

    @staticmethod
    def mask_transits(time, flux, period, duration, epoch, flux_err=None):
        mask = foldedleastsquares.transit_mask(time, period, duration, epoch)
        time = time[~mask]
        flux = flux[~mask]
        if flux_err is not None:
            flux_err = flux_err[~mask]
        return time, flux, flux_err

    @staticmethod
    def correct_epoch(mission, epoch):
        result = epoch
        if mission == constants.MISSION_TESS and epoch - constants.TBJD > 0:
            result = epoch - constants.TBJD
        elif (mission == constants.MISSION_K2 or mission == constants.MISSION_KEPLER) and epoch - constants.KBJD > 0:
            result = epoch - constants.TBJD
        return result

    @staticmethod
    def bin(time, values, bins, values_err=None, bin_err_mode='values_std'):
        if len(time) <= bins:
            value_err = values_err if values_err is not None else np.nanstd(values)
            time_err = (time[1] - time[0]) if len(time) > 1 else np.nan
            return time, values, time_err, value_err
        bin_means, bin_edges, binnumber = stats.binned_statistic(time, values, statistic='mean', bins=bins)
        if bin_err_mode == 'flux_err':
            bin_stds, _, _ = stats.binned_statistic(time, values_err, statistic='mean', bins=bins)
        else:
            bin_stds, _, _ = stats.binned_statistic(time, values, statistic='std', bins=bins)
        bin_width = (bin_edges[1] - bin_edges[0])
        bin_centers = bin_edges[1:] - bin_width / 2
        bin_means_data_mask = np.isnan(bin_means)
        bin_centers = bin_centers[~bin_means_data_mask]
        bin_means = bin_means[~bin_means_data_mask]
        bin_stds = bin_stds[~bin_means_data_mask]
        return bin_centers, bin_means, bin_width, bin_stds

    @staticmethod
    def calculate_period_grid(time, min_period, max_period, oversampling, star_info, transits_min_count,
                              max_oversampling=15):
        time_span_curve = time[-1] - time[0]
        dif = time[1:] - time[:-1]
        jumps = np.where(dif > 1)[0]
        jumps = np.append(jumps, len(time) - 1)
        previous_jump_index = 0
        time_span_all_sectors = 0
        empty_days = 0
        for jumpIndex in jumps[0:-1]:
            empty_days = empty_days + time[jumpIndex + 1] - time[jumpIndex - 1]
        if oversampling is None:
            oversampling = int(1 / ((time_span_curve - empty_days) / time_span_curve))
            oversampling = oversampling if oversampling < max_oversampling else max_oversampling
            oversampling = oversampling if oversampling > 3 else 3
        for jumpIndex in jumps:
            time_chunk = time[
                         previous_jump_index + 1:jumpIndex]  # ignoring first measurement as could be the last from the previous chunk
            if len(time_chunk) > 0:
                time_span_all_sectors = time_span_all_sectors + (time_chunk[-1] - time_chunk[0])
            previous_jump_index = jumpIndex
        return DefaultTransitTemplateGenerator() \
                   .period_grid(star_info.radius, star_info.mass, time_span_curve, min_period,
                                max_period, oversampling, transits_min_count, time_span_curve), oversampling

    @staticmethod
    def compute_cadence(time):
        cadence_array = np.diff(time) * 24 * 60 * 60
        cadence_array = cadence_array[~np.isnan(cadence_array)]
        cadence_array = cadence_array[cadence_array > 0]
        return int(np.round(np.nanmedian(cadence_array)))

    @staticmethod
    def estimate_transit_cadences(cadence_s, duration_d):
        cadence = cadence_s / 3600 / 24
        return duration_d // cadence

    @staticmethod
    def mission_lightkurve_sector_extraction(mission, lightkurve_item):
        sector_name = None
        sector = None
        if mission == constants.MISSION_TESS:
            sector = lightkurve_item.sector
            sector_name = 'sector'
        elif mission == constants.MISSION_KEPLER:
            sector = lightkurve_item.quarter
            sector_name = 'quarter'
        elif mission == constants.MISSION_K2:
            sector = lightkurve_item.campaign
            sector_name = 'campaign'
        return sector_name, sector

    @staticmethod
    def mission_pixel_size(mission):
        px_size_arcs = None
        if mission == constants.MISSION_TESS:
            px_size_arcs = 20.25
        elif mission == constants.MISSION_KEPLER:
            px_size_arcs = 4
        elif mission == constants.MISSION_K2:
            px_size_arcs = 4
        return px_size_arcs

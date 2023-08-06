import numpy as np
import pandas as pd
from scipy.integrate import cumtrapz
from worklab.utils import lowpass_butter
from worklab.imu import push_imu
from scipy.signal import find_peaks


def butterfly(data, sfreq: float = 400.):
    """
    Calculate butterfly sprint test outcome measures.

    Parameters
    ----------
    data : dict or pd.Series
        processed sessiondata structure or pd.Series with frame data
    sfreq : float
        sampling frequency

    Returns
    -------
    data : pd.Series
        pd.Series with Butterfly sprint test data
    outcomes_bs : pd.Series
        pd.Series with most important outcome variables of the Butterfly sprint test
    """

    vel = "vel"
    if type(data) == dict:
        data = data["frame"]

    data[vel] = lowpass_butter(data[vel], sfreq=sfreq, cutoff=10)

    m = int(len(data[vel]) - (0.5 * sfreq))
    for st in range(1, m):
        if data[vel][st] > 0.1:
            if data[vel][int(st + (0.5 * sfreq))] > 1.0:
                start_value = st
                break
    data = data[start_value:].reset_index(drop=True)
    data["dist"] = cumtrapz(data[vel], initial=0.0) / sfreq

    data["dist_y"] = cumtrapz(np.gradient(data["dist"]) * np.sin(
        np.deg2rad(cumtrapz(data["rot_vel"] / sfreq, initial=0.0))), initial=0.0)
    data["dist_x"] = cumtrapz(np.gradient(data["dist"]) * np.cos(
        np.deg2rad(cumtrapz(data["rot_vel"] / sfreq, initial=0.0))), initial=0.0)

    end_point = int(pd.DataFrame(data["dist_x"]).idxmin())

    dist_x_zero = data["dist_x"][end_point:]
    find_end = dist_x_zero[dist_x_zero > 0]
    end_value = find_end.index[0]

    data = data[:end_value]
    data["time"] -= data['time'][0]
    data["rot_vel_left"] = data["rot_vel"][data["rot_vel"] > 30]
    data["rot_vel_right"] = data["rot_vel"][data["rot_vel"] < -30]

    outcomes_bs = dict()
    outcomes_bs['endtime'] = end_value / sfreq
    outcomes_bs['vel_mean'] = np.mean(data[vel])
    outcomes_bs['vel_peak'] = np.max(data[vel])
    outcomes_bs['acc_peak'] = np.max(data["acc"])
    outcomes_bs['rot_vel_mean_right'] = np.mean(data["rot_vel_right"])
    outcomes_bs['rot_vel_mean_left'] = np.mean(data["rot_vel_left"])
    outcomes_bs['rot_vel_peak_right'] = np.min(data["rot_vel_right"])
    outcomes_bs['rot_vel_peak_left'] = np.max(data["rot_vel_left"])
    outcomes_bs['rot_acc_peak'] = np.max(data["rot_acc"])

    outcomes_bs = pd.DataFrame([outcomes_bs])
    outcomes_bs = round(outcomes_bs, 2)
    return data, outcomes_bs


def illinois(data, sfreq: float = 400.):
    """
    Calculate illinois test outcome measures.

    Parameters
    ----------
    data : dict or pd.Series
        processed sessiondata structure or pd.Series with frame data
    sfreq : float
        sampling frequency

    Returns
    -------
    data : pd.Series
        pd.Series with Illinois test data
    outcomes_il : pd.Series
        pd.Series with most important outcome variables of the Illinois test
    """

    vel = "vel"
    if type(data) == dict:
        data = data["frame"]

    data[vel] = lowpass_butter(data[vel], sfreq=sfreq, cutoff=10)

    m = int(len(data[vel]) - (0.5 * sfreq))
    for st in range(1, m):
        if data[vel][st] > 0.1:
            if data[vel][int(st + (0.5 * sfreq))] > 1.0:
                start_value = st
                break
    data = data[start_value:].reset_index(drop=True)
    data["dist"] = cumtrapz(data[vel], initial=0.0) / sfreq

    data["dist_y"] = cumtrapz(np.gradient(data["dist"]) * np.sin(
        np.deg2rad(cumtrapz(data["rot_vel"] / sfreq, initial=0.0))), initial=0.0)
    data["dist_x"] = cumtrapz(np.gradient(data["dist"]) * np.cos(
        np.deg2rad(cumtrapz(data["rot_vel"] / sfreq, initial=0.0))), initial=0.0)

    peaks, _ = find_peaks(data["dist_x"])
    end_point = peaks[-1]

    dist_x_zero = data["dist_x"][end_point:]
    find_end = dist_x_zero[dist_x_zero < 0]
    end_value = find_end.index[0]

    data = data[:end_value]
    data["time"] -= data['time'][0]
    data["rot_vel_left"] = data["rot_vel"][data["rot_vel"] > 30]
    data["rot_vel_right"] = data["rot_vel"][data["rot_vel"] < -30]

    outcomes_il = dict()
    outcomes_il['endtime'] = end_value / sfreq
    outcomes_il['vel_mean'] = np.mean(data[vel])
    outcomes_il['vel_peak'] = np.max(data[vel])
    outcomes_il['acc_peak'] = np.max(data["acc"])
    outcomes_il['rot_vel_mean_right'] = np.mean(data["rot_vel_right"])
    outcomes_il['rot_vel_mean_left'] = np.mean(data["rot_vel_left"])
    outcomes_il['rot_vel_peak_right'] = np.min(data["rot_vel_right"])
    outcomes_il['rot_vel_peak_left'] = np.max(data["rot_vel_left"])
    outcomes_il['rot_acc_peak'] = np.max(data["rot_acc"])

    outcomes_il = pd.DataFrame([outcomes_il])
    outcomes_il = round(outcomes_il, 2)
    return data, outcomes_il


def sprint_10m(data, sfreq: float = 400.):
    """
    Calculate 10m sprint test outcomes measures.

    Parameters
    ----------
    data : dict or pd.Series
        processed sessiondata structure or pd.Series with frame data
    sfreq : float
        sampling frequency

    Returns
    -------
    data : pd.Series
        pd.Series with 10m sprint data
    outcomes_sprint : pd.Series
        pd.Series with most important outcome variables of the 10m sprint test
    """

    vel = "vel"
    if type(data) == dict:
        data = data["frame"]

    data[vel] = lowpass_butter(data[vel], sfreq=sfreq, cutoff=10)

    m = int(len(data[vel]) - (0.5 * sfreq))
    for st in range(1, m):
        if data[vel][st] > 0.1:
            if data[vel][int(st + (0.5 * sfreq))] > 1.0:
                start_value = st
                break
    data = data[start_value:].reset_index(drop=True)
    data["dist"] = cumtrapz(data[vel], initial=0.0) / sfreq

    data["dist_y"] = cumtrapz(np.gradient(data["dist"]) * np.sin(
        np.deg2rad(cumtrapz(data["rot_vel"] / sfreq, initial=0.0))), initial=0.0)
    data["dist_x"] = cumtrapz(np.gradient(data["dist"]) * np.cos(
        np.deg2rad(cumtrapz(data["rot_vel"] / sfreq, initial=0.0))), initial=0.0)

    n10 = int(len(data["dist_x"]))
    for val2 in range(0, n10):
        if data["dist_x"][val2] > 2:
            two_value = val2
            break
    for val5 in range(0, n10):
        if data["dist_x"][val5] > 5:
            five_value = val5
            break
    for val10 in range(0, n10):
        if data["dist_x"][val10] > 10:
            end_value = val10
            break

    data = data[:end_value]
    data["time"] -= data['time'][0]
    push_ind, acc_filt, n_pushes, cycle_time, push_freq = push_imu(
        data["accelerometer_x"], sfreq=sfreq)

    outcomes_sprint = dict()
    outcomes_sprint['time_2m'] = two_value / sfreq
    outcomes_sprint['time_5m'] = five_value / sfreq
    outcomes_sprint['time_10m'] = end_value / sfreq
    outcomes_sprint['vel_2m_peak'] = np.max(data[vel][:two_value])
    outcomes_sprint['vel_5m_peak'] = np.max(data[vel][two_value:five_value])
    outcomes_sprint['vel_10m_peak'] = np.max(data[vel][five_value:end_value])
    outcomes_sprint['pos_vel_peak'] = data["dist_x"][data[vel].idxmax()]
    outcomes_sprint['vel_mean'] = np.mean(data[vel])
    outcomes_sprint['vel_peak'] = np.max(data[vel])
    outcomes_sprint['acc_2m_peak'] = np.max(data["acc"][:two_value])
    outcomes_sprint['acc_5m_peak'] = np.max(data["acc"][two_value:five_value])
    outcomes_sprint['acc_10m_peak']: np.max(data["acc"][five_value:end_value])
    outcomes_sprint['acc_peak'] = np.max(data["acc"])
    outcomes_sprint['pos_acc_peak'] = data["dist_x"][data["acc"].idxmax()]
    outcomes_sprint['n_pushes'] = n_pushes
    outcomes_sprint['dist_push1'] = data["dist_x"][push_ind[0]]
    outcomes_sprint['dist_push2'] = data["dist_x"][push_ind[1]]
    outcomes_sprint['dist_push3'] = data["dist_x"][push_ind[2]]
    outcomes_sprint['cycle_time'] = np.mean(cycle_time[0])

    outcomes_sprint = pd.DataFrame([outcomes_sprint])
    outcomes_sprint = round(outcomes_sprint, 2)
    return data, outcomes_sprint


def sprint_20m(data, sfreq: float = 400.):
    """
    Calculate 20m sprint outcomes measures.

    Parameters
    ----------
    data : dict or pd.Series
        processed sessiondata structure or pd.Series with frame data
    sfreq : float
        sampling frequency

    Returns
    -------
    data : pd.Series
        pd.Series with 20m sprint data
    outcomes_sprint : pd.Series
        pd.Series with most important outcome variables of the 20m sprint test
    """

    vel = "vel"
    if type(data) == dict:
        data = data["frame"]

    data[vel] = lowpass_butter(data[vel], sfreq=sfreq, cutoff=10)

    m = int(len(data[vel]) - (0.5 * sfreq))
    for st in range(1, m):
        if data[vel][st] > 0.1:
            if data[vel][int(st + (0.5 * sfreq))] > 1.0:
                start_value = st
                break
    data = data[start_value:].reset_index(drop=True)
    data["dist"] = cumtrapz(data[vel], initial=0.0) / sfreq

    data["dist_y"] = cumtrapz(np.gradient(data["dist"]) * np.sin(
        np.deg2rad(cumtrapz(data["rot_vel"] / sfreq, initial=0.0))), initial=0.0)
    data["dist_x"] = cumtrapz(np.gradient(data["dist"]) * np.cos(
        np.deg2rad(cumtrapz(data["rot_vel"] / sfreq, initial=0.0))), initial=0.0)

    n20 = int(len(data["dist_x"]))
    for val5 in range(0, n20):
        if data["dist_x"][val5] > 5:
            five_value = val5
            break
    for val10 in range(0, n20):
        if data["dist_x"][val10] > 10:
            ten_value = val10
            break
    for val20 in range(0, n20):
        if data["dist_x"][val20] > 20:
            end_value = val20
            break

    data = data[:end_value]
    data["time"] -= data['time'][0]
    push_ind, acc_filt, n_pushes, cycle_time, push_freq = push_imu(
        data["accelerometer_x"], sfreq=sfreq)

    outcomes_sprint = dict()
    outcomes_sprint['time_5m'] = five_value / sfreq
    outcomes_sprint['time_10m'] = ten_value / sfreq
    outcomes_sprint['time_20m'] = end_value / sfreq
    outcomes_sprint['vel_5m_peak'] = np.max(data[vel][:five_value])
    outcomes_sprint['vel_10m_peak'] = np.max(data[vel][five_value:ten_value])
    outcomes_sprint['vel_20m_peak'] = np.max(data[vel][ten_value:end_value])
    outcomes_sprint['pos_vel_peak'] = data["dist_x"][data[vel].idxmax()]
    outcomes_sprint['vel_mean'] = np.mean(data[vel])
    outcomes_sprint['vel_peak'] = np.max(data[vel])
    outcomes_sprint['acc_5m_peak'] = np.max(data["acc"][:five_value])
    outcomes_sprint['acc_10m_peak'] = np.max(data["acc"][five_value:ten_value])
    outcomes_sprint['acc_20m_peak']: np.max(data["acc"][ten_value:end_value])
    outcomes_sprint['acc_peak'] = np.max(data["acc"])
    outcomes_sprint['pos_acc_peak'] = data["dist_x"][data["acc"].idxmax()]
    outcomes_sprint['n_pushes'] = n_pushes
    outcomes_sprint['dist_push1'] = data["dist_x"][push_ind[0]]
    outcomes_sprint['dist_push2'] = data["dist_x"][push_ind[1]]
    outcomes_sprint['dist_push3'] = data["dist_x"][push_ind[2]]
    outcomes_sprint['cycle_time'] = np.mean(cycle_time[0])

    outcomes_sprint = pd.DataFrame([outcomes_sprint])
    outcomes_sprint = round(outcomes_sprint, 2)
    return data, outcomes_sprint


def spider(data, sfreq: float = 400.):
    """
    Calculate spider outcomes measures.

    Parameters
    ----------
    data : dict or pd.Series
        processed sessiondata structure or pd.Series with frame data
    sfreq : float
        sampling frequency

    Returns
    -------
    data : pd.Series
        pd.Series with spider test data
    outcomes_spider : pd.Series
        pd.Series with most important outcome variables of the spider test

    """

    vel = "vel"
    if type(data) == dict:
        data = data["frame"]

    data[vel] = lowpass_butter(data[vel], sfreq=sfreq, cutoff=10)

    m = int(len(data[vel]) - (0.5 * sfreq))
    for st in range(1, m):
        if data[vel][st] > 0.1:
            if data[vel][int(st + (0.5 * sfreq))] > 1.0:
                start_value = st
                break
    data = data[start_value:].reset_index(drop=True)
    data["dist"] = cumtrapz(data[vel], initial=0.0) / sfreq

    data["dist_y"] = cumtrapz(np.gradient(data["dist"]) * np.sin(
        np.deg2rad(cumtrapz(data["rot_vel"] / sfreq, initial=0.0))), initial=0.0)
    data["dist_x"] = cumtrapz(np.gradient(data["dist"]) * np.cos(
        np.deg2rad(cumtrapz(data["rot_vel"] / sfreq, initial=0.0))), initial=0.0)

    end_point = int(pd.DataFrame(data["dist_x"]).idxmax())

    dist_x_zero = data["dist_x"][end_point:]
    find_end = dist_x_zero[dist_x_zero < 0]
    end_value = find_end.index[0]

    data = data[:end_value]
    data["time"] -= data['time'][0]
    data["rot_vel_left"] = data["rot_vel"][data["rot_vel"] > 30]
    data["rot_vel_right"] = data["rot_vel"][data["rot_vel"] < -30]
    data["dist_x"] = -data["dist_x"]

    outcomes_spider = dict()
    outcomes_spider['endtime'] = end_value / sfreq
    outcomes_spider['vel_mean'] = np.mean(data[vel])
    outcomes_spider['vel_peak'] = np.max(data[vel])
    outcomes_spider['acc_peak'] = np.max(data["acc"])
    outcomes_spider['rot_vel_mean_right'] = np.mean(data["rot_vel_right"])
    outcomes_spider['rot_vel_mean_left'] = np.mean(data["rot_vel_left"])
    outcomes_spider['rot_vel_peak_right'] = np.min(data["rot_vel_right"])
    outcomes_spider['rot_vel_peak_left'] = np.max(data["rot_vel_left"])
    outcomes_spider['rot_acc_peak'] = np.max(data["rot_acc"])

    outcomes_spider = pd.DataFrame([outcomes_spider])
    outcomes_spider = round(outcomes_spider, 2)
    return data, outcomes_spider

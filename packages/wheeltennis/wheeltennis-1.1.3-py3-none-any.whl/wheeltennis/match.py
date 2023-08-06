import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from scipy.integrate import cumtrapz


def vel_var(sessiondata):
    """
    Calculate velocity variables of a wheelchair tennis match

    Parameters
    ----------
    sessiondata : dict
        processed sessiondata structure

    Returns
    -------
    outcomes_vel : pd.Series
        pd.Series with all velocity variables

    """
    # Cut the dataset in forward and reverse velocity
    forward = sessiondata['frame'][(sessiondata['frame']['vel']) > 0.1].reset_index(drop=True)
    reverse = sessiondata['frame'][(sessiondata['frame']['vel']) < -0.1].reset_index(drop=True)

    mean_vel = np.mean(forward['vel'])
    peak_vel = np.max(forward['vel'])

    lsa = forward[forward['vel'] < 1]
    lsa_per = len(lsa) / len(forward) * 100
    msa = forward[(forward['vel'] > 1) & (forward['vel'] < 2)]
    msa_per = len(msa) / len(forward) * 100
    hsa = forward[forward['vel'] > 2]
    hsa_per = len(hsa) / len(forward) * 100

    n_hsa = (hsa['time'].diff() > 2).sum()
    n_hsa_pm = (n_hsa / ((len(forward) + len(reverse)) / 100)) * 60

    peaks, _ = find_peaks(forward['vel'], prominence=0.5, distance=50, width=50, height=2)
    vel_peaks = forward['vel'][peaks]
    vel_peaks = vel_peaks.sort_values(ascending=False)
    mean_vel_best5 = np.mean(vel_peaks.head(5))

    mean_rev_vel = -np.mean(reverse['vel'])
    peak_rev_vel = -np.min(reverse['vel'])

    outcomes_vel = pd.DataFrame([])
    outcomes_vel = outcomes_vel.append([{'vel_mean': mean_vel,
                                         'vel_peak': peak_vel,
                                         'rev_vel_mean': mean_rev_vel,
                                         'rev_vel_peak': peak_rev_vel,
                                         'per_low_speed_zone': lsa_per,
                                         'per_mid_speed_zone': msa_per,
                                         'per_high_speed_zone': hsa_per,
                                         'num_high_speed_activations_pm': n_hsa_pm,
                                         'mean_best_5_vel': mean_vel_best5}], ignore_index=True)
    return outcomes_vel


def acc_var(sessiondata):
    """
    Calculate acceleration variables of a wheelchair tennis match

    Parameters
    ----------
    sessiondata : dict
        processed sessiondata structure

    Returns
    -------
    outcomes_acc : pd.Series
        pd.Series with all acceleration variables

    """
    # Cut the dataset in forward, reverse velocity and positive accelerations
    forward = sessiondata['frame'][(sessiondata['frame']['vel']) > 0.1].reset_index(drop=True)
    forward_acc = forward[(forward['acc']) > 0.1].reset_index(drop=True)

    mean_acc = np.mean(forward_acc['acc'])

    laa = forward_acc[forward_acc['acc'] < 0.75]
    laa_per = len(laa) / len(forward_acc) * 100
    maa = forward_acc[(forward_acc['acc'] > 0.75) & (forward_acc['acc'] < 1.5)]
    maa_per = len(maa) / len(forward_acc) * 100
    haa = forward_acc[forward_acc['acc'] > 1.5]
    haa_per = len(haa) / len(forward_acc) * 100

    outcomes_acc = pd.DataFrame([])
    outcomes_acc = outcomes_acc.append([{'acc_mean': mean_acc,
                                         'per_low_acc_zone': laa_per,
                                         'per_mid_acc_zone': maa_per,
                                         'per_high_acc_zone': haa_per}], ignore_index=True)
    return outcomes_acc


def rot_vel_var(sessiondata, side: bool = True):
    """
    Calculate rotational velocity variables of a wheelchair tennis match

    Parameters
    ----------
    sessiondata : dict
        processed sessiondata structure
    side : bool
        if set to True left side is analysed
        if set to False right side is analysed

    Returns
    -------
    outcomes_rot_vel : pd.Series
        pd.Series with all rotational velocity variables

    """
    # Cut the dataset in part where there was movement
    move = sessiondata['frame'][(sessiondata['frame']['vel'] < -0.1) | (sessiondata['frame']['vel'] > 0.1)].reset_index(
        drop=True)

    if side is True:  # left
        rotate = move[move['rot_vel'] > 10].reset_index(drop=True)
        side = 'left'
    else:  # right
        rotate = move[move['rot_vel'] < -10].reset_index(drop=True)
        rotate['rot_vel'] = -rotate['rot_vel']
        side = 'right'

    turn1 = rotate[(rotate['vel'] > -0.5) & (rotate['vel'] < 0.5)].reset_index(drop=True)
    turn2 = rotate[(rotate['vel'] > -1.5) & (rotate['vel'] < 1.5)].reset_index(drop=True)
    curve1 = rotate[(rotate['vel'] > 1) & (rotate['vel'] < 2)].reset_index(drop=True)
    curve2 = rotate[rotate['vel'] > 1.5].reset_index(drop=True)

    moves = [rotate, turn1, turn2, curve1, curve2]
    moves_keys = ['all', 'turn1', 'turn2', 'curve1', 'curve2']
    outcomes_rot_vel = pd.DataFrame([])

    for movement, keys in zip(moves, moves_keys):
        if keys == 'all':
            peaks, _ = find_peaks(movement['rot_vel'], prominence=50, height=90, width=20, distance=50)
        else:
            peaks, _ = find_peaks(movement['rot_vel'], prominence=50, height=90, width=20, distance=50)
        rot_vel_peaks = movement['rot_vel'][peaks]
        rot_vel_peaks = rot_vel_peaks.sort_values(ascending=False)
        mean_rot_vel = np.mean(movement['rot_vel'])
        mean_rot_vel_best5 = np.mean(rot_vel_peaks.head(5))
        outcomes_rot_vel[keys + '_mean_rot_vel_' + side] = [mean_rot_vel]
        outcomes_rot_vel[keys + '_mean_best5_rot_vel_' + side] = [mean_rot_vel_best5]

    return outcomes_rot_vel


def rot_acc_var(sessiondata, side: bool = True):
    """
    Calculate rotational acceleration variables of a wheelchair tennis match

    Parameters
    ----------
    sessiondata : dict
        processed sessiondata structure
    side : bool
        if set to True left side is analysed
        if set to False right side is analysed

    Returns
    -------
    outcomes_rot_acc : pd.Series
        pd.Series with all rotational acceleration variables

    """
    # Cut the dataset in part where there was movement
    move = sessiondata['frame'][(sessiondata['frame']['vel'] < -0.1) | (sessiondata['frame']['vel'] > 0.1)].reset_index(
        drop=True)

    if side is True:  # left
        rotate = move[move['rot_vel'] > 10].reset_index(drop=True)
        rotate_acc = rotate[rotate['rot_acc'] > 10].reset_index(drop=True)
        side = 'left'
    else:  # right
        rotate = move[move['rot_vel'] < -10].reset_index(drop=True)
        rotate_acc = rotate[rotate['rot_acc'] > 10].reset_index(drop=True)
        side = 'right'

    turn1 = rotate_acc[(rotate_acc['vel'] > -0.5) & (rotate_acc['vel'] < 0.5)].reset_index(drop=True)
    turn2 = rotate_acc[(rotate_acc['vel'] > -1.5) & (rotate_acc['vel'] < 1.5)].reset_index(drop=True)
    curve1 = rotate_acc[(rotate_acc['vel'] > 1) & (rotate_acc['vel'] < 2)].reset_index(drop=True)
    curve2 = rotate_acc[rotate_acc['vel'] > 1.5].reset_index(drop=True)

    moves = [rotate_acc, turn1, turn2, curve1, curve2]
    moves_keys = ['all', 'turn1', 'turn2', 'curve1', 'curve2']
    outcomes_rot_acc = pd.DataFrame([])

    for movement, keys in zip(moves, moves_keys):
        mean_rot_acc = np.mean(movement['rot_acc'])
        outcomes_rot_acc[keys + '_mean_rot_acc_' + side] = [mean_rot_acc]

    return outcomes_rot_acc


def gen_var(sessiondata, side: bool = True, sfreq: float = 400.):
    """
    Calculate general variables of a wheelchair tennis match

    Parameters
    ----------
    sessiondata : dict
        processed sessiondata structure
    side: bool = True
        if set to True (right-handed)
        if set to False (left-handed)
    sfreq : float
        sampling frequency

    Returns
    -------
    outcomes_gen : pd.Series
        pd.Series with all general variables (time, distance, turns)

    """
    # Cut the dataset in forward and reverse velocity and the resting part
    forward = sessiondata['frame'][(sessiondata['frame']['vel']) > 0.1].reset_index(drop=True)
    reverse = sessiondata['frame'][(sessiondata['frame']['vel']) < -0.1].reset_index(drop=True)
    rest = sessiondata['frame'][(sessiondata['frame']['vel'] < 0.1) & (sessiondata['frame']['vel'] > -0.1)].reset_index(
        drop=True)

    work = len(forward['time']) + len(reverse['time'])
    rest = len(rest['time'])
    total = len(sessiondata['frame']['time'])

    ratio_forward = len(forward['time']) / work * 100
    ratio_reverse = len(reverse['time']) / work * 100
    for_rev = ratio_forward / ratio_reverse

    ratio_work = work / total * 100
    ratio_rest = rest / total * 100
    work_rest = ratio_work / ratio_rest

    if side is True:
        noracket_rotate = forward[forward['rot_vel'] > 160]
        racket_rotate = forward[forward['rot_vel'] < -160]
    else:
        noracket_rotate = forward[forward['rot_vel'] < -160]
        racket_rotate = forward[forward['rot_vel'] > 160]

    n_noracket_turns = (noracket_rotate['time'].diff() > 2).sum()
    n_noracket_turns_pm = (n_noracket_turns / ((len(forward) + len(reverse)) / 100)) * 60
    n_racket_turns = (racket_rotate['time'].diff() > 2).sum()
    n_racket_turns_pm = (n_racket_turns / ((len(forward) + len(reverse)) / 100)) * 60

    tot_duration_min = total / (sfreq * 60)
    tot_distance = max(sessiondata['frame']['dist'])

    distance_pm = tot_distance / tot_duration_min

    outcomes_gen = pd.DataFrame([])
    outcomes_gen = outcomes_gen.append([{'ratio_forward': ratio_forward,
                                         'ratio_reverse': ratio_reverse,
                                         'forward_reverse': for_rev,
                                         'n_noracket_turns_pm': n_noracket_turns_pm,
                                         'n_racket_turns_pm': n_racket_turns_pm,
                                         'ratio_work': ratio_work,
                                         'ratio_rest': ratio_rest,
                                         'work_rest': work_rest,
                                         'tot_duration_m': tot_duration_min,
                                         'tot_distance': tot_distance,
                                         'distance_pm': distance_pm}], ignore_index=True)
    return outcomes_gen


def speed_zones(sessiondata):
    speed_zone_outcomes = pd.DataFrame([])
    movement = sessiondata['frame'][
        (sessiondata['frame']['vel_filt'] > 0.1) | (sessiondata['frame']['vel_filt'] < -0.1)]
    zones = [-10, 0, 5, 7.5, 10, 12.5, 15]
    zones2 = [0, 5, 7.5, 10, 12.5, 15, 99]
    zones_ms = [x / 3.6 for x in zones]
    zones_ms2 = [x / 3.6 for x in zones2]

    for zone, zone2 in zip(zones_ms, zones_ms2):
        zone_ind = ((movement['vel_filt'] >= zone) & (movement['vel_filt'] < zone2))
        movement_zone = movement[zone_ind]
        if zone_ind is not None:
            per_speed_zone = (len(movement_zone) / len(movement) * 100)
            frame_dist = cumtrapz(movement_zone['vel_filt'], initial=0.0) / 52
            disp_speed_zone = (max(abs(frame_dist)))
            freq_speed_zone = ((movement_zone['time'].diff() > 0.5).sum())
        else:
            per_speed_zone = 0
            disp_speed_zone = 0
            freq_speed_zone = 0

        outcomes = pd.DataFrame([[per_speed_zone, disp_speed_zone, freq_speed_zone]],
                                columns=['per_speed_zone', 'disp_speed_zone', 'freq_speed_zone'],
                                index=[str(round(zone, 2)) + ' - ' + str(round(zone2, 2))])
        speed_zone_outcomes = pd.concat([speed_zone_outcomes, outcomes])

    return speed_zone_outcomes


def acc_zones(sessiondata):
    acc_zone_outcomes = pd.DataFrame([])
    movement = sessiondata['frame'][
        (sessiondata['frame']['vel_filt'] > 0.1) | (sessiondata['frame']['vel_filt'] < -0.1)]
    zones = [-99, 0, 1, 1.5, 2, 2.5, 5]
    zones2 = [0, 1, 1.5, 2, 2.5, 5, 99]

    for zone, zone2 in zip(zones, zones2):
        zone_ind = ((movement['acc'] >= zone) & (movement['acc'] < zone2))
        movement_zone = movement[zone_ind]
        if zone_ind is not None:
            per_acc_zone = (len(movement_zone) / len(movement) * 100)
            frame_dist = cumtrapz(movement_zone['vel_filt'], initial=0.0) / 52
            disp_acc_zone = (max(abs(frame_dist)))
            freq_acc_zone = ((movement_zone['time'].diff() > 0.1).sum())
        else:
            per_acc_zone = 0
            disp_acc_zone = 0
            freq_acc_zone = 0

        outcomes = pd.DataFrame([[per_acc_zone, disp_acc_zone, freq_acc_zone]],
                                columns=['per_acc_zone', 'disp_acc_zone', 'freq_acc_zone'],
                                index=[str(round(zone, 2)) + ' - ' + str(round(zone2, 2))])
        acc_zone_outcomes = pd.concat([acc_zone_outcomes, outcomes])

    return acc_zone_outcomes

# def turns(sessiondata):

#     movement = sessiondata['frame'][(sessiondata['frame']['vel_filt']>0.1) | (sessiondata['frame']['vel_filt']<-0.1)]
#     left_rotate = movement[movement['rot_vel_filt'] > 120]
#     right_rotate = movement[movement['rot_vel_filt'] < -120]


#     left_turns = (left_rotate['time'].diff() > 0.5).sum()
#     left_turns_pm = (left_turns / (len(movement) / 100)) * 60
#     right_turns = (right_rotate['time'].diff() > 0.5).sum()
#     right_turns_pm = (right_turns / (len(movement) / 100)) * 60

#     return left_turns, right_turns

# def key_var(sessiondata):
#     """
#     Calculate key variables of a wheelchair tennis match, based on study:
#     ...
#
#     Parameters
#     ----------
#     sessiondata : dict
#         processed sessiondata structure
#
#     Returns
#     -------
#     outcomes_key : pd.Series
#         pd.Series with all key variables
#
#     """
#     # Cut the dataset in forward and reverse velocity
#     forward = sessiondata['frame'][(sessiondata['frame']['vel']) > 0.1].reset_index(drop=True)
#     reverse = sessiondata['frame'][(sessiondata['frame']['vel']) < -0.1].reset_index(drop=True)
#
#     mean_vel = np.mean(forward['vel'])
#     peak_vel = np.max(forward['vel'])
#
#     lsa = forward[forward['vel'] < 1]
#     lsa_per = len(lsa) / len(forward) * 100
#     msa = forward[(forward['vel'] > 1) & (forward['vel'] < 2)]
#     msa_per = len(msa) / len(forward) * 100
#     hsa = forward[forward['vel'] > 2]
#     hsa_per = len(hsa) / len(forward) * 100
#
#     n_hsa = (hsa['time'].diff() > 2).sum()
#     n_hsa_pm = (n_hsa / ((len(forward) + len(reverse)) / 100)) * 60
#
#     peaks, _ = find_peaks(forward['vel'], height=2.5, width=100, distance=100)
#     vel_peaks = forward['vel'][peaks]
#     vel_peaks = vel_peaks.sort_values(ascending=False)
#     mean_vel_best5 = np.mean(vel_peaks.head(5))
#
#     mean_rev_vel = -np.mean(reverse['vel'])
#     peak_rev_vel = -np.min(reverse['vel'])
#
#     outcomes_vel = pd.DataFrame([])
#     outcomes_vel = outcomes_vel.append([{'rot_vel_curve': mean_vel,
#                                          'mean_best_5_vel': mean_vel_best5,
#                                          'rot_vel_turn': mean_rev_vel,
#                                          'num_high_speed_activations_pm': n_hsa_pm,
#
#                                          'rev_vel_peak': peak_rev_vel,
#                                          'per_low_speed_zone': lsa_per,
#                                          'per_mid_speed_zone': msa_per,
#                                          'per_high_speed_zone': hsa_per,
#                                          'num_high_speed_activations_pm': n_hsa_pm,
#                                          }], ignore_index=True)
#     return outcomes_vel

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 10:43:25 2022

@author: oscar
"""


def get_group(pid, groups):
    """
    This functions get the group of the corresponding id of the page.

    Parameters
    ----------
    pid:
        type: str
        page_id to conpute the group for.
    groups:
        type: dict
        Maps the group to the page ids.

    Returns
    -------
    str
    """

    group_out = 'no_group'
    try:
        for group in groups:
            if pid in groups[group]:
                group_out = group
    except Exception:
        pass

    return group_out


def get_name(pid, dict_page_id_to_name):
    try:
        out_name = dict_page_id_to_name[pid]
    except Exception:
        out_name = 'no_name'
    return out_name

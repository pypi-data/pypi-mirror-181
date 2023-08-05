"""
Analysis utility functions.
Copyright (C) 2022 Humankind Investments
"""

import pandas as pd
import numpy as np
from .db_utils import database_connect


# CLEANING DUPLICATE AND SPLIT VISITS +++++++++++++++++++++++++++++++++++++++++++++++++++++++
def drop_false_splits(df):
    """
    Drop false splits.
    
    Drop extraneous false splits, i.e. visits with duplicate visit counts per visitor
    occurring more than thirty minutes from each other. For each set of false splits, 
    the visit with the most activity is kept.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of false splits.
        
    Returns
    -------
    pd.DataFrame
        Dataframe of remaining splits after drops.
    """
    
    # keep visit among false splits with longest visit duration or most actions
    cdf = df.sort_values(by=['visit_duration', 'actions'],
                         ascending=[False, False]).drop_duplicates(
                             subset=['visitor_id', 'visit_count']).reset_index(drop=True)
    
    return cdf


def combine_true_splits(df, dt0=True):
    """
    Combine true splits.
    
    Combine and return true split visits, i.e. visits with duplicate visit counts 
    per visitor occurring within thirty minutes of one another.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of true splits.
    dt0 : bool
        Whether delta-dt between visits is 0, indicating split visits occur at same time.
        
    Returns
    -------
    pd.DataFrame
        Dataframe of combined splits.
    """
    
    # separate columns by how data to be aggregated
    mean_cols = [col for col in df.columns if col.split('_')[0] == 'avg']
    sum_cols = [col for col in df.columns if col.split('_')[-1] in [
        'actions', 'pages', 'downloads', 'outlinks', 'buyetfs', 'brokerlinks', 
        'plays', 'pauses', 'resumes', 'seeks', 'finishes', 
        'time', 'submissions', 'duration'] and col != 'time' and col not in mean_cols]
    first_cols = [col for col in df.columns if col not in
                  mean_cols + sum_cols and col.split('_')[0] not in [
                      'first', 'last', 'entry', 'exit'] and col.split('_')[-1] not in [
                          'flow', 'ts', 'list'] and not col.endswith('video_resolution')]
    manual_cols = [col for col in df.columns if col not in sum_cols + mean_cols + first_cols]

    # convert numeric columns to proper type
    df[mean_cols] = df[mean_cols].astype(float)
    
    # combine split visits with same visitor id and visit count
    # --> sort by visit id for split visits occurring at same time; split by datetime otherwise
    sort_col = 'visit_id' if dt0 else 'datetime'
    grp_cols = ['visitor_id', 'visit_count']
    # --> also group by datetime for split visits occurring at same time
    if dt0: grp_cols.append('datetime')
    grp = df.sort_values(by=sort_col).groupby(grp_cols)
    
    # apply basic aggregates for appropriate columns (first/last, sum, mean)
    first_grp = grp[[col for col in first_cols if col not in grp.keys]]
    # --> pull basic visit info from last visit info in half hour window if delta-t != 0
    first_df = first_grp.first() if dt0 else first_grp.last()
    sum_df = grp[[col for col in sum_cols if col not in grp.keys]].sum()
    mean_df = grp[[col for col in mean_cols if col not in grp.keys]].mean()
    cdf = pd.concat([first_df, sum_df, mean_df], axis=1)

    # combine remaining columns manually ...
    
    # select first and last non-empty action, and combine non-empty action flows in order
    actgrp = df[df['first_action'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    acts_df = pd.concat([actgrp['first_action'].first(), 
                         actgrp['last_action'].last(),
                         actgrp['action_flow'].apply(lambda x: ','.join(x)),
                         actgrp['action_ts'].apply(lambda x: ','.join(x)),
                         actgrp['action_site_flow'].apply(lambda x: ','.join(x)), 
                         actgrp['action_path_flow'].apply(lambda x: ','.join(x))], axis=1)
    
    # select first/last entry/exit pages, and fill in missing values based on first/last actions
    pgs_df = pd.concat([actgrp['entry_page'].first(), actgrp['exit_page'].last()], axis=1)
    pgs_df.loc[(pgs_df['entry_page'] == 'None') &
               (acts_df['first_action'].str.rsplit('_', 1).str[0].isin(
                   ['humankind_video', 'humankind-short_video', 'getstarted_form'])),
               'entry_page'] = 'humankind'
    pgs_df.loc[(pgs_df['entry_page'] == 'None') &
               ((acts_df['first_action'].str.rsplit('_', 1).str[0].isin(
                   ['wtf_video', 'wtf-short_video', 'buyetf'])) |
                (acts_df['first_action'].str.split('_', 1).str[-1].isin(
                    ['brokerlink_click', 'download']))), 'entry_page'] = 'humankindfunds'
    pgs_df.loc[(pgs_df['exit_page'] == 'None') &
               (acts_df['last_action'].str.rsplit('_', 1).str[0].isin(
                   ['humankind_video', 'humankind-short_video', 'getstarted_form'])),
               'exit_page'] = 'humankind'
    pgs_df.loc[(pgs_df['exit_page'] == 'None') &
               ((acts_df['last_action'].str.rsplit('_', 1).str[0].isin(
                   ['wtf_video', 'wtf-short_video', 'buyetf'])) |
                (acts_df['last_action'].str.split('_', 1).str[-1].isin(
                    ['brokerlink_click', 'download']))), 'exit_page'] = 'humankindfunds'

    # combine non-empty page flows
    pggrp = df[df['page_flow'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    pgs_df = pd.concat([
        pgs_df, pggrp['page_flow'].apply(lambda x: ','.join(x)), 
        pggrp['page_ts'].apply(lambda x: ','.join(x))], axis=1).fillna('None')
    
    # combine non-empty article post and ranked company page lists
    for pg in ['article-post', 'ranked-company']:
        pg += '_page_list'
        pgs_df = pd.concat([pgs_df, df[df[pg].fillna('None').replace(
            'NaN', 'None') != 'None'].sort_values(by=sort_col).groupby(
                grp_cols)[pg].apply(lambda x: ','.join(x))], axis=1).fillna('None')
        
    # combine non-empty download flows
    dlgrp = df[df['download_flow'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    dls_df = pd.concat([
        dlgrp['download_flow'].apply(lambda x: ','.join(x)), 
        dlgrp['download_ts'].apply(lambda x: ','.join(x))], axis=1).fillna('None')
    
    # combine non-empty outlink flows
    olgrp = df[df['outlink_flow'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    ols_df = pd.concat([
        olgrp['outlink_flow'].apply(lambda x: ','.join(x)), 
        olgrp['outlink_ts'].apply(lambda x: ','.join(x))], axis=1).fillna('None')

    # combine non-empty outlink lists
    for ol in ['social', 'crs', 'disclosures', 'articles']:
        ol += '_outlink_list'
        ols_df = pd.concat([ols_df, df[df[ol].fillna('None').replace(
            'NaN', 'None') != 'None'].sort_values(by=sort_col).groupby(
                grp_cols)[ol].apply(lambda x: ','.join(x))], axis=1).fillna('None')
           
    # combine non-empty buy-etf timestamps
    etfs_df = df[df['buyetf_ts'].fillna('None').replace(
        'NaN', 'None') != 'None'].sort_values(by=sort_col).groupby(
            grp_cols)['buyetf_ts'].apply(lambda x: ','.join(x))
    
    # combine non-empty broker link flows
    brkgrp = df[df['brokerlink_flow'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    brks_df = pd.concat([
        brkgrp['brokerlink_flow'].apply(lambda x: ','.join(x)), 
        brkgrp['brokerlink_ts'].apply(lambda x: ','.join(x))], axis=1).fillna('None')
    
    # combine non-empty video flows and non-empty video resolutions
    vidgrp = df[df['video_action_flow'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    vids_df = pd.concat([
        vidgrp['video_action_flow'].apply(lambda x: ','.join(x)), 
        vidgrp['video_action_ts'].apply(lambda x: ','.join(x)),
        df[df['video_resolution'] != 'None'].sort_values(by=sort_col).groupby(
            grp_cols)['video_resolution'].apply(lambda x: ','.join(x))], axis=1).fillna('None')

    # combine non-empty form flows
    frmgrp = df[df['form_action_flow'] != 'None'].sort_values(by=sort_col).groupby(grp_cols)
    frms_df = pd.concat([
        frmgrp['form_action_flow'].apply(lambda x: ','.join(x)), 
        frmgrp['form_action_ts'].apply(lambda x: ','.join(x))], axis=1).fillna('None')
    
    # combine all split visit columns
    cdf = pd.concat([cdf, acts_df, pgs_df, dls_df, ols_df, etfs_df,
                     brks_df, vids_df, frms_df], axis=1).fillna('None')
    
    # reset missing values in appropriate columns
    cdt = cdf.index.get_level_values(2) if dt0 else cdf['datetime']
    for pg in [col[:-1] for col in df.isnull().sum()[df.isnull().sum() > 0].index
               if col.endswith('_pages')]:
        cdf.loc[cdt <= df[df[pg + 's'].isnull()].sort_values(
            by='datetime', ascending=False)['datetime'].iloc[0],
                [col for col in cdf.columns if pg in col]] = np.nan
    for dl in [col[:-1] for col in df.isnull().sum()[df.isnull().sum() > 0].index
               if col.endswith('_downloads')]:
        cdf.loc[cdt <= df[df[dl + 's'].isnull()].sort_values(
            by='datetime', ascending=False)['datetime'].iloc[0],
                [col for col in cdf.columns if col == dl + 's'
                 or col == dl + '_duration']] = np.nan
    for ol in [col[:-1] for col in df.isnull().sum()[df.isnull().sum() > 0].index
               if col.endswith('_outlinks')]:
        cdf.loc[cdt <= df[df[ol + 's'].isnull()].sort_values(
            by='datetime', ascending=False)['datetime'].iloc[0],
                [col for col in cdf.columns if ol in col]] = np.nan
    if any(df['buyetfs'].isnull()):
        cdf.loc[cdt <= df[df['buyetfs'].isnull()].sort_values(
            by='datetime', ascending=False)['datetime'].iloc[0],
                [col for col in cdf.columns if 'buyetf' in col]] = np.nan
    for vid in [col.rsplit('_', 1)[0] for col in df.isnull().sum()[df.isnull().sum() > 0].index
                if col.endswith('_video_plays')]:
        cdf.loc[cdt <= df[df[vid + '_plays'].isnull()].sort_values(
            by='datetime', ascending=False)['datetime'].iloc[0],
                [col for col in cdf.columns if vid in col]] = np.nan
    for frm in [col.rsplit('_', 1)[0] for col in df.isnull().sum()[df.isnull().sum() > 0].index
                if col.endswith('_form_actions')]:
        cdf.loc[cdt <= df[df[frm + '_actions'].isnull()].sort_values(
            by='datetime', ascending=False)['datetime'].iloc[0],
                [col for col in cdf.columns if frm in col]] = np.nan
    
    return cdf
    
    
def clean_split_visits(df, true_split=True, same_time=True):
    """
    Clean split visits, combining true splits and dropping false splits.
    
    Combine true split visits, i.e. visits with duplicate visit counts per visitor 
    occurring within thirty minutes of one another, and drop extraneous false splits,
    i.e. visits with duplicate visit counts per visitor occurring more than thirty 
    minutes from each other.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of split visits.
    true_split : bool
        Whether split visits are true splits or false splits.
    same_time : bool
        Whether true splits occur at same time or different times.
        
    Returns
    -------
    pd.DataFrame
        Cleaned dataframe of split visits.
    """

    # calculate differences in time between split visits
    grp = df.sort_values(by='datetime').groupby(['visitor_id', 'visit_count'])
    # --> deltadt = time between each split visit for given visitor ID and visit count
    deltadt = grp['datetime'].apply(list).apply(
        lambda x: [(x[i+1] - x[i]).total_seconds() for i in range(len(x)-1)]).rename('deltadt')
    # --> visit_id_pairs = split visit pairs for which delta-dt calculated
    visit_id_pairs = grp['visit_id'].unique().apply(
        lambda x: [(x[i], x[i+1]) for i in range(len(x)-1)] if len(x) > 1 else
        [(x[0], x[0])]).rename('visit_id_pairs')
    split_dt = pd.concat([deltadt, visit_id_pairs], axis=1)
    
    # filter out split visits already cleaned (no duplicates)
    split_mask = split_dt['deltadt'].str.len() > 0
    split_dt = pd.concat([split_dt[split_mask]['deltadt'].explode(),
                          split_dt[split_mask]['visit_id_pairs'].explode()], axis=1)
    
    # sum up total delta-dt for true splits occurring at different times or false splits
    if not true_split or not same_time:
        split_dt = pd.concat([
            split_dt.reset_index().groupby(['visitor_id', 'visit_count'])['deltadt'].sum(),
            split_dt['visit_id_pairs'].apply(
                lambda x: list(x)).explode().drop_duplicates().reset_index().groupby([
                    'visitor_id', 'visit_count'])['visit_id_pairs'].unique()], axis=1)
    # set delta-dt thresholds for selecting split visits of given type
    if true_split:
        deltadt_mask = split_dt['deltadt'] == 0 if same_time else split_dt['deltadt'] < 1800
    else:
        deltadt_mask = split_dt['deltadt'] >= 1800
    # isolate split visits of given type
    split_ids = split_dt[deltadt_mask]['visit_id_pairs'].apply(
        lambda x: list(x)).explode().drop_duplicates()
    split_visits = df[df['visit_id'].isin(split_ids)].reset_index(drop=True)
    
    # combine true splits or drop false splits
    if true_split: clean_splits = combine_true_splits(split_visits, same_time).reset_index()
    else: clean_splits = drop_false_splits(split_visits)

    # drop split visits of given type, and add newly cleaned split visits
    df = df.drop(df.loc[df['visit_id'].isin(split_visits['visit_id'])].index)
    df = pd.concat([df, clean_splits]).sort_values(by='visit_id').reset_index(drop=True)
    
    return df


def get_split_visits(df):
    """
    Get split visits from visit-level data.
    
    Identify and return all split visits from visit-level data set, where split visits
    are those with duplicate visit counts per visitor.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of visits.
    
    Returns
    -------
    pd.DataFrame
        Dataframe of split visits.
    """

    # count number of visit IDs associated with each visitor ID - visit count pair
    visit_count = df.groupby(['visitor_id', 'visit_count'])['visit_id'].count()
    
    # isolate visitor ID - visit count pairs with multiple visit IDs
    dupl_visit_count = visit_count[visit_count > 1]
    
    # pull out split visits from visit-level data set
    split_visits = df.loc[df[['visitor_id', 'visit_count']].apply(
        tuple, axis=1).isin(dupl_visit_count.index)].reset_index(drop=True)
    
    return split_visits


def clean_duplicate_visits(df):
    """
    Clean duplicate visits from visit-level data.
    
    The real-time visits logged in the visit-level data set are sometimes prone to 
    tracking errors by Matomo that result in duplicate visits. Such duplicate visits 
    can take the form of true duplicates, where multiple rows contain identical entries 
    but for the visit IDs attached to them. Alternatively, duplicate visits can appear 
    in the form of split visits, where a single visit is split into multiple entries with 
    different visit IDs and visit metrics for the same visit count and visitor ID. 
    When such split visits occur within a small window of time, i.e. within thirty minutes 
    of one another, such split visits represent true splits that should be recombined into 
    the original visits from which they were split. On the other hand, when split visits 
    are spread across large amounts of time, i.e. hours or days, they represent false splits, 
    or truly unique visits that Matomo erroneously attributed the same visit count to, which 
    are cleaned by dropping all but those with the longest visit durations or most activity.
    
    Parameters
    ----------
    df : pd.DataFrame
        Dataframe of visits.
    
    Returns
    -------
    pd.DataFrame
        Dataframe of visits with cleaned duplicates.
    """

    # DROP DUPLICATE VISITS +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # duplicate visits = entries with identical metrics except for visit IDs
    df = df.drop_duplicates(subset=[col for col in df.columns if
                                    col != 'visit_id']).reset_index(drop=True)

    
    # IDENTIFY SPLIT VISITS +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # split visits = visits with duplicate visit counts per visitor
    
    # isolate split visits to be combined or cleaned
    split_df = get_split_visits(df)

    # keep track of initial split visit IDs (for dropping later)
    split_visit_ids = split_df['visit_id']

    # drop split visits with no actions (no use in combining these if nothing to combine)
    split_df = split_df.drop(split_df[split_df['actions'] == 0].index).reset_index(drop=True)

    # add datetime column
    split_df['datetime'] = pd.to_datetime(split_df['date'].astype(str) + ' ' + split_df['time'])
    
    # COMBINE SAME-TIME TRUE SPLITS +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # same-time true splits = split visits occurring at exact same time
    split_df = clean_split_visits(split_df, true_split=True, same_time=True)
    
    # COMBINE DIFFERENT-TIME TRUE SPLITS ++++++++++++++++++++++++++++++++++++++++++++++++++++
    # different-time true splits = split visits occurring within 30 minutes of one another
    split_df = clean_split_visits(split_df, true_split=True, same_time=False)
    
    # CLEAN FALSE SPLITS ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # false splits = split visits occurring more than 30 minutes from each other
    split_df = clean_split_visits(split_df, true_split=False)
    
    # DROP SPLIT VISITS AND REPLACE WITH CLEANED SPLITS +++++++++++++++++++++++++++++++++++++
    df = df.drop(df[df['visit_id'].isin(split_visit_ids)].index)
    df = pd.concat([df, split_df.drop(columns='datetime')],
                   ignore_index=True).sort_values(by='visit_id').reset_index(drop=True)
    
    return df

def drop_hki(df):
    """
    Drop visits from Humankind and yellow systems employees

    Parameters
    ----------
    df : pd.DataFrame
        visit-level data.

    Returns
    -------
    df : pd.DataFrame
        visit-level data.

    """
    #drop visits by humankind employees
    hkimask = (((df['ip'] == '71.172.0.0') & (df['city'] == 'Jersey City')) |  
               ((df['ip'] == '108.21.0.0') & (df['city'] == 'Brooklyn')) | ((df['ip'] == '75.67.0.0') & (df['city'] == 'Amesbury')) | 
               ((df['ip'] == '67.253.0.0') & (df['city'] == 'Raymond')) | ((df['ip'] == '216.15.0.0') & (df['city'] == 'Allentown')) |  
               ((df['ip'] == '98.2.0.0') & (df['city'] == 'Portland')) |  
               ((df['ip'] == '173.68.0.0') & (df['city'] == 'New York')) |  
               ((df['ip'] == '47.20.0.0') & (df['city'] == 'Ossining')) |  
               ((df['ip'] == '207.237.0.0') & (df['city'] == 'New York')) |
               ((df['ip'] == '24.146.0.0') & (df['city'] == 'The Bronx')) |  
               ((df['ip'] == '68.129.0.0') & (df['city'] == 'Pleasantville')))
    # remove non-campaign referral entries from humankind users
    df= df.drop(df[(df['referrer_type'] != 'campaign') & hkimask].index)
    # drop visits from yellowsystem
    ysmask = df['country'].isin(['Armenia', 'Belarus', 'Georgia'])
    df= df.loc[~ysmask]
    return df

def drop_dev(df, db_dict):
    """
    Find all visitors that have ever been to the dev sites and exclude them

    Parameters
    ----------
    df : pd.DataFrame
        Visit data.
    db_dict : dict
        Dictionary of credentials for all databases. For example:
        db_dict = {'hkisocial' : cred.hkisocial,
                    'hkiweb' : cred.hkiweb,
                    'hkimarket' : cred.hkimarket,
                    'hkiads' : cred.hkiads,
                    }

    Returns
    -------
    df : pd.DataFrame
        The input df is changed inplace.

    """
    
    query= """
    select distinct visitor_id
     from action_log
     where 
     	shorturl like '%/dev.%'
     	or shorturl like '%/develop.%'
     	or shorturl like '%devrankings%'
     	or shorturl like '%amplifyapp%'
    """
    _, conn = database_connect('hkiweb', db_dict)
    dev= pd.read_sql(query, conn)
    conn.close()
    df= df.loc[~df['visitor_id'].isin(dev['visitor_id'])]
    return df

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
from wordcloud import WordCloud
import re
import networkx as nx
import os.path

pd.options.display.max_colwidth = 9999
pd.options.display.float_format = '${:,.2f}'.format

##### Read data ########
@st.cache(persist = True, suppress_st_warning=True)
def load_verified_data():
    #use_cols = ['[INV] Invoice ID', '[INV] Invoice Line Number',
    #    '[INV] Description', '[INV] PO Description',
    #    '[INV]Commodity (enriched) (Ariba Classification Taxonomy (L1))',
    #   '[INV]Commodity (enriched) (Ariba Classification Taxonomy (L2))',
    #   '[INV]Commodity (enriched) (Ariba Classification Taxonomy (L3))',
    #   '[INV]Commodity (enriched) (Ariba Classification Taxonomy (L4))',
    #   '[INV]Commodity (enriched) (Ariba Classification Taxonomy (L5))',
    #   ]
    #df_data = pd.read_csv('./Data/ItemClassification.csv', sep= ',', encoding = 'utf8', usecols=use_cols)
    #df_data.rename(columns={ '[INV]Commodity (enriched) (Ariba Classification Taxonomy (L1))':'L1',
    #   '[INV]Commodity (enriched) (Ariba Classification Taxonomy (L2))':'L2',
    #   '[INV]Commodity (enriched) (Ariba Classification Taxonomy (L3))':'L3',
    #   '[INV]Commodity (enriched) (Ariba Classification Taxonomy (L4))':'L4',
    #   '[INV]Commodity (enriched) (Ariba Classification Taxonomy (L5))':'L5',}, inplace=True)
#
    #df_verified = pd.read_csv('./Data/VerifiedResult.csv', sep= ',', encoding = 'utf8')
#
    #df_data_with_verification = pd.merge(df_data, df_verified, how = 'left', left_on = ['[INV] Invoice ID', '[INV] Invoice Line Number'],
    #    right_on = ['[INV] Invoice ID', '[INV] Invoice Line Number'])
    #
    #df_data_with_verification['L1_ver'].fillna("Not Yet", inplace = True)
    #df_data_with_verification['L2_ver'].fillna("Not Yet", inplace = True)
    #df_data_with_verification['L3_ver'].fillna("Not Yet", inplace = True)
    #df_data_with_verification['L4_ver'].fillna("Not Yet", inplace = True)
    #df_data_with_verification['L5_ver'].fillna("Not Yet", inplace = True)
    #
    #df_summary = df_data_with_verification.groupby(by = ['L1','L2', 'L3','L4','L5','L1_ver','L2_ver','L3_ver','L4_ver','L5_ver']).agg({'[INV] Invoice ID':'count'}).reset_index()
    df_summary = pd.read_csv('./Data/Summary_result.csv', sep= ',', encoding = 'utf8')
    return df_summary

def count_result(df_, l):
    col = l + '_ver'
    return df_[df_[col] != 'Not Yet']['[INV] Invoice ID'].sum(), df_[df_[col] == 'Not Yet']['[INV] Invoice ID'].sum(),df_[df_[col] == 'correct']['[INV] Invoice ID'].sum(), df_[df_[col] == 'incorrect']['[INV] Invoice ID'].sum(),df_[df_[col] == 'need more info.']['[INV] Invoice ID'].sum()



st.title("Summarization of Ariba Enrichment")
df_summary = load_verified_data()
#st.write(df_summary)

ls_L1 = list(set(df_summary['L1']))
ls_L1.sort()
col_l1, col_l2,col_l3, col_l4,col_l5 = st.beta_columns(5)
sel_L1 = col_l1.multiselect("L1", ls_L1)
df_filter_by_classes = df_summary[df_summary['L1'].isin(sel_L1)]
st.write(df_filter_by_classes)
num_verified_1, num_not_yet_1, num_cor_1, num_incor_1, num_need_info_1 = count_result(df_filter_by_classes, 'L1')
st.write("L1:  No. of records:", df_filter_by_classes['[INV] Invoice ID'].sum())
st.write(" - No. of verified records:", num_verified_1)
st.write(" - No. of not determined records:", num_not_yet_1)
st.write(" - No. of correct records:", num_cor_1)
st.write(" - No. of incorrect records:", num_incor_1)
st.write(" - No. of records with need more info.:", num_need_info_1)



ls_L2_from_L1 = list(set(df_summary[df_summary['L1'].isin(sel_L1)]['L2']))
ls_L2_from_L1.sort()
sel_L2 = col_l2.multiselect("L2", ls_L2_from_L1)
if(len(sel_L2) > 0):
    df_filter_by_classes = df_filter_by_classes[df_filter_by_classes['L2'].isin(sel_L2)]
    num_verified_2, num_not_yet_2, num_cor_2, num_incor_2, num_need_info_2 = count_result(df_filter_by_classes, 'L2')
    st.write("L2:  No. of records:", df_filter_by_classes['[INV] Invoice ID'].sum())
    st.write(" - No. of verified records:", num_verified_2)
    st.write(" - No. of not determined records:", num_not_yet_2)
    st.write(" - No. of correct records:", num_cor_2)
    st.write(" - No. of incorrect records:", num_incor_2)
    st.write(" - No. of records with need more info.:", num_need_info_2)    


ls_L3_from_L2 = list(set(df_summary[df_summary['L2'].isin(sel_L2)]['L3']))
ls_L3_from_L2.sort()
sel_L3 = col_l3.multiselect("L3", ls_L3_from_L2)
if(len(sel_L3) > 0):
    df_filter_by_classes = df_filter_by_classes[df_filter_by_classes['L3'].isin(sel_L3)]
    num_verified_3, num_not_yet_3, num_cor_3, num_incor_3, num_need_info_3 = count_result(df_filter_by_classes, 'L3')
    st.write("L3:  No. of records:", df_filter_by_classes['[INV] Invoice ID'].sum())
    st.write(" - No. of verified records:", num_verified_3)
    st.write(" - No. of not determined records:", num_not_yet_3)
    st.write(" - No. of correct records:", num_cor_3)
    st.write(" - No. of incorrect records:", num_incor_3)
    st.write(" - No. of records with need more info.:", num_need_info_3) 


ls_L4_from_L3 = list(set(df_summary[df_summary['L3'].isin(sel_L3)]['L4']))
ls_L4_from_L3.sort()
sel_L4 = col_l4.multiselect("L4", ls_L4_from_L3)
if(len(sel_L4) > 0):
    df_filter_by_classes = df_filter_by_classes[df_filter_by_classes['L4'].isin(sel_L4)]
    num_verified_4, num_not_yet_4, num_cor_4, num_incor_4, num_need_info_4 = count_result(df_filter_by_classes, 'L4')
    st.write("L4:  No. of records:", df_filter_by_classes['[INV] Invoice ID'].sum())
    st.write(" - No. of verified records:", num_verified_4)
    st.write(" - No. of not determined records:", num_not_yet_4)
    st.write(" - No. of correct records:", num_cor_4)
    st.write(" - No. of incorrect records:", num_incor_4)
    st.write(" - No. of records with need more info.:", num_need_info_4)

ls_L5_from_L4 = list(set(df_summary[df_summary['L4'].isin(sel_L4)]['L5']))
ls_L5_from_L4.sort()
sel_L5 = col_l5.multiselect("L5", ls_L5_from_L4)
if(len(sel_L5) > 0):
    df_filter_by_classes = df_filter_by_classes[df_filter_by_classes['L5'].isin(sel_L5)]
    num_verified_5, num_not_yet_5, num_cor_5, num_incor_5, num_need_info_5 = count_result(df_filter_by_classes, 'L5')
    st.write("L5:  No. of records:", df_filter_by_classes['[INV] Invoice ID'].sum())
    st.write(" - No. of verified records:", num_verified_5)
    st.write(" - No. of not determined records:", num_not_yet_5)
    st.write(" - No. of correct records:", num_cor_5)
    st.write(" - No. of incorrect records:", num_incor_5)
    st.write(" - No. of records with need more info.:", num_need_info_5)

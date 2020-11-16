import streamlit as st
import graphviz as graphviz
import pandas as pd

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

finite = graphviz.Digraph("finite_state_machine", filename="fsm.gv")
finite.attr(rankdir="LR", size="8,5")





####

df_summary = load_verified_data()
#st.write(data)

ls_L1 = list(set(df_summary['L1']))
ls_L1.sort()
sel_L1 = st.multiselect("L1", ls_L1)
df_filter_by_classes = df_summary[df_summary['L1'].isin(sel_L1)]


#st.write(sel_L1[0].split( )[0])

ls_L2_from_L1 = list(set(df_summary[df_summary['L1'].isin(sel_L1)]['L2']))
ls_L2_from_L1.sort()

finite.attr("node", shape="doublecircle")
finite.attr("node", shape="circle")
root_name = sel_L1[0].split( )[0]
finite.node(root_name)

for l2_name in ls_L2_from_L1:
 #   st.write(l2_name.split( )[0])
    finite.edge(root_name, l2_name.split( )[0], label="l2_name_XXX")



st.graphviz_chart(finite)
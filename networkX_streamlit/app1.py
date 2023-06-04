import streamlit as st
import networkx as nx
import pandas as pd
import pyvis as pv
from pyvis.network import Network
import itertools
import os

st.set_page_config(page_title="network graph",layout="wide")
print(os.getcwd())


###reading the data file
@st.cache()
def get_data():
    df = pd.read_csv("file.csv")
    return df


df = get_data()

dtc_codes = set(df['dtc_Codes'].values)
# nodes = set(df['Node'].values)
# subnodes_1 = set(df['subnode1'].values)
# subnodes_2 = set(df['subnode2'].values)

options = st.sidebar.selectbox(label="DTC_Codes",options=dtc_codes)


# HtmlFile = open("nx.html", 'r', encoding='utf-8')
# source_code = HtmlFile.read() 
# st.components.v1.html(source_code, height = 900,width=900)

def get_graph():
    G = nx.DiGraph(directed=True)
    df_selected = df[df['dtc_Codes'].isin([options])]
    dtc_codes_to_nodes = list(
    map(lambda x:(x[1],x[2],x[3]),df_selected.loc[:,['dtc_Codes','Node','Node Occurence']].itertuples()))
    # dtc_codes_to_nodes = itertools.product([options],set(df_selected['Node'].values))
    nodes_to_subnodes1 = list(
    map(
        lambda x:(x[1],x[2]),list(df_selected.loc[:,['Node','subnode1']].itertuples())
    )
)
    subnode1_to_subnode2 = list(
    filter(
        lambda x:x[1]!='0',list(
    map(
        lambda x:(x[1],x[2]),list(df_selected.loc[:,['subnode1','subnode2']].itertuples())
    )
)
    )
)
    G.add_weighted_edges_from(dtc_codes_to_nodes)
    G.add_edges_from(nodes_to_subnodes1)
    G.add_edges_from(subnode1_to_subnode2)
    return G

def get_network():
    nt = Network( height='500px',width='100%',
                 bgcolor='#222222',
                font_color='white',directed=True)

    # Take Networkx graph and translate it to a PyVis graph format
    nt.from_nx(get_graph())

    # Generate network with specific layout settings
    nt.repulsion(       node_distance=420,
                        central_gravity=0.33,
                        spring_length=110,
                        spring_strength=0.10,
                        damping=0.95)
    return nt


try:
    path = './tmp'
    get_network().save_graph(f'{path}/nx.html')
    HtmlFile = open(f'{path}/nx.html', 'r', encoding='utf-8')

# Save and read graph as HTML file (locally)
except:
    path = './html_files'
    get_network().save_graph(f'{path}/nx.html')
    HtmlFile = open(f'{path}/nx.html', 'r', encoding='utf-8')


st.components.v1.html(HtmlFile.read(), height=1200)

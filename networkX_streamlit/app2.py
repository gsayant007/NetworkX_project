import streamlit as st
import networkx as nx
import pandas as pd
import pyvis as pv
from pyvis.network import Network
import itertools


st.set_page_config(page_title="network graph",layout="wide")


###reading the data file
@st.cache()
def get_data():
    df = pd.read_csv("file.csv")
    return df

df = get_data()

dtc_codes = set(df['dtc_Codes'].values)

options = st.sidebar.selectbox(label="DTC_Codes",options=dtc_codes)


def get_network():
    df_selected = df[df['dtc_Codes'].isin([options])]
    g = Network(height='500px',width='100%',directed=True)

    for x in list(
        map(
            lambda x:(x[1],x[2],x[3]),df_selected.loc[:,['dtc_Codes','Node','Node Occurence']].itertuples()
        )
    ):
        g.add_node(x[0])
        g.add_node(x[1])
        g.add_edge(x[0], x[1], title=str(x[2]),value = x[2])

    for x in list(
        map(
            lambda x:(x[1],x[2],x[3]),df_selected.loc[:,['Node','subnode1','Subnode1_occurence']].itertuples()
        )
    ):
        g.add_node(x[0])
        g.add_node(x[1])
        g.add_edge(x[0], x[1], title=str(x[2]),value = x[2])

    for x in list(
        map(
            lambda x:(x[1],x[2],x[3]),df_selected.loc[:,['subnode1','subnode2','subnode2 occurence']].itertuples()
        )
    ):
        g.add_node(x[0])
        g.add_node(x[1])
        g.add_edge(x[0], x[1], title=str(x[2]),value = x[2])



    g.repulsion(node_distance=420,
                central_gravity=0.33,
                spring_length=110,
                spring_strength=0.10,
                damping=0.95)



      # Generate network with specific layout settings
    g.repulsion(       node_distance=420,
                          central_gravity=0.33,
                          spring_length=110,
                          spring_strength=0.10,
                          damping=0.95)
    g.show("./html_files/nx2.html")
    return g


try:
    path = './tmp'
    get_network().save_graph(f'{path}/nx.html')
    HtmlFile = open(f'{path}/nx2.html', 'r', encoding='utf-8')

# Save and read graph as HTML file (locally)
except:
    path = './html_files'
    get_network().save_graph(f'{path}/nx.html')
    HtmlFile = open(f'{path}/nx2.html', 'r', encoding='utf-8')


st.components.v1.html(HtmlFile.read(), height=1200)
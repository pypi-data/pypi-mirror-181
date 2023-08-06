import pickle
import os
import biomart
import matplotlib.pyplot as plt
import networkx as nx

from PyWGCNA.comparison import *

# bcolors
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


# read WGCNA obj
def readWGCNA(file):
    """
    Read a WGCNA from a saved pickle file.

    :param file: Name / path of WGCNA object
    :type file: str

    :return: PyWGCNA object
    :rtype: PyWGCNA class
    """
    if not os.path.isfile(file):
        raise ValueError('WGCNA object not found at given path!')

    picklefile = open(file, 'rb')
    wgcna = pickle.load(picklefile)

    print(f"{BOLD}{OKBLUE}Reading {wgcna.name} WGCNA done!{ENDC}")
    return wgcna


# compare serveral networks
def comparenetworks(PyWGCNAs):
    """
    Compare serveral PyWGCNA objects
                
    :param PyWGCNAs: list of PyWGCNA objects
    :type PyWGCNAs: list of PyWGCNA class

    :return: compare object
    :rtype: Compare class
    """
    geneModules = {}
    for PyWGCNA in PyWGCNAs:
        geneModules[PyWGCNA.name] = PyWGCNA.datExpr.var
    compare = Comparison(geneModules=geneModules)
    compare.compareNetworks()

    return compare


# compare WGCNA to single cell
def compareSingleCell(PyWGCNAs, sc):
    """
    Compare WGCNA and gene marker from single cell experiment

    :param PyWGCNAs: WGCNA object
    :type PyWGCNAs: PyWGCNA class
    :param sc: gene marker table which has ....
    :type sc: pandas dataframe

    :return: compare object
    :rtype: Compare class

    """
    geneModules = {}
    for PyWGCNA in PyWGCNAs:
        geneModules[PyWGCNA.name] = PyWGCNA.datExpr.var
    compare = Comparison(geneModules=geneModules,
                         geneMarker=sc,
                         sc=True)
    compare.compareNetworks()

    return compare


def getGeneList(dataset='mmusculus_gene_ensembl',
                attributes=['ensembl_gene_id', 'external_gene_name', 'gene_biotype'],
                maps=['gene_id', 'gene_name', 'go_id']):
    """
    get table that map gene ensembl id to gene name from biomart

    :param dataset: name of the dataset we used from biomart; mouse: mmusculus_gene_ensembl and human: hsapiens_gene_ensembl
        you can find more information here: https://bioconductor.riken.jp/packages/3.4/bioc/vignettes/biomaRt/inst/doc/biomaRt.html#selecting-a-biomart-database-and-dataset
    :type dataset: string
    :param attributes: List the types of data we want
    :type attributes: list
    :param maps: mapping between attributes and column names of gene information you want to show
    :type maps: list
    
    :return: table extracted from biomart related to the datasets including information from attributes
    :rtype: pandas dataframe
    """

    server = biomart.BiomartServer('http://uswest.ensembl.org/biomart')
    mart = server.datasets[dataset]

    # Get the mapping between the attributes
    response = mart.search({'attributes': attributes})
    data = response.raw.data.decode('ascii')

    geneInfo = pd.DataFrame(columns=attributes)
    # Store the data in a dict
    for line in data.splitlines():
        line = line.split('\t')
        dict = {}
        for i in range(len(attributes)):
            dict[attributes[i]] = line[i]
        geneInfo = geneInfo.append(dict, ignore_index=True)

    geneInfo.index = geneInfo[attributes[0]]
    geneInfo.drop(attributes[0], axis=1, inplace=True)

    if maps is not None:
        geneInfo.columns = maps[1:]

    return geneInfo


def getGeneListGOid(dataset='mmusculus_gene_ensembl',
                    attributes=['ensembl_gene_id', 'external_gene_name', 'go_id'],
                    Goid='GO:0003700'):
    """
    get table that find gene id and gene name to specific Go term from biomart

    :param dataset: name of the dataset we used from biomart; mouse: mmusculus_gene_ensembl and human: hsapiens_gene_ensembl
        you can find more information here: https://bioconductor.riken.jp/packages/3.4/bioc/vignettes/biomaRt/inst/doc/biomaRt.html#selecting-a-biomart-database-and-dataset
    :type dataset: string
    :param attributes: List the types of data we want
    :type attributes: list
    :param Goid: GO term id you would like to get genes from them
    :type Goid: list or str

    :return: table extracted from biomart related to the datasets including information from attributes with filtering
    :rtype: pandas dataframe
    """

    server = biomart.BiomartServer('http://uswest.ensembl.org/biomart')
    mart = server.datasets[dataset]

    # mart.show_attributes()
    # mart.show_filters()

    response = mart.search({
        'filters': {
            'go': [Goid]
        },
        'attributes': attributes
    })
    data = response.raw.data.decode('ascii')

    geneInfo = pd.DataFrame(columns=attributes)
    # Store the data in a dict
    for line in data.splitlines():
        line = line.split('\t')
        dict = {}
        for i in range(len(attributes)):
            dict[attributes[i]] = line[i]
        geneInfo = geneInfo.append(dict, ignore_index=True)

    return geneInfo


# read comparison obj
def readComparison(file):
    """
    Read a comparison from a saved pickle file.

    :param file: Name / path of comparison object
    :type file: string

    :return: comparison object
    :rtype: comparison class
    """
    if not os.path.isfile(file):
        raise ValueError('Comparison object not found at given path!')

    picklefile = open(file, 'rb')
    comparison = pickle.load(picklefile)

    print(f"{BOLD}{OKBLUE}Reading comparison done!{ENDC}")
    return comparison


def jaccard(list1, list2):
    """
    Calculate jaccard similarity matrix for two lists

    :param list1: first list containing the data
    :type list1: list
    :param list2: second list containing the data
    :type list2: list

    :return: jaccard similarity
    :rtype: double
    """
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


def plot_jaccard_similarity(jaccard_similarity,
                            color=None,
                            cutoff=0.1,
                            save=True,
                            plot_show=True,
                            plot_format="png",
                            file_name="jaccard_similarity"):
    """
    Plot jaccard similarity matrix as a network

    :param jaccard_similarity: dataframe containing jaccard similarity between all modules in all PyWGCNA objects
    :type jaccard_similarity: pandas dataframe
    :param color: if you want to color nodes for each networks separately
    :type color: dict
    :param cutoff: threshold you used for filtering jaccard similarity
    :type cutoff: double
    :param save: indicate if you want to save the plot or not (default: True)
    :type save: bool
    :param plot_show: indicate if you want to show the plot or not (default: True)
    :type plot_show: bool
    :param plot_format: indicate the format of plot (default: png)
    :type plot_format: str
    :param file_name: name and path of the plot use for save (default: jaccard_similarity)
    :type file_name: str
    """
    df = pd.DataFrame(jaccard_similarity.stack())
    df.reset_index(inplace=True)
    df = df[df[0] >= cutoff]
    df.columns = ['source', 'dest', 'weight']

    G = nx.from_pandas_edgelist(df, 'source', 'dest', 'weight')
    node_labels = {}
    nodes = list(G.nodes())
    for i in range(len(nodes)):
        node_labels[nodes[i]] = nodes[i].split(":")[1]
    edges = G.edges()
    weights = [G[u][v]['weight'] * 10 for u, v in edges]
    edge_labels = {}
    for u, v in edges:
        edge_labels[u, v] = str(G[u][v]['weight'])

    color_map = []
    if color is None:
        color_map = None
    else:
        for node in G:
            color_map.append(color[node.split(":")[0]])

    fig, ax = plt.subplots(figsize=(len(G.nodes()) / 2.5, len(G.nodes()) / 2.5))
    nx.draw_networkx(G,
                     node_color=color_map,
                     width=weights,
                     labels=node_labels,
                     font_size=15,
                     font_weight="bold",
                     node_size=1500,
                     with_labels=True,
                     ax=ax)

    if color is not None:
        for label in color:
            ax.plot([0], [0], color=color[label], label=label)

    plt.legend()
    plt.tight_layout()
    if plot_show:
        plt.show()
    else:
        plt.close()
    if save:
        plt.savefig(f"{file_name}.{plot_format}")

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.cluster import KMeans


def clustering(datos, combo, tabControl2, clus):
    array = datos.values
    x = array[:, 0:1]
    y = array[:, 1:2]
    if (combo == "2"):
        kmeans = KMeans(n_clusters=2)
        kmeans.fit(array)
    else:
        kmeans = KMeans(n_clusters=3)
        kmeans.fit(array)
    clustering.centroides = kmeans.cluster_centers_
    graphClusters(x, y, kmeans, tabControl2, clus)
    return kmeans.cluster_centers_

## Graficar Clusters
def graphClusters(x, y, kmeans, tabControl2, clus):
    tabControl2.tab(0, state='disabled')
    tabControl2.tab(1, state='normal')
    tabControl2.select(1)
    fig = plt.figure(figsize=(6.5, 4))
    ax = fig.gca()
    plt.scatter(x.reshape(x.shape[0]), y.reshape(y.shape[0]), s=11, c=kmeans.labels_, cmap="rainbow")
    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=100, alpha=0.5);
    canvas = FigureCanvasTkAgg(fig, master=clus)
    plt_widget = canvas.get_tk_widget()
    plt_widget.place(x=75, y=45)

## Node

Any time that you start an instance of Elasticsearch, you are starting a node. A collection of connected nodes is called a **cluster**. If you are running a single node of Elasticsearch, then you have a cluster of one node.

Every node in the cluster can handle **HTTP** and **Transport** traffic by default. The transport layer is used exclusively for communication between nodes and the **Java TransportClient**; the HTTP layer is used only by external REST clients.

All nodes know about all the other nodes in the cluster and can forward client requests to the appropriate node. Besides that, each node serves one or more purpose:  所有节点都知道集群中的所有其他节点，并且可以将客户端请求转发到适当的节点。 除此之外，每个节点都有一个或多个目的：

##### Master-eligible node

A node that has node.master set to true (default), which makes it eligible to be elected as the master node, which controls the cluster.  node.master设置为true（默认）的节点，使其有资格被选为控制集群的主节点。

##### Data node

A node that has node.data set to true (default). Data nodes hold data and perform data related operations such as CRUD, search, and aggregations.  node.data设置为true的节点（默认值）。 数据节点保存数据并执行与数据相关的操作，例如CRUD，搜索和聚合。

##### Ingest node

A node that has node.ingest set to true (default). Ingest nodes are able to apply an ingest pipeline to a document in order to transform and enrich the document before indexing. With a heavy ingest load, it makes sense to use dedicated ingest nodes and to mark the master and data nodes as node.ingest: false.  node.ingest设置为true的节点（默认值）。 摄取节点能够将摄取管道应用于文档，以便在编制索引之前转换和丰富文档。 使用大量的摄取负载，使用专用的摄取节点并将主节点和数据节点标记为node.ingest：false是有意义的。

##### Tribe node

A tribe node, configured via the tribe.* settings, is a special type of coordinating only node that can connect to multiple clusters and perform search and other operations across all connected clusters.  通过 tribe.* settings 配置的 tribe 节点是一种特殊类型的仅协调节点，可以连接到多个集群并在所有连接的集群中执行搜索和其他操作。

By default a node is a master-eligible node and a data node, plus it can pre-process documents through ingest pipelines. This is very convenient for small clusters but, as the cluster grows, it becomes important to consider separating dedicated master-eligible nodes from dedicated data nodes.  默认情况下，节点是符合主节点的节点和数据节点，此外它还可以通过摄取管道预处理文档。 这对于小型集群非常方便，但随着集群的增长，考虑将专用的符合主节点的节点与专用数据节点分开变得很重要。

Note：Coordinating node  协调节点

Requests like search requests or bulk-indexing requests may involve data held on different data nodes. A search request, for example, is executed in two phases which are coordinated by the node which receives the client request — the coordinating node.  诸如搜索请求或批量索引请求之类的请求可能涉及保存在不同数据节点上的数据。 例如，搜索请求在两个阶段中执行，这两个阶段由接收客户端请求的节点 - 协调节点协调。

In the scatter phase, the coordinating node forwards the request to the data nodes which hold the data. Each data node executes the request locally and returns its results to the coordinating node. In the gather phase, the coordinating node reduces each data node’s results into a single global resultset.  在分散阶段，协调节点将请求转发到保存数据的数据节点。 每个数据节点在本地执行请求并将其结果返回给协调节点。 在收集阶段，协调节点将每个数据节点的结果减少为单个全局结果集。

Every node is implicitly a coordinating node. This means that a node that has all three node.master, node.data and node.ingest set to false will only act as a coordinating node, which cannot be disabled. As a result, such a node needs to have enough memory and CPU in order to deal with the gather phase.  每个节点都隐式地是一个协调节点。 这意味着将所有三个node.master，node.data和node.ingest设置为false的节点仅用作协调节点，无法禁用该节点。 结果，这样的节点需要具有足够的存储器和CPU以便处理收集阶段。

### Master Eligible Node

The master node is responsible for lightweight cluster-wide actions such as creating or deleting an index, tracking which nodes are part of the cluster, and deciding which shards to allocate to which nodes. It is important for cluster health to have a stable master node.  主节点负责轻量级群集范围的操作，例如创建或删除索引，跟踪哪些节点是群集的一部分，以及决定将哪些分片分配给哪些节点。 集群运行状况对于拥有稳定的主节点非常重要。

Any master-eligible node (all nodes by default) may be elected to become the master node by the master election process.  可以通过主选举过程选择任何符合主节点的节点（默认情况下所有节点）成为主节点。

Master nodes must have access to the data/ directory (just like data nodes) as this is where the cluster state is persisted between node restarts.  主节点必须能够访问数据/目录（就像数据节点一样），因为这是在节点重新启动之间保持集群状态的地方。

Indexing and searching your data is CPU-, memory-, and I/O-intensive work which can put pressure on a node’s resources. To ensure that your master node is stable and not under pressure, it is a good idea in a bigger cluster to split the roles between dedicated master-eligible nodes and dedicated data nodes.  索引和搜索数据是CPU，内存和I / O密集型工作，可能会对节点资源造成压力。 为确保主节点稳定且不受压力，在较大的群集中最好分割专用主节点和专用数据节点之间的角色。

While master nodes can also behave as coordinating nodes and route search and indexing requests from clients to data nodes, it is better not to use dedicated master nodes for this purpose. It is important for the stability of the cluster that master-eligible nodes do as little work as possible.  虽然主节点也可以表现为协调节点并将搜索和索引请求从客户端路由到数据节点，但最好不要将专用主节点用于此目的。 对于集群的稳定性而言，符合主节点的节点尽可能少地工作是很重要的。

To create a dedicated master-eligible node, set:  要创建专用的符合主节点的节点，请设置：

```
node.master: true 
node.data: false 
node.ingest: false 
search.remote.connect: false ## Disable cross-cluster search (enabled by default).
```

### Avoiding split brain with minimum_master_nodes

To prevent data loss, it is vital to configure the `discovery.zen.minimum_master_nodes` setting (which defaults to 1) so that each master-eligible node knows the minimum number of master-eligible nodes that must be visible in order to form a cluster.  为了防止数据丢失，配置discovery.zen.minimum_master_nodes设置（默认为1）至关重要，这样每个符合主节点的节点都知道为了形成集群必须可见的最大主节点数。

To explain, imagine that you have a cluster consisting of two master-eligible nodes. A network failure breaks communication between these two nodes. Each node sees one master-eligible node… itself. With `minimum_master_nodes` set to the default of 1, this is sufficient to form a cluster. Each node elects itself as the new master (thinking that the other master-eligible node has died) and the result is two clusters, or a split brain. These two nodes will never rejoin until one node is restarted. Any data that has been written to the restarted node will be lost.  为了解释，假设您有一个由两个符合主节点的节点组成的集群。 网络故障会破坏这两个节点之间的通信。 每个节点都会看到一个符合主节点的节点......本身。 将“minimum_master_nodes”设置为默认值1，这足以形成一个集群。 每个节点选择自己作为新的主节点（认为其他符合主节点的节点已经死亡），结果是两个集群，或者是一个分裂的大脑。 在重新启动一个节点之前，这两个节点永远不会重新加入。 已写入重新启动的节点的任何数据都将丢失。

Now imagine that you have a cluster with three master-eligible nodes, and `minimum_master_nodes` set to 2. If a network split separates one node from the other two nodes, the side with one node cannot see enough master-eligible nodes and will realise that it cannot elect itself as master. The side with two nodes will elect a new master (if needed) and continue functioning correctly. As soon as the network split is resolved, the single node will rejoin the cluster and start serving requests again.

This setting should be set to a quorum of master-eligible nodes:

```
(master_eligible_nodes / 2) + 1
```

In other words, if there are three master-eligible nodes, then minimum master nodes should be set to (3 / 2) + 1 or 2:

```
discovery.zen.minimum_master_nodes: 2
```

To be able to remain available when one of the master-eligible nodes fails, clusters should have at least three master-eligible nodes, with `minimum_master_nodes` set accordingly. A rolling upgrade, performed without any downtime, also requires at least three master-eligible nodes to avoid the possibility of data loss if a network split occurs while the upgrade is in progress.  为了能够在其中一个符合主节点的节点发生故障时保持可用，群集应至少具有三个符合主节点的节点，并相应地设置minimum_master_nodes。 在没有任何停机的情况下执行的滚动升级还需要至少三个符合主节点的节点，以避免在升级过程中发生网络拆分时数据丢失的可能性。

This setting can also be changed dynamically on a live cluster with the cluster update settings API:

```
PUT _cluster/settings
{
  "transient": {
    "discovery.zen.minimum_master_nodes": 2
  }
}
```

An advantage of splitting the master and data roles between dedicated nodes is that you can have just three master-eligible nodes and set minimum_master_nodes to 2. You never have to change this setting, no matter how many dedicated data nodes you add to the cluster.  在专用节点之间拆分主角色和数据角色的一个优点是，您只能拥有三个符合主节点的节点，并将minimum_master_nodes设置为2.无论您添加到群集的专用数据节点有多少，都无需更改此设置。


### Data Node

Data nodes hold the shards that contain the documents you have indexed. Data nodes handle data related operations like CRUD, search, and aggregations. These operations are I/O-, memory-, and CPU-intensive. It is important to monitor these resources and to add more data nodes if they are overloaded.  数据节点包含包含已编制索引的文档的分片。 数据节点处理与数据相关的操作，如CRUD，搜索和聚合。 这些操作是I / O-，内存和CPU密集型的。 监视这些资源并在超载时添加更多数据节点非常重要。

The main benefit of having dedicated data nodes is the separation of the master and data roles.

To create a dedicated data node, set:

```
node.master: false 
node.data: true 
node.ingest: false 
search.remote.connect: false  # Disable cross-cluster search (enabled by default).
```

### Ingest Node

Ingest nodes can execute pre-processing pipelines, composed of one or more ingest processors. Depending on the type of operations performed by the ingest processors and the required resources, it may make sense to have dedicated ingest nodes, that will only perform this specific task.  摄取节点可以执行由一个或多个摄取处理器组成的预处理流水线。 根据摄取处理器执行的操作类型和所需资源，具有专用摄取节点可能是有意义的，这些节点仅执行此特定任务。

To create a dedicated ingest node, set:

```
node.master: false 
node.data: false 
node.ingest: true 
search.remote.connect: false  # Disable cross-cluster search (enabled by default).
```

### Coordinating only node

If you take away the ability to be able to handle master duties, to hold data, and pre-process documents, then you are left with a coordinating node that can only route requests, handle the search reduce phase, and distribute bulk indexing. Essentially, coordinating only nodes behave as smart load balancers.  如果您剥夺了处理主要职责，保存数据和预处理文档的能力，那么您将留下一个协调节点，该节点只能路由请求，处理搜索减少阶段和分发批量索引。 实质上，仅协调节点就像智能负载平衡器一样。

Coordinating only nodes can benefit large clusters by offloading the coordinating node role from data and master-eligible nodes. They join the cluster and receive the full cluster state, like every other node, and they use the cluster state to route requests directly to the appropriate place(s).  通过从数据和符合主节点的节点卸载协调节点角色，仅协调节点可以使大型群集受益。 它们加入群集并像其他每个节点一样接收完整的群集状态，并使用群集状态将请求直接路由到适当的位置。

Adding too many coordinating only nodes to a cluster can increase the burden on the entire cluster because the elected master node must await acknowledgement of cluster state updates from every node! The benefit of coordinating only nodes should not be overstated — data nodes can happily serve the same purpose.  将过多的仅协调节点添加到群集会增加整个群集的负担，因为所选主节点必须等待来自每个节点的群集状态更新的确认！ 不应过分夸大仅协调节点的好处 - 数据节点可以愉快地用于相同的目的。

To create a dedicated coordinating node, set:

```
node.master: false 
node.data: false 
node.ingest: false 
search.remote.connect: false 
```

### Node data path settings

##### path.data

Every data and master-eligible node requires access to a data directory where shards and index and cluster metadata will be stored. The `path.data` defaults to `$ES_HOME/data` but can be configured in the `elasticsearch.yml` config file an absolute path or a path relative to `$ES_HOME` as follows:

```
path.data:  /var/elasticsearch/data
```

Like all node settings, it can also be specified on the command line as:

```
./bin/elasticsearch -Epath.data=/var/elasticsearch/data
```

When using the .zip or .tar.gz distributions, the path.data setting should be configured to locate the data directory outside the Elasticsearch home directory, so that the home directory can be deleted without deleting your data! The RPM and Debian distributions do this for you already.   使用.zip或.tar.gz发行版时，应配置path.data设置以在Elasticsearch主目录之外找到数据目录，以便可以删除主目录而不删除数据！ RPM和Debian发行版已经为您完成了这项工作。

#####  node.max_local_storage_nodes

The `data path` can be shared by multiple nodes, even by nodes from different clusters. This is very useful for testing failover and different configurations on your development machine. In production, however, it is recommended to run only one node of Elasticsearch per server.  数据路径可以由多个节点共享，甚至可以由来自不同集群的节点共享。 这对于测试开发计算机上的故障转移和不同配置非常有用。 但是，在生产中，建议每台服务器只运行一个Elasticsearch节点。

By default, Elasticsearch is configured to prevent more than one node from sharing the same data path. To allow for more than one node (e.g., on your development machine), use the setting `node.max_local_storage_nodes` and set this to a positive integer larger than one.  默认情况下，Elasticsearch配置为阻止多个节点共享同一数据路径。 要允许多个节点（例如，在开发计算机上），请使用设置node.max_local_storage_nodes并将其设置为大于1的正整数。

Never run different node types (i.e. master, data) from the same data directory. This can lead to unexpected data loss.


### 问题

* 主节点的选举过程？？
* 数据节点如何分片？？
* cluster.name
* node.name
* network settings
* X-Pack node settings
* [Curator](https://www.elastic.co/guide/en/elasticsearch/client/curator/current/index.html)



**Write Request Flow**

1. A Client API process starts on the requesting node.
2. Client API sends the request and metadata information (file size, file name) to the Master (NameNode - JP1). 
   Actual data is not transferred to the Master.
3. Master generates detailed metadata: calculates the number of blocks, defines replication 
   (e.g., three copies per block), and allocates placement locations using the Rack Awareness Policy.
4. Master stores this metadata in its local EXT file system (not HDFS).
5. Master sends the metadata (block locations) back to the Client API.
6. Client API creates a Pipeline process.
7. The Pipeline splits the data, creates replicas, and streams the blocks sequentially to the designated slave nodes.
8. Slave nodes acknowledge receipt, and the Client API informs the Master that the write is successful.

**Read Request Flow**

1. Client API sends the read request to the Master (NameNode).
2. Master responds with the metadata, including the locations of all block replicas.
3. Client API directly reads only one copy of the block from one DataNode (no pipeline is used for read).
   If the selected copy is unavailable, it skips that node and reads from another replica.


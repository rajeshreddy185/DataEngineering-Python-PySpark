### Hadoop Distributed File System (HDFS)

HDFS is the primary storage system used by Hadoop applications, designed to store very large files across multiple 
machines in a distributed manner. It's optimized for high-throughput access to large datasets and is 
highly fault-tolerant.

Core Distributed File System Concepts:

File System: A layer acting between the software and hardware, used to read and write data to/from the hard disk
Examples: Windows uses NTFS (New Technology File System); Linux uses EXT (Extensible File System)
Types of File Systems:
    ◦ Standalone File Systems (SDFS): Like NTFS and EXT.
    ◦ Distributed File Systems (DFS): Like HDFS and S3 (object store).

Block Concept: All file systems use blocks to split large files into small partitions for easier read/write operations
SDFS Block Sizes: Windows NTFS uses 16 KB; Linux EXT uses 512 KB
Node and Cluster: A single machine (physical or virtual machine) is a node; a group of nodes is a cluster

HDFS Distinguishing Features: Block Distribution and Replication

Default block size was 64 MB (till Hadoop Version 1)
Default block size is 128 MB (after Hadoop Version 1)
Block size is highly configurable, but must be a multiple of two (e.g., 32 MB, 64 MB, 128 MB, etc.)

Data Distribution (The Core Difference):
Data engineers only define a cluster as "distributed" if the data itself is distributed
In SDFS, a 1 GB file is stored entirely on one machine
In HDFS, a 1 GB file is divided into blocks, and these blocks are stored across different machines/nodes 
in the cluster

Replication (Fault Tolerance):
Replication means creating copies for data blocks. This mechanism is introduced by Hadoop itself.
Default replication strategy is three replicas (one actual block + two copies)


#### Architecture Deep Dive
Master-Slave: One master communicates with all slaves; slaves do not communicate with each other

- **NameNode (Master)**
  - Manages file system namespace
  - Maintains metadata (edits log, fsimage)
  - Tracks file-to-block mapping and block locations
  - Handles client read/write requests
  - Single point of failure (mitigated by HA setup)

- **DataNodes (Workers)**
  - Store and retrieve data blocks
  - Perform block creation, deletion, and replication
  - Send heartbeats to NameNode

#### Data Storage Mechanics
- Block size: 128MB (default)
- Replication factor: 3 (default)
- Rack awareness for fault tolerance
- Write-once-read-many model

Disadvantage of Master-Slave: Single Point of Failure (SPOF), as the master is a Single Point of Communication (SPOC)

Node Roles:
   Master Node: Runs NameNode (and Job Tracker/Resource Manager). Requires high RAM configuration compared to other nodes
   Slave Node: Runs DataNode (and Task Tracker/Node Manager)
  Edge Node: A separate node used by developers to trigger jobs (read/write requests). This is the best practice; 
            we should not connect directly to the Master or Slave nodes. The Edge Node does not store HDFS data.

Data Write and Read Architecture (Hadoop 1): 
  HDFS is installed on top of a Standalone File System (e.g., EXT on Linux) on each node
  Use specific hadoop commands to ensure data is uploaded to HDFS for distribution, not the local EXT file system

## The Hadoop Ecosystem

Apache Hadoop is an open-source framework designed for distributed storage and processing of large datasets across 
clusters of commodity hardware. It provides a reliable, scalable platform for big data processing.
Big Data is the problem; Hadoop is a solution.
It originated from Google's GFS (Google File System) and MapReduce papers.
The core components of Hadoop are HDFS (Hadoop Distributed File System) for data storage and MapReduce for parallel 
data processing.

The broader "Hadoop framework" or "ecosystem" includes many other tools developed by various groups, such as:
Hive: Allows SQL queries for processing data in Hadoop. (Created by Facebook)
Pig: Uses Pig Latin scripting for data transformations. (Created by Yahoo)
Sqoop: For importing data from relational databases (RDBMS) to Hadoop and exporting data from Hadoop to RDBMS.
Oozie: A scheduler for automating Hadoop jobs. (Created by Yahoo)
HBase: A NoSQL database that works on top of HDFS. (Created by Facebook)
Mahout: For machine learning and data science tasks.
Flume: For collecting real-time streaming data into Hadoop.

Hadoop frameworks are "loosely coupled," meaning you can remove or add components without the entire system failing.
Hadoop can integrate with other big data technologies (like Spark) and also with non-big data technologies (like traditional RDBMS).
Components within the Hadoop ecosystem serve different purposes, including data storage, processing, data pipelines, 
scheduling, and data science.


<img width="900" alt="static1" src="https://github.com/rajeshreddy185/polls/blob/main/mysite3-20210509T044718Z-001/mysite3/Hadoop_Ecosystem_Architecture.webp">
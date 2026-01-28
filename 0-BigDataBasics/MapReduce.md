**MapReduce**

MapReduce is a software framework used for processing vast amounts of data in parallel across a Hadoop cluster.
It works by breaking down a large task into smaller sub-tasks, distributing them, and then consolidating the results.

Processing Phases

A. Map Phase

Input: Data is read from HDFS as (Key, Value) pairs.
Action: The user-defined Map() function processes these pairs and produces intermediate (Key, Value) pairs.
Goal: Filtering and sorting data (e.g., extracting "City" and "Temperature" from a huge log file).

B. Shuffle & Sort Phase

Action: The framework automatically groups all intermediate values associated with the same intermediate key.
Goal: To ensure the Reducer receives all data related to a specific key at once.

C. Reduce Phase

Input: (Key, List of Values) from the Shuffle phase.
Action: The user-defined Reduce() function aggregates, sums, or simplifies the list of values into a smaller set of values.
Goal: Final aggregation (e.g., finding the "Maximum Temperature" for each city).


MapReduce was created to solve three specific problems: Scale, Cost, and Failure

In traditional systems, you bring data to the computer to process it. With Big Data, the data is too heavy to move.

The MapReduce Way: It sends the code (the "Map" and "Reduce" functions) to the specific servers where the data blocks 
already live. This is called Data Locality, and it saves massive amounts of network bandwidth.

In a cluster of 1,000 "commodity" (cheap) servers, it is a  certain that one will crash every day.

The Solution: If a server fails while running a "Map" task, the master node simply notices the heartbeat stopped and 
assigns that specific task to another server that has a replica of that data. The job doesn't fail; it just reroutes.

Absolute Simplicity, MapReduce hides all the "distributed" complexity. The framework handles the grouping, the data 
transfer between servers, and the hardware failures automatically.

Cost Effective: 
Because MapReduce is designed to handle failure gracefully, you don't need expensive, high-end "enterprise" servers. 
You can build a supercomputer out of thousands of cheap, "commodity" PCs.


Where :

Massive "Cold" Batch Processing: If you have a job that takes 20 hours and processes 10 PB of data where speed isn't the
priority, MapReduce is extremely stable and uses very little RAM.

One-pass ETL: Simple data cleaning where you don't need to look at the data twice.


Advantages

Scalability: Can process petabytes of data by adding more commodity hardware.
Fault Tolerance: If a node fails during a Map task, the Master detects it and re-schedules that task on another node.
Data Locality: Tasks are scheduled on the nodes where the data blocks actually reside, minimizing network traffic.

Limitations (Why Spark is often preferred)

Disk Intensive: MapReduce writes intermediate data to HDFS at every stage, causing a Disk I/O Bottleneck.
Slow for Iterative Jobs: In Machine Learning, where data is read repeatedly, MapReduce is inefficient because it cannot 
                         cache data in memory.
High Latency: Not suitable for real-time or interactive processing.



1. MapReduce 1 (Hadoop 1.x Architecture)

JobTracker: This is the master daemon responsible for cluster monitoring, resource allocation, task scheduling, and 
execution management. It communicates with the NameNode to identify where data blocks are located.
TaskTracker: These are the slave daemons that reside on each data node. They receive tasks from the JobTracker, 
launch a Map or Reduce JVM to process the data, and send heartbeats back to the JobTracker every 
three seconds to report status.

Key Operational Goals
• Data Locality: A primary aim of MapReduce is to achieve data locality, meaning the processing task identifies 
which node contains the required data block and executes the logic on that specific machine to minimize network traffic.
• Fault Tolerance: If a node or task fails, the JobTracker monitors this through heartbeats and can restart only the 
failed subtask on a different node rather than restarting the entire job.
• Parallelism: The number of Map tasks is typically decided by the number of data blocks (e.g., 1GB of data divided 
into 64MB blocks results in 16 mappers), while the number of Reduce tasks is decided by the developer

TaskTracker (Worker): Ran on each node, executed tasks (Map or Reduce), and sent "heartbeats" back to the JobTracker.

The Main Problem: The JobTracker became a massive bottleneck. Once the cluster reached about 4,000 nodes, 
the JobTracker would get overwhelmed trying to manage both the hardware resources and the thousands of individual tasks.




2. MapReduce 2

While Version 1 relied on a JobTracker and TaskTracker, Version 2 decoupled resource management from the processing engine,
allowing Hadoop to support multiple frameworks beyond just MapReduce

In MapReduce 2, the system is managed by two primary daemons that replaced the older "V1" components:

Resource Manager (Master): This daemon acts as the central authority for the entire cluster. 
Unlike the V1 JobTracker, it does not manage individual tasks; instead, it focuses on cluster-level resource allocation
and scheduling

Node Manager (Slave): These reside on each data node, overseeing the resources (like RAM and CPU) of that specific 
machine and launching tasks as directed

Application Master (AM)
A critical innovation in MapReduce 2 is the Application Master. When a user submits a job (such as a JAR file), the 
Resource Manager launches an Application Master in one of the slave nodes.

Job-Specific Management: The AM acts as an "assistant manager" solely for that specific job. It is responsible for
negotiating resources with the Resource Manager, tracking the status of its mappers and reducers, and handling heartbeats

Input Splits: While blocks are physical units of data in HDFS, splits are logical units used by the framework. 
By default, one block equals one split, which equals one mapper. However, a developer can adjust the 
`mapred.max.split.size` to increase or decrease the number of mappers independently of the physical block count.

Speculative Execution: If a specific task is "stuck" or running unusually slowly due to hardware or infrastructure issues 
(not code bugs), the system triggers speculative execution. It launches a duplicate task on a different node.
Whichever task finishes first is accepted as the result, and the other is killed.

Multi-Framework Support: Because YARN serves as a generic cluster manager, the same infrastructure can simultaneously run 
MapReduce, Spark, Storm, or Flink jobs.


Submission: The Client sends the job to the ResourceManager.

Allocation: The ResourceManager picks a node and launches a Container to run the ApplicationMaster.
Negotiation: The ApplicationMaster looks at the HDFS data splits and asks the ResourceManager for "worker" containers.
Execution: The ApplicationMaster tells NodeManagers to start the Map and Reduce tasks inside those containers.
Cleanup: Once the job is done, the ApplicationMaster shuts down and releases all containers back to the pool.

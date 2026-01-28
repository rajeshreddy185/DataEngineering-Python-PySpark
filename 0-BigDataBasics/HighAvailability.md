**Failure Handling and High Availability (HA)**
• Heartbeat: Slave nodes communicate with the Master every three seconds (a heartbeat) to confirm they are alive

Slave Node (DataNode) Failure:
  ◦ Master detects the failure (no heartbeat).
  ◦ If a block copy is lost, the system remains operational due to other replicas.
  ◦ Hadoop automatically initiates automatic failover by copying the missing block from a healthy replica to a new node 
    that doesn't currently hold that block copy.
  ◦ Master updates the metadata location details.
  ◦ Recommendation: Whether failure is temporary or permanent, treat it as permanent, remove the node, and add a new one 
    immediately to ensure automatic failover happens reliably.

Master Node (NameNode) Failure (Hadoop 1):
    ◦ Hadoop Version 1 did not support High Availability (HA).
    ◦ If the NameNode failed, all read/write/job requests were killed.
    ◦ If the NameNode's hard disk crashed permanently, the entire metadata store (which is local to the NameNode's EXT)
      was lost, making all data blocks on the slaves unusable.

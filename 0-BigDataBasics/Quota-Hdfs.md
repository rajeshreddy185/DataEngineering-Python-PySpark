In HDFS, Quotas are administrative limits set on specific directories to manage cluster resources and prevent a single 
user or application from consuming all available storage.


HDFS supports two types of quotas: Name Quotas and Space Quotas.

**1. Name Quotas**

This limits the number of files and directories that can be created in a directory tree.
How it works: If you set a name quota of N, the directory can contain a total of N-1 items (including the directory itself).
Why use it: The NameNode stores metadata in RAM. Every file/directory takes up about 150 bytes of NameNode memory.
High name quotas protect the NameNode from running out of RAM due to millions of small files.

**2. Space Quotas**
This limits the total number of bytes used by files in a directory tree.
How it works: It counts the raw disk space used. Crucially, this includes replication.
The Math: If you have a 1GB file and a replication factor of 3, it consumes 3GB of your space quota.
Why use it: To manage physical disk capacity across different teams or projects.

# 1. Set a Name Quota (Limit to 1000 items)
```hdfs dfsadmin -setQuota 1000 /user/marketing/data```

# 2. Set a Space Quota (Limit to 500 Gigabytes)
# Supports suffixes: k, m, g, t, p
```hdfs dfsadmin -setSpaceQuota 500g /user/marketing/data```

# 3. View Quota Information
# Output columns: NameQuota, NameRemaining, SpaceQuota, SpaceRemaining, Path
```hdfs dfs -count -q -h /user/marketing/data```

# 4. Clear Quotas
```
hdfs dfsadmin -clrQuota /user/marketing/data
hdfs dfsadmin -clrSpaceQuota /user/marketing/data
```

NOTE: 

Hard Limits: If a quota is exceeded, the write operation (like put or mkdir) will fail immediately with an 
```NSQuotaExceededException or DSQuotaExceededException```.

Rename behavior: You can rename a file within a directory even if the quota is full, as long as the destination 
directory has enough quota for the "new" name/space.

New Directories: When you create a new directory, it inherits no quotas (unlimited) by default unless specifically set.

Snapshots: If snapshots are enabled, deleted files still count against the space quota until the snapshot is deleted.
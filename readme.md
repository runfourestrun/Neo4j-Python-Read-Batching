### An example of read batching using the neo4j python driver 🐍🐍

> it was found that read batching actually makes the runtime slower as compared to running without batching. 



### basic implementation pattern is as follows

* create an n-array where the max of the array is the max label count, and each element is a skip Interval. 
* example, if your (p:Person)  label has 50,000 nodes, that is the max element in the skip interval array/sequence
* [10000,20000,30000,40000,50000]
* Worth mentioning but this solution works best for properties that are indexed, as the array is already sorted (I believe..)
```angular2html
f'MATCH (u:User) RETURN u ORDER BY u.id SKIP {skip_interval} LIMIT 10000'
```




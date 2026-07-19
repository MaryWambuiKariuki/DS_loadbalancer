# DS_loadbalancer
# Task 4
Experiment A-1

Objective - To evaluate how the load balancer distributes 10,000 asynchronous client requests among three backend server replicas using consistent hashing.

Result:

Server-1	5243

Server-2	2100

Server-3	2657

Observation:
The requests were distributed across all three server replicas. Although the load distribution was not perfectly even, each server successfully handled a portion of the incoming traffic. Server-1 processed the highest number of requests, while Server-2 and Server-3 handled the remaining requests.
The imbalance occurs because the consistent hashing algorithm maps requests based on hash values rather than using a round-robin strategy. With only nine virtual nodes per server, some servers naturally receive a larger share of the hash space.

Conclusion:
The experiment demonstrates that the load balancer correctly routes requests to multiple backend servers. The implementation is functional and capable of distributing traffic, although increasing the number of virtual nodes would improve load balancing fairness.

<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/15621f48-698f-4f24-a948-d57120763321" />

A-2: Scalability Analysis (N = 2 to N = 6)

Objective - The purpose of this experiment was to evaluate how well the load balancer scales as the number of backend server replicas increases. The number of server replicas (N) was varied from 2 to 6, and 10,000 client requests were sent during each run. The average number of requests handled per server was then recorded and plotted in a line chart.

Method

For each experiment:

The required number of server replicas was created using the /add and /rm endpoints.
A total of 10,000 asynchronous HTTP requests were generated.
Each backend server recorded the number of requests it processed.
The average load per server was calculated using
Average Load=Number of Servers/Total Requests
	​
The average load values were plotted against the number of server replicas.

Observations:
The line chart shows that the average number of requests handled by each server decreases as more server replicas are added.

For example: 
Number of Servers	Average Requests per Server

2	5000.0

3	3333.335

4	2449.75

5	1997.4

6	1666.667


Performance Analysis:
The results demonstrate that the load balancer is scalable.

As additional server replicas are introduced:
the workload is divided among more servers,
the processing load on each server decreases,
the system becomes capable of serving more client requests without overloading a single server,
response time can potentially improve since individual servers handle fewer requests.

The consistent hashing implementation allows new servers to join the system without requiring all existing requests to be redistributed, which minimizes disruption and improves scalability.

Conclusion:
The experiment confirms that the load balancer scales effectively with an increasing number of server replicas. Increasing the number of backend servers reduces the average workload handled by each server while maintaining correct request routing through the consistent hash ring. This demonstrates that the implementation is capable of supporting higher workloads by simply adding more server instances.

<img width="800" height="500" alt="image" src="https://github.com/user-attachments/assets/daaa4740-50e3-4b1f-adac-6daec7f45eb1" />

A-3 Server Failure Recovery

The heartbeat monitor continuously checks the health of all backend replicas every five seconds. When a backend server was manually stopped using Docker, the heartbeat detected that the server had become unreachable. The load balancer automatically removed the failed server from the consistent hash ring and created a replacement container with the same server identifier. During recovery, client requests continued to be processed by the remaining replicas, demonstrating fault tolerance and high availability. The automatic recovery mechanism restored the original number of replicas within a few seconds without requiring manual intervention.

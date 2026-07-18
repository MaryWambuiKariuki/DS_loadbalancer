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


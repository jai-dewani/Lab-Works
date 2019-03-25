n = int(input("Enter number of jobs: "))
print("Enter Process ID, Arrival Time, Burst Time")
arival_burst_time = []
for a in range(0, n):
	temp = list(map(int, input().strip().split()))

	temp[0], temp[1] = temp[1], temp[0]

	arival_burst_time.append(temp)

arival_burst_time.sort()

currentTime = arival_burst_time[0][0]+arival_burst_time[0][2]

ready = []
finished = []
completionTime = []

i = 0
while len(finished) != n:
	completionTime.append(currentTime)
	while True:
		if i < n and arival_burst_time[i][0] <= currentTime:
			ready.append(arival_burst_time[i])
			i += 1
		else:
			break
	if ready == []:
		currentTime += 1
		continue
	ready.sort(key = lambda x : x[2])

	finished.append(ready.pop(0))
	currentTime += ready[0][2]

print(finished)
completionTime.append(currentTime)
print(completionTime)


arg = input("Enter the number of jobs")
print("Enter PID - Arrival Time - Burst Time")
db = []
for a in range(0, arg):
	temp = map(int, raw_input().strip().split())

	temp[0], temp[1] = temp[1], temp[0]

	temp.extend([0, (0 + temp[2]) / temp[2]])

	db.append(temp)

db.sort()

currentTime = db[0][0]

ready = []
finished = []
timeTakenByProcesses = []

i = 0
while len(finished) != arg:
	while True:
		if i < arg and db[i][0] <= currentTime:
			ready.append(db[i])
			i += 1
		else:
			break
	if ready == []:
		currentTime += 1
		for d in range(0, len(ready)):
			ready[a][3] += 1
			ready[a][4] = (ready[a][3] + ready[a][2]) / ready[a][2]
		continue
	ready.sort(key = lambda x : x[4])
	ready.reverse()

	# finished.append(ready[0])
	# currentTime += ready[0][2]
	# ready.pop(0)

	ready[0][2] -= 1
	currentTime += 1
	if ready[0][2] == 0:
		finished.append(ready[0])
		timeTakenByProcesses.append([currentTime, ready[0][1]])
		ready.pop(0)

print(finished)
print(timeTakenByProcesses)
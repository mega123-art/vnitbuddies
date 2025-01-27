n=int(input())
difficulty = []
happiness = []

for i in range(n):
    difficulty.append(int(input()))
for i in range(n):
    happiness.append(int(input()))

k=int(input())
skill=[]
for i in range(k):
    skill.append(int(input()))

for i in range(len(happiness)):
    for j in range(len(happiness) - 1):
        if happiness[j] < happiness[j + 1]:
            # Swap elements in both lists
            happiness[j], happiness[j + 1] = happiness[j + 1], happiness[j]
            difficulty[j], difficulty[j + 1] = difficulty[j + 1], difficulty[j]
count=0
sum=0
skill.sort()
for i in range(n):
    for j in range(len(skill)):
        if skill[j]>=difficulty[i] and count!=k:
            count+=1
            sum+=happiness[i]
            break
   

    

print(sum)

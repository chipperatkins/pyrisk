f = open('output.txt','r')
results = {}
for line in f:
	words = line.split()
	for idx,word in enumerate(words):
		if '[' in word:
			if results.has_key(word):
				results[word] += int(words[idx+1])
			else:	results[word] = int(words[idx+1])
print results

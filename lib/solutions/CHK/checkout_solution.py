

# noinspection PyUnusedLocal
# skus = unicode string
from collections import Counter

def checkout(skus):
	ccc = Counter([x for x in skus])
	tot = 0
	grand_tot = 0
	print (ccc)
	for (cc,num) in ccc.items():
		print (cc,num)
	return grand_tot
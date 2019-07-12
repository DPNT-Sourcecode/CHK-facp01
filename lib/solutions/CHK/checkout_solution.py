

# noinspection PyUnusedLocal
# skus = unicode string
from collections import Counter

PriceList = { 'A':50, 'B':30, 'C':20, 'D':15 }
SpecialOffers = { 'A':(3,130), 'B':(2,45) }

def checkout(skus):
	ccc = Counter([x for x in skus])
	tot = 0
	grand_tot = 0
	print (ccc)
	for (cc,num) in ccc.items():
		price = PriceList.get(cc,0)
		so = SpecialOffers.get(cc,())
		if price == 0 and not so:
			return -1
		num_so, p_so = (so[0], so[1]) if so else (1,0)  # get special price
		tot = ( num/num_so * p_so) + ( num % num_so * price) if so else num * price  # price special offers + normal price
		grand_tot += tot
		print ("cc: {},num: {} price: {} so: {} tot: {} grand_tot: {}".format(cc,num,price,so,tot,grand_tot))
	return grand_tot
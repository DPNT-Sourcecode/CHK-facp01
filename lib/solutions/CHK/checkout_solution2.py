

# noinspection PyUnusedLocal
# skus = unicode string
from collections import Counter

'''
+------+-------+------------------------+
| Item | Price | Special offers         |
+------+-------+------------------------+
| A    | 50    | 3A for 130, 5A for 200 |
| B    | 30    | 2B for 45              |
| C    | 20    |                        |
| D    | 15    |                        |
| E    | 40    | 2E get one B free      |
+------+-------+------------------------+
'''

PriceList     = { 'A':50, 'B':30, 'C':20, 'D':15, 'E':40 }
SpecialOffers = { 'A':[(3,130),(5,200),(1,50)], 'B':[(2,45),(1,30)], 'C':[(1,20)], 'D':[(1,15)], 'E':[(1,40)] } # , 'E':[(2,'B')] }
FreeOffers    = { 'E':[(2,'B')] } 

TESTING = True	# set to True when debugging

# debug options ...

### debug = print    		# uncomment - to turn on extra debug and comment out line below
def debug(*argv): pass	# comment out for additional debug...

def skusValid(cntSkus):
	''' check the skus all exist in the sperciaqlOffers '''
	validSkus = map(lambda x: x in cntSkus, SpecialOffers.keys())
	print("{} == {}".format(cntSkus,validSkus))
	return all(validSkus)


def tot_free_offers(cc, num, cntSkus ):
    '''
    calculate the free offers (if any) on a specific group of SKU
    eg. EEEEE => EE EE (2) E (1) => B B E =>  -45 + 40
    '''
    grand_tot = 0
    fo = FreeOffers.get(cc,())		# B => [(2,45),(1,30)]
    fo = sorted(fo,reverse=True)   		# sort is descending order

    for ff in fo: 						# loop through free offers
        debug ('tot_free_offers ' + '-'*10, cc, num, ff)
        f0,f1 = ff[0], ff[1]			# E == 2 'B'
        n0 =  (num//f0);				# EEEEE => EE EE (2) E (1) ==> 2
        numf1 = cntSkus.get(f1,0)				# actual number of "free" Bs ordered
        debug ("eligible for {} free {} - actual: {}".format(n0,f1,numf1))
        num_free = min(n0,numf1)		# you only get discount if actually ordered the free sku "B"
        tot = price_sku(f1,num_free)
        grand_tot += tot
        debug ("tot_free_offers - grand_tot: {}".format(grand_tot))
    return grand_tot

def price_sku(cc, num ):   # B 2 
    ''' 
    Price a SKU (or multiple) eg. BBB => B 3 
    '''
    grand_tot = 0
    so = SpecialOffers.get(cc,())		# B => [(2,45),(1,30)]
    so = sorted(so,reverse=True)   		# sort is descending order


    for ss in so: 						# loop through special offers
        debug ('price_sku '+'-'*10, cc, num, ss)
        s0,s1 = ss[0], ss[1]
        n0 =  (num//s0);
        num -= n0 * s0
        #debug (s0,s1,n0,num)
        tot = (n0*s1); 
        grand_tot += tot
        debug (cc,tot,grand_tot)
    return grand_tot

# main checkout funtion...
def checkout(skus):
	''' price a list of skus
	eg. AAAABBCC == 4A = 3A(130) + A(50) == 180
	                2B = 2B(45)
	                2C = 2C(40)      ==> 265
	'''
	cntSkus = Counter([x for x in skus])
	if not skusValid(cntSkus):
		return -1
	tot = 0
	grand_tot = 0
	debug(SpecialOffers)
	debug(skus)
	debug(cntSkus)

	for (cc,num) in cntSkus.items():
		grand_tot += price_sku(cc, num)						# calc normal price
		grand_tot -= tot_free_offers(cc, num , cntSkus)		# remove free offers (if eligible)
		debug ("cc: {},num: {} grand_tot: {}".format(cc,num,grand_tot))

	return grand_tot

# test suite...
def test():
	goods = "AAAABBCC"
	res = checkout(goods)
	print ("test 1 - res: {} ==> ".format(res) + "True" if (res == 265) else "False")

	goods = "AAAEE"
	res = checkout(goods)
	print ("test 2 - res: {} ==> ".format(res) + "True" if (res == 210) else "False")


	goods = "AAAEEBB"
	res = checkout(goods)
	print ("test 3 - res: {} ==> ".format(res) + "True" if (res == 225) else "False")

	goods = "ABBBBBBBBCCC"
	res = checkout(goods)
	print ("test 4 - res: {} ==> ".format(res) + "True" if (res == 290) else "False")

	res = price_sku('E', 3 )		# EEE
	print ("test 5 - res: {} ==> ".format(res) + "True" if (res == 120) else "False")

	skus = 'EEEEEEE'
	cntSkus = Counter([x for x in skus])
	res = tot_free_offers('E', 7 , cntSkus)		# EEEEEEE
	print ("test 6 - res: {} ==> ".format(res) + "True" if (res == 0) else "False")

#   invalid data tests
	data = [ "a", "-", "ABCa"]
	for goods in data:
		goods = "a"
		res = checkout(goods)
		print ("test 7 - res: {} ==> ".format(res) + "True" if (res == -1) else "False")


# unit testing
if TESTING:
	test()

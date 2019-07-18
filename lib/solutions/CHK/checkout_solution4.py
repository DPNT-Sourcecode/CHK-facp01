

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
| F    | 10    | 2F get one F free      |
| G    | 20    |                        |
| H    | 10    | 5H for 45, 10H for 80  |
| I    | 35    |                        |
| J    | 60    |                        |
| K    | 80    | 2K for 150             |
| L    | 90    |                        |
| M    | 15    |                        |
| N    | 40    | 3N get one M free      |
| O    | 10    |                        |
| P    | 50    | 5P for 200             |
| Q    | 30    | 3Q for 80              |
| R    | 50    | 3R get one Q free      |
| S    | 30    |                        |
| T    | 20    |                        |
| U    | 40    | 3U get one U free      |
| V    | 50    | 2V for 90, 3V for 130  |
| W    | 20    |                        |
| X    | 90    |                        |
| Y    | 10    |                        |
| Z    | 50    |                        |
+------+-------+------------------------+


'''

SpecialOffers = { 'A':[(3,130),(5,200),(1,50)], 'B':[(2,45),(1,30)], 'C':[(1,20)], 'D':[(1,15)], 'E':[(1,40)], \
		'F':[(1,10)], \
		'G':[(1,20)], \
		'H':[(5,45),(10,80),(1,10)],   # 5H for 45, 10H for 80 \
		'I':[(1,35)], \
		'J':[(1,60)], \
		'K':[(1,80), (2,150)], 	# 2K for 150 \
		'L':[(1,90)], \
		'M':[(1,15)], \
		'N':[(1,40)], \
		'O':[(1,10)], \
		'P':[(1,50),(5,200)], \
		'Q':[(1,30),(3,80)], \
		'R':[(1,50)], \
		'S':[(1,30)], \
		'T':[(1,20)], \
		'U':[(1,40)], \
		'V':[(1,50),(2,90),(3,130)], \
		'W':[(1,20)], \
		'X':[(1,90)], \
		'Y':[(1,10)], \
		'Z':[(1,50)] }

FreeOffers    = { 'E':[(2,'B')], 'F':[(2,'F')], 'N':[(3, 'M')], 'R':[(3, 'Q')], 'U':[(3, 'U')] } 

MultiBuyGoods = "STXYZ"


TESTING = True	# set to True when debugging

# debug options ...

debug = print    		# uncomment - to turn on extra debug and comment out line below
#def debug(*argv): pass	# comment out for additional debug...

def skusValid(cntSkus):
	''' check the skus all exist in the sperciaqlOffers '''
	sk = SpecialOffers.keys()
	ck = cntSkus.keys()
	valid = all (k in sk for k in ck)
	debug ("sk: {} ck:  {}== {}".format(sk,ck,valid))
	return valid


def tot_free_offers(cc, num, cntSkus ):
    '''
    calculate the free offers (if any) on a specific group of SKU
    eg. EEEEE => EE EE (2) E (1) => B B E =>  -45 + 40
    '''
    discount_tot = 0
    fo = FreeOffers.get(cc,())			# 'E':[(2,'B')]
    fo = sorted(fo,reverse=True)   		# sort is descending order

    for ff in fo: 						# loop through free offers
        debug ('tot_free_offers ' + '-'*10, cc, num, ff)
        f0,f1 = ff[0], ff[1]			# E == 2 'B'
        ### n0 =  (num//f0)					# EEEEE => EE EE (2) E (1) ==> 2
       	special_case = (cc == f1)
       	###print (cc,f1,special_case)
       	n0 =  (num//f0) if not special_case else (num//(f0+1))
        numf1 = cntSkus.get(f1,0)				# actual number of "free" Bs ordered
        debug ("eligible for {} free {} - actual: {}".format(n0,f1,numf1))   # eligible for 1 free B - actual: 2
        num_free = min(n0,numf1)		# you only get discount if actually ordered the free sku "B"
        if num_free > 0:   # 
	        totF = price_sku(f1,numf1-num_free)	# 1 == 30 
	        totA = price_sku(f1,numf1)		# 2 == 45
	        discount_tot += totF            # if totF > totF else totF
	        discount_tot -= totA
        debug ("tot_free_offers - discount_tot: {}".format(discount_tot))
    return discount_tot

def price_sku(cc, num=1 ):   # B 2 
    ''' 
    Price a SKU (or multiple) eg. BBB => B 3 
    '''
    grand_tot = 0
    so = SpecialOffers.get(cc,())		# B => [(2,45),(1,30)]
    so = sorted(so,reverse=True)   		# sort is descending order


    for ss in so: 						# loop through special offers
        #debug ('price_sku '+'-'*10, cc, num, ss)
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
		grand_tot += tot_free_offers(cc, num , cntSkus)		# remove free offers (if eligible)
		debug ("cc: {},num: {} grand_tot: {}".format(cc,num,grand_tot))

	grand_tot -= multi_buy_discount(skus)

	return grand_tot

def price_good(good):
    tot = 0
    for c in good:
    	tot += price_sku(c)
    return tot	

def multi_buy_discount(goods):
	sgoods = set(goods)
	sfree  = set(MultiBuyGoods)
	comm = sgoods & sfree
	pcomm = price_good(comm)
	discount = 0
	if len(comm) >= 3:
		discount = pcomm - 45
	print ("sgoods: {} sfree:{} comm: {} pcomm: {} discount: {}".format(sgoods,sfree,comm,pcomm,discount))
	return discount


# ---------     test suite...-------------------
def test_goods(skus,exp):
 	res = checkout(skus)
 	print ("test 8 - res: {} ==> ".format(res) + "True" if (res == exp) else "False")


def test():
# 	goods = "AAAABBCC"
# 	res = checkout(goods)
# 	stat = "True" if (res == 265) else "False"
# 	print ("test 1 - res: {} ==> {}".format(res,stat))

# 	goods = "AAAEE"
# 	res = checkout(goods)
# 	print ("test 2 - res: {} ==> ".format(res) + "True" if (res == 210) else "False")


# 	goods = "AAAEEBB"
# 	res = checkout(goods)
# 	print ("test 3 - res: {} ==> ".format(res) + "True" if (res == 240) else "False")  ## /??

# 	goods = "ABBBBBBBBCCC"
# 	res = checkout(goods)
# 	print ("test 4 - res: {} ==> ".format(res) + "True" if (res == 290) else "False")

# 	res = price_sku('E', 3 )		# EEE
# 	print ("test 5 - res: {} ==> ".format(res) + "True" if (res == 120) else "False")

# 	skus = 'EEEEEEE'
# 	cntSkus = Counter([x for x in skus])
# 	res = tot_free_offers('E', 7 , cntSkus)		# EEEEEEE
# 	print ("test 6 - res: {} ==> ".format(res) + "True" if (res == 0) else "False")

# #   invalid data tests
# 	data = [ "a", "-", "ABCa"]
# 	for goods in data:
# 		goods = "a"
# 		res = checkout(goods)
# 		print ("test 7 - res: {} ==> ".format(res) + "True" if (res == -1) else "False")

# 	goods = "ABCDEABCDE"
# 	res = checkout(goods)
# 	print ("test 8 - res: {} ==> ".format(res) + "True" if (res == 280) else "False")
	
    test_goods("EEB",80)
    test_goods("ABCDE",155)
    test_goods("EEEB",120)
    test_goods("ABCDEABCDE",280)
    test_goods("ABCDEABCDE",280)
    test_goods("AAAAAEEBAAABB",455)
    test_goods("ABCDECBAABCABBAAAEEAA",665)
    test_goods("F",10)
    test_goods("FF",20)
    test_goods("ABCDEF",165)


def test2():
	goods = "ABCXYZ"
	goods = "XYZ"
	disc = multi_buy_discount(goods)


# unit testing
if TESTING:
	#test()
	test2()
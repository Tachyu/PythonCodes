start = '2015-11-01'                       # 回测起始时间
end = '2016-06-01'                         # 回测结束时间
benchmark = 'HS300'                        # 策略参考标准
universe = ['000429.XSHE', '000521.XSHE', '000539.XSHE', '000553.XSHE', '000596.XSHE']  # 证券池，支持股票和基金
# universe  = ['601398.XSHG', '600028.XSHG', '601988.XSHG', '600036.XSHG', '600030.XSHG',
#                '601318.XSHG', '600000.XSHG', '600019.XSHG', '600519.XSHG', '601166.XSHG']
capital_base = 100000                      # 起始资金
commission = Commission(buycost=0.001, sellcost=0.008, unit='perValue')
freq = 'd'                                 # 策略类型，'d'表示日间策略使用日线回测，'m'表示日内策略使用分钟线回测
refresh_rate = 1                           # 调仓频率，表示执行handle_data的时间间隔，若freq = 'd'时间间隔的单位为交易日，若freq = 'm'时间间隔为分钟

def initialize(account):                   # 初始化虚拟账户状态
    pass

#获取五日均值
def get5ave(account,stock,div=0):
    hist = account.get_attribute_history('closePrice', 5 + div)
    return sum(hist[stock][0:4])/5

#获取十日均值
def get10ave(account,stock,div=0):
    hist = account.get_attribute_history('closePrice', 10 + div)
    return sum(hist[stock][0:4])/10

#大致判断数列增减性
def isIncre(dif):
    incre_time = 0
    decre_time = 0
    for i in range(0,len(dif) - 2,1):
        #变化率加大
        if dif[i] - dif[i+1] > 0:
            incre_time += 1
        else:
            decre_time += 1

    if incre_time > decre_time:
        return True
    else:
        return False

def isTimeToChange(account, stock):
    ave_5 = []
    ave_10 = []

    for i in range(0,3,1):
        ave_5.append(get5ave(account, stock, i))
        ave_10.append(get10ave(account, stock, i))
    
    #10日均值于5日均值的差
    dif_10_5 = list(map(lambda x: x[0]-x[1], zip(ave_10, ave_5)))  

    #3天内：5日均值与10日均值上升交叉，则为买入机会
    if (isIncre(account.get_attribute_history('closePrice', 3)[stock])):
        if (isIncre(dif_10_5)):
            return 1
        else:
            return 0
    #3天内：5日均值与10日均值下降交叉，则为买入机会
    else:
        if (isIncre(dif_10_5)):
            return -1
        else:
            return 0



# #获取十日变化率变化情况
# #变化率减缓，返回1
# #变化率变大，返回-1
# def getDifSta(account,stock):

#     dif = []
#     hist = account.get_attribute_history('closePrice', 11)

#     #计算变化率
#     for i in range(1,10,1):
#         dif.append(abs(hist[stock][i] - hist[stock][i - 1]))

#     if (isIncre



# #若五日均值小于十日均值，且变化率减缓，则买入，返回 1
# #若五日均值小于十日均值，且变化率变大，则卖出，返回-1
# #若五日均值大于十日均值，且变化率变大，则买入, 返回 1
# #若五日均值大于十日均值，且变化率减缓，则卖出, 返回-1
# def handle_sub(account,stock):
#     if get5ave(account,stock) < get10ave(account,stock):
#         # return 1
#         if getDifSta(account,stock) == 1:
#             return 1
#         else:
#             return -1
#     else:
#         # return -1
#         if getDifSta(account,stock) == -1:s
#             return 1
#         else:
#             return -1
            



def handle_data(account):                  # 每个交易日的买入卖出指令
    hist = account.get_attribute_history('closePrice', 10)
    boll_up = 0.7
    boll_down = 0.3
    for s in account.universe:
        bollData = DataAPI.MktStockFactorsOneDayGet(tradeDate=str(account.previous_date)[0:10].replace('-',''),secID = s,field=u"BollUp,BollDown",pandas="1")        
        status = isTimeToChange(account, s)
        rate = (account.referencePrice[s] - bollData['BollDown']) / (bollData['BollUp'] - bollData['BollDown'])
        if len(rate) != 1:
            print 'error'
            return

        if rate[0] >= boll_up:
            order_to(s,0)
        elif rate[0] <= boll_down:
            order(s,500)
        else:
            order(s,100)
        # #价格处于上游
        # if rate == boll_up and status == 1:
        #     order(s,1000)
        # elif rate == boll_up and status == 0:
        #     pass
        # elif rate == boll_up and status == -1:
        #     order_to(s,0)
        # elif rate == boll_down and status == 1:
        #     order(s,2000)
        # elif rate == boll_down and status == 0:
        #     order(s,500)
        # else: #rate == boll_down and status == -1:
        #     order_to(s,0)
    return

class steprate:
    """
    rate = [
        (10000,10),
        (20000,15),
        (30000,20),
        (40000,25),
        (50000,30),
        (-1,50),
    ]
    """
    def __init__(self,steptype=None):
        self.types = ['full', 'stepfull', 'stepover'] 
        self.type = self.getType(steptype) if steptype else None
        self.amount = 0
        self.result = 0
        self.results = []
        self.rate = []
        
    def getType(self,t):
        if t is None:
            return self.type if self.type else None
        
        if isinstance(t, int):
            # rst = self.types[t-1] if t>0 else None
            rst = t if t in range(1,len(self.types)) else None
        
        if isinstance(t, str):
            rst = self.types.index(t) + 1 if self.types.count(t)>0 else None
            
        self.type = rst
        return rst
    
    def checkRate(self, rate:list):
        rst = [r[0] for r in rate if r[0]==-1]
        return True if len(rst) else False
    
    def getRateIndex(self,amount,steps:list):
        # if self.checkRate(rate) == False:
        #     print('Bad format of Rate')
        #     return None
        if amount > steps[-2]:
            return len(steps)
        for index, b in enumerate(steps):
            if amount <= b:
                return index
    
    def compute(self, amount:float, rate:list or float, deduction:float=0, steptype:str=None):
        deduction = abs(deduction)
        self.amount = amount
        
        if amount <= 0 or amount <= deduction:
            return 0

        if self.checkRate(rate) == False:
            print('Bad format of Rate')
            return None
        
        if steptype:
            steptype = self.getType(steptype)
        
        if self.type == 1:
            rate = rate[-1][-1] if isinstance(rate, list) else rate
            return self.compute_full(amount, rate, deduction)
        elif self.type == 2:
            return self.compute_stepfull(amount, rate, deduction)
        elif self.type == 3:
            return self.compute_stepover(amount, rate, deduction)
        else:
            return None

    def compute_full(self, amount:float, rate:float, deduction:float=0):
        deduction = abs(deduction)
        if amount > deduction:
            rst = (amount - deduction) * rate / 100
        else:
            rst = 0
        
        self.result = rst
        self.results = [rst]
        return rst
    
    def compute_stepfull(self, amount:float, rate:list, deduction:float=0):
        deduction = abs(deduction)
        if amount <= 0 or amount <= deduction:
            return 0

        if self.checkRate(rate) == False:
            print('Bad format of Rate')
            return None

        r_index = self.getRateIndex(amount, [r[0] for r in rate])
        if r_index == len(rate):
            rst = (amount - deduction) * rate[-1][1] / 100
        else:
            rst = (amount - deduction) * rate[r_index][1] / 100

        self.result = rst
        self.results = [rst]
        return rst

    def compute_stepover(self, amount:float, rate:list, deduction:float=0):
        deduction = abs(deduction)
        if amount <= 0 or amount <= deduction:
            return 0

        if self.checkRate(rate) == False:
            print('Bad format of Rate')
            return None
        
        steps = [r[0] for r in rate]
        rates = [r[1] for r in rate]
        addup = []

        r_index = self.getRateIndex(amount, steps)
        steps = steps[:r_index] if r_index > 0 else steps[0:1]
        steps = steps + [-1] if -1 not in steps else steps
        rates = rates[:len(steps)]
        
        for index, s in enumerate(steps):
            amount2 = amount-deduction
            if index == 0:
                amount2 = amount2 if amount2 <= s else s
                
            elif index+1==len(steps):
                amount2 = amount2 - steps[index-1]
                amount2 = amount2 if amount2 > 0 else 0
                
            else:
                amount2 = steps[index] - steps[index-1] if amount2 > steps[index] else  amount2 - steps[index-1]
                
            addup.append(amount2 * rates[index] / 100)

        # print(amount,amount2,r_index, steps, rates, addup)
        self.results = addup
        self.result = sum(addup)
        return sum(addup)

if __name__ == "__main__":
    rate = [
        (10000,10),
        (20000,15),
        (30000,20),
        (40000,25),
        (50000,30),
        (-1,50),
    ]
    
    obj = steprate()
    obj.compute(70001, rate, 10000,'stepover')
    
    print(obj.result)
    print(obj.results)
    
import json
#jsonvals is either defined or passed in during definition
class timetablegenerator():
    def __init__(self,l):
        #self.jsonvals = jsonvals
        self.l = l
        self.LTimings = [["08:00-08:50","09:00-09:50","10:00-10:50","11:00-11:50","12:00-12:50",""],"LUNCH",["14:00-14:50","15:00-15:50","16:00-16:50","17:00-17:50","18:00-18:50","19:00-19:50"]]
        self.PTimings = [["08:00-08:50","08:51-09:40","09:51-10:40","10:41-11:30","11:40-12:30","12:31-13:20"],"LUNCH",["14:00-14:50","14:51-15:40","15:51-16:40","16:41-17:30","17:40-18:30","18:31-19:20"]]
        self.schedule = [
            [[None, None, None, None, None], 'LUNCH', [None, None, None, None, None, None]],
            [[None, None, None, None, None], 'LUNCH', [None, None, None, None, None, None]],
            [[None, None, None, None, None], 'LUNCH', [None, None, None, None, None, None]],
            [[None, None, None, None, None], 'LUNCH', [None, None, None, None, None, None]],
            [[None, None, None, None, None], 'LUNCH', [None, None, None, None, None, None]]
            ]
        with open('data.json','r') as f:
                    c = f.read()
                    self.jsonvals  = json.loads(c)
        self.LSlots = [
            [["A1","F1","D1","TB1","TG1"],[],["A2","F2","D2","TB2","TG2"]],
            [["B1","G1","E1","TC1","TAA1"],[],["B2","G2","E2","TC2","TAA2"]],
            [["C1","A1","F1","V1","V2"],[],  ["C2","A2","F2","TD2","TBB2"]],
            [["D1","B1","G1","TE1","TCC1"],[],["D2","B2","G2","TE2","TCC2"]],
            [["E1","C1","TA1","TF1","TDD1"],[],["E2","C2","TA2","TF2","TDD2"]],
                  ]
        self.PSlots = [
            [['L1', 'L2', 'L3', 'L4', 'L5', 'L6'],[],['L31', 'L32', 'L33', 'L34', 'L35', 'L36']],
            [['L7', 'L8', 'L9', 'L10', 'L11', 'L12'],[],['L37', 'L38', 'L39', 'L40', 'L41', 'L42']],
            [['L13', 'L14', 'L15', 'L16', 'L17', 'L18'],[],['L43', 'L44', 'L45', 'L46', 'L47', 'L48']],
            [['L19', 'L20', 'L21', 'L22', 'L23', 'L24'],[],['L49', 'L50', 'L51', 'L52', 'L53', 'L54']],
            [['L25', 'L26', 'L27', 'L28', 'L29', 'L30'],[],['L55', 'L56', 'L57', 'L58', 'L59', 'L60']]
             ]
        self.final_alloted = []
        self.final_courses = []
        self.theorymorn = 1
        #assumed theory morning
        self.timings_gen()

    def timings_gen(self):
        if self.theorymorn:
            self.Timings = [self.LTimings[0],"LUNCH",self.PTimings[2]]
            self.Time = self.Timings[0] + ["LUNCH",]+ self.Timings[2]
        else:
            self.Timings = [self.PTimings[0],"LUNCH",self.LTimings[2]]
            self.Time = self.Timings[0] + ["LUNCH",]+ self.Timings[2]

    def priority_order(self,d):
        p = dict()
        for i in d:
            k,v = i,d[i]
            try:
                p[v].append(k)
            except:
                p[v] = [k,]
        d = dict(sorted(p.items(),reverse = True))
        return d
    
    def listcreator(self,l):
        self.l2 = []
        for i in l:
            self.l2.append(list(self.jsonvals[i]["SLOTS"].keys()))
        return self.l2

    def getslot(self,slot,lorp = 'L'):
        l = []
        slotss = list(slot.split('+'))
        if lorp == 'L':
            for i in self.LSlots:
                for j in i:
                    for k in j:                    
                        if k in slot:
                            l.append((self.LSlots.index(i),i.index(j),j.index(k)))
                            break
        elif lorp == 'P':
            for i in self.PSlots:
                for j in i:
                    for k in j:
                        if k in slotss:
                            t = (self.PSlots.index(i),i.index(j),j.index(k))
                            l.append(t)
                            continue
        return l

    def slot_empty(self,t):#return True if empty
        #print(self.schedule)
        try:
            #print(self.schedule[t[0]][t[1]][t[2]])
            if self.schedule[t[0]][t[1]][t[2]] == None:
                return True
            return False
        except:
            return False

    def valid_slot(self,course,slot):
        if self.theorymorn:
            if course[-1] == "L" or course[:4] == "BSTS":#theory class
                u = self.getslot(slot,"L")
                for i in u:
                    if i[1] != 0:
                        return False

            else:#lab class
                u = self.getslot(slot,"P")
                for i in u:
                    if i[1] != 2:
                        return False
        else:
            if course[-1] == "L" or course[:4] == "BSTS":#theory class
                u = self.getslot(slot,"L")
                for i in u:
                    if i[1] != 2:
                        return False

            else:#lab class
                u = self.getslot(slot,"P")
                for i in u:
                    if i[1] != 0:
                        return False
        return True

    def setslot(self,t,code, p = 1):
        if p:
            try:
                if self.slot_empty(t):
                    self.schedule[t[0]][t[1]][t[2]] = code                    
                    return True
                else:                    
                    return False
            except:
                return False
        else:
            self.schedule[t[0]][t[1]][t[2]] = None
            return True

    def set_sch(self,final):
        for i in final:
            for j in i[2]:
                self.setslot(j,i[0])

    def timetable(self,l,ind = 0):
        if ind == len(l):
            return True
        else:
            course = l[ind]
            lorp = 'P'
            if course[-1] == 'L' or course[:4] == "BSTS":
                lorp = 'L'
            courseoptions = self.l2[ind]
            for j in range(len(courseoptions)):                
                k = courseoptions[j]                
                u = self.getslot(k,lorp)                
                for i in u:
                    x = self.slot_empty(i)                    
                    y = self.valid_slot(course,k)
                    if (not y):
                        break
                    if (not x):
                        break
                    self.setslot(i,course)
                    if self.timetable(l,ind+1):                
                        self.final_alloted.append([course,courseoptions[j],u,y])
                        return True
                    else:
                        pass
        return False
    
    

                
    def print_sch(self,s):
        print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        print("|     ",end = '')
        for k in self.Time:
            if k == "LUNCH":
                    print("LUNCH",end = ' ')
            elif k == ' ':
                pass
            else:            
                print('|',k,end = ' ')
        print('|')
        print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        days = ['MON','TUE','WED','THU','FRI']
        for l in range(len(s)):
            i = s[l]
            print('|',days[l],end =' ')
            for j in i[0]+ ["LUNCH",]+i[2] :
                if j == None:
                    print('|',' '*11,end = " ")
                elif j == "LUNCH":
                    print("|  LUNCH ",end = '')
                else:
                    print('|  ',j,end ='  ')
            print('|')
            print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

        print("  COURSE  |   SLOT ")     
        for i in self.final_alloted:
            print(' ',i[0],' | ',i[1],sep = '')
    def final_generation(self):
        self.l2 = self.listcreator(self.l)
        self.t = self.timetable(self.l)
        self.set_sch(self.final_alloted)
        #self.print_sch(self.schedule)
        if self.t:
            self.print_sch(self.schedule)
        else:
            print('not possible try different set of subjects'.upper())
        return

def r():
    l = ['BECE101L','BECE101P','BPHY101P','BPHY101L','BSTS102P','BMAT102L','BENG101L','BENG101P','BCSE102L','BCSE102P']

    timetablegen = timetablegenerator(l)
    timetablegen.final_generation()

r()


        
                   

from docx.api import Document
import json
document = Document('courseallocationreport.docx')
d = {}
d2 = {}
for z in range(59):
    table = document.tables[z]
    keys = None
    for i, row in enumerate(table.rows):
        text = [cell.text for cell in row.cells]
        t = text[0]
        slot = text[3]
        name = text[4]

        if t == "COURSE COD" or t == '':
            continue
        if t not in d:
            try:
                d[t] = float(text[2])
                d2[t] = {"COURSE TITLE": text[1],"CREDITS": float(text[2]),"SLOTS" :  {slot:1,}}
            except:
                d[t] = 0
                d2[t] = {"COURSE TITLE": text[1],"CREDITS": 0,"SLOTS" :  {slot:1,}}
        
        if slot in d2[t]["SLOTS"]:
                d2[t]["SLOTS"][slot] += 1
        else:
            d2[t]["SLOTS"][slot] = 1
        
        try:
            d2[t][name].append(slot)
            if slot not in d2[t]["SLOTS"]:
                d2[t]["SLOTS"].append(slot)
        except:
            d2[t][name] = [slot,]

d2['COURSES AVAILABLE'] = d


with open('data.json','w') as f:
    json.dump(d2,f,indent = 1)
print('done')

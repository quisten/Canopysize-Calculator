#
# CanopySize Tables 2 JSON files
# 
# Manually import tables and indices and convert these to JSON files
# 
# 1.Norwegian_Regulations
# 2.BrianG_Recommendations
# 3.Swedish_Regulations
# 4.French_Regulations 
# 5.British_Regulations
#
# Save as [Table_Content.JSON, Table_Index.JSON]
########################################################################

import json
import csv


def main():

    exportNorwegian = True
    exportBrianG = True
    exportSweden = True
    exportBritish = True
    exportFrench = True

    if exportNorwegian:

        weight = [x+10 for x in range(60, 130, 5)]
        highWLSize = [int((x*2.20462)/2.6) for x in weight]
        print(highWLSize)
        # Weights                  60,  65,  70,  75,  80,  85,  90,  95,  100, 105, 110, 115, 120, 125 
        NLF_Rules = {20:  { "Student" : [190, 190, 190, 190, 190, 210, 210, 230, 230, 250, 250, 250, 270, 270] },
                    100: { "A" : [160, 160, 170, 180, 180, 190, 190, 190, 190, 210, 210, 230, 230, 240] },
                    200: { "B" : [140, 140, 150, 160, 160, 170, 170, 170, 170, 190, 190, 210, 210, 220] },
                    400: { "B" : [130, 135, 140, 150, 150, 160, 160, 160, 160, 170, 170, 190, 190, 200], 
                           "B+AdvCanopyCourse": [117, 120, 124, 127, 129, 134, 139, 144, 150, 158, 165, 174, 178, 185] },
                    600: { "B" : [120, 125, 130, 140, 140, 150, 150, 150, 150, 160, 160, 170, 180, 190],
                            "C+AdvCanopyCourse": [109, 111, 114, 117, 117, 120, 124, 128, 132, 140, 145, 154, 165, 170]}, 
                    800: { "B" : [110, 115, 120, 125, 130, 135, 135, 140, 140, 150, 150, 160, 160, 170], 
                            "C+AdvCanopyCourse": [100, 100, 104, 107, 109, 114, 117, 120, 124, 128, 132, 140, 145, 150]},
                    1000: { "B" : [105, 105, 110, 115, 120, 125, 125, 130, 130, 140, 140, 150, 150, 160],
                            "C+CanopyCourse": [ 96,  96,  99,  99,  99, 104, 107, 109, 112, 117, 119, 124, 129, 135]},
                    1200: { "C" : [ 85,  85,  90,  90,  90,  95, 100, 100, 105, 110, 110, 115, 120, 125]},
                    1500: { "C" : highWLSize}}
                    #9999: { "C" : [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0]}}
        
        with open("Tables/Norway_Table.json", "w") as fout:
            json.dump(NLF_Rules, fout, indent=4)
        with open("Tables/Norway_Index.json", "w") as fout:
            json.dump(weight, fout, indent=4)

    if exportBrianG: 
        IndexY = [1,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,499]
        IndexX = [110, 121, 132, 143, 154, 165, 176, 187, 198, 209, 220, 232, 243, 254, 265]
        IndexX = [x/2.20462 for x in IndexX]
        Req = ["Recommended", "Minimum"]
        BG_Table = dict() 

        with open("Tables/BG_Table3.csv", "r", encoding='UTF-8') as fin:
            table = csv.reader(fin, delimiter=",")
            for i, row in enumerate(table):
                jumps = IndexY[int(i/2.0)]
                skill = Req[i%2]
                if jumps in BG_Table.keys():
                    BG_Table[jumps][skill] = row
                else:
                    BG_Table[jumps] = {skill: row}
    
        with open("Tables/Brian_Germain_Table.json", "w") as fout:
            json.dump(BG_Table, fout, indent=4)
        
        with open("Tables/Brian_Germain_Index.json", "w") as fout:
            json.dump(IndexX, fout, indent=4)
        
    if exportSweden: 
        
        IndexX = [50,55,60,65,70,75,80,85,90,95,100,105,110,115,120]
        IndexY = [1,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,600,800,1000]
        
        Req = ["Recommended", "Minimum"]
        BG_Table = dict() 

        with open("Tables/swedish_regulations.csv", "r", encoding='UTF-8-SIG') as fin:
            table = csv.reader(fin, delimiter=",")
            for i, row in enumerate(table):
                row = [abs(int(x)) for x in row]
                jumps = IndexY[int(i/2.0)]
                skill = Req[i%2]
                if jumps in BG_Table.keys():
                    BG_Table[jumps][skill] = row
                else:
                    BG_Table[jumps] = {skill: row}
    
        with open("Tables/Sweden_Table.json", "w") as fout:
            json.dump(BG_Table, fout, indent=4)
        
        with open("Tables/Sweden_Index.json", "w") as fout:
            json.dump(IndexX, fout, indent=4)

    if exportBritish:
        IndexX = [i for i in range(60, 116)]
        IndexY = [99, 299, 399, 599, 799, 999, 1399, 1600, 1800]
    
        keyPairs = [ [99, "A"], [99, "B"] ,
                     [299, "B"], [299, "C"],
                    [300,"Minimum"], 
                    [400,"Minimum"], 
                    [500,"Minimum"], 
                    [800,"Minimum"], 
                    [1000,"Minimum"], 
                    [1200,"Minimum"], 
                    [1400,"Minimum"],
                    [1600,"Minimum"],                  
                    [1800,"Minimum"]]

        with open("Tables/british_regulations.csv", "r", encoding="UTF-8-SIG") as fin:
            importedTable = csv.reader(fin)
            table = dict()
            for i, row in enumerate(importedTable):
                jumps = keyPairs[i][0]
                req = keyPairs[i][1]

                if jumps in table.keys():
                    table[jumps][req] = row
                else:
                    table[jumps] = {req:row}
              
        with open("Tables/British_Table.json", "w") as fout:
            json.dump(table, fout, indent=4)
        with open("Tables/British_Index.json", "w") as fout:
            json.dump(IndexX, fout, indent=4)

    if exportFrench:
        IndexX = [i for i in range(60, 110)]
        IndexY = [99, 249, 399, 599, 799, 999, 1399, 1799, 2000]

        table = dict()

        with open("Tables/french_regulations.csv", "r", encoding="UTF-8-SIG") as fin: 
            importedTable = csv.reader(fin, delimiter=',')
            for i, row in enumerate(importedTable): 
                row = [int(x) for x in row]
                row_x = [int(x*.89) for x in row]
                
                jumps=IndexY[i]
                #table[jumps] = {"Recommended": row} 
                table[jumps] = {"Recommended": row, "Minimum": row_x} 

        with open("Tables/French_Table.json", "w") as fout:
            json.dump(table, fout, indent=4)
        with open("Tables/French_Index.json", "w") as fout:
            json.dump(IndexX, fout, indent=4)

    return True

if __name__ == '__main__':
    main()   


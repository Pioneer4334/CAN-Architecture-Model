# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 11:52:18 2018

@author: Pioneer
"""

import math
import random
from tkinter import *

class CanArch:
    def __init__(self):
        self.hashTable = list()
        self.x0 = 50
        self.y0 = 50
        self.x1 = 950
        self.y1 = 700
        self.win = Tk()
        self.win.title("Can Architecture")
        self.win.state('zoomed')
        
        #Row 0
        indexFrame = Frame(self.win)
        indexFrame.grid(row=0, column=0)
        indexCanvas = Canvas(indexFrame, bg='white', width=700, height=30)
        indexCanvas.pack()
        ix = 60
        indexCanvas.create_text(30, 18, text="Index: ", font=('Helvetica', 10, 'bold'))
        indexCanvas.create_oval(ix+100, 10, ix+115, 25, fill="yellow", width=2)
        indexCanvas.create_text(ix+159, 18, text=": Active Node", font=('Helvetica', 10, 'bold'))
        self.addNode = Button(self.win, text="Add Node", command=self.AddNode)
        self.addNode.grid(row=0, column=1, sticky=W)
        
        #Row 1
        Label(text="Input node ID to delete the node then press enter").grid(row=1, column=0, sticky=E)
        delFrame = Frame(self.win)
        self.deleteKey = Text(delFrame, height=1, width=5)
        self.deleteKey.bind("<Return>", self.DeleteNode)
        self.lblDelWarning = Label(delFrame, fg="red")
        delFrame.grid(row=1, column=1, sticky="nsew")
        self.deleteKey.pack(side="left")
        self.lblDelWarning.pack(side="left")
        
        #Row 3
        self.canvas = Canvas(self.win, width=950, height=800)
        self.canvas.grid(row=3, columnspan=2)
        
        self.Can()
    #---------------------------------------------------------------------------------------------------------------
    
    def ResetWarning(self):
        self.lblDelWarning.config(text="")
    #---------------------------------------------------------------------------------------------------------------
    
    def CheckBoundary(self, lstNodes, totalDist):
        try:
            ld = 0
            for selN in lstNodes:
                ld += abs(selN[1])
            return abs(totalDist) == ld, ld
        except Exception as ex:
            raise ex
    #---------------------------------------------------------------------------------------------------------------
                               
    def FindBoundary(self, rowIndex, x, y):
        xOld = self.hashTable[rowIndex]["xy"][0]
        yOld = self.hashTable[rowIndex]["xy"][1]
        midpoint = ((xOld+x)/2, (yOld+y)/2)
        cc1, cc2 = None, None
        lc1, lc2 = None, None
        if abs(xOld - midpoint[0]) > abs(yOld - midpoint[1]):
            if midpoint[0] < x:
                cc1 = (midpoint[0], self.hashTable[rowIndex]["cc1"][1])
                cc2 = (self.hashTable[rowIndex]["cc2"][0], self.hashTable[rowIndex]["cc2"][1])
                self.hashTable[rowIndex]["cc2"] = (midpoint[0], self.hashTable[rowIndex]["cc2"][1])
            else:
                cc1 = (self.hashTable[rowIndex]["cc1"][0], self.hashTable[rowIndex]["cc1"][1])
                cc2 = (midpoint[0], self.hashTable[rowIndex]["cc2"][1])
                self.hashTable[rowIndex]["cc1"] = (midpoint[0], self.hashTable[rowIndex]["cc1"][1])
            lc1 = (midpoint[0],  self.hashTable[rowIndex]["cc1"][1])
            lc2 = (midpoint[0], self.hashTable[rowIndex]["cc2"][1])
        else:
            if midpoint[1] < y:
                cc1 = (self.hashTable[rowIndex]["cc1"][0], midpoint[1])
                cc2 = (self.hashTable[rowIndex]["cc2"][0], self.hashTable[rowIndex]["cc2"][1])
                self.hashTable[rowIndex]["cc2"] = (self.hashTable[rowIndex]["cc2"][0], midpoint[1])
            else:
                cc1 = (self.hashTable[rowIndex]["cc1"][0], self.hashTable[rowIndex]["cc1"][1])
                cc2 = (self.hashTable[rowIndex]["cc2"][0], midpoint[1])
                self.hashTable[rowIndex]["cc1"] = (self.hashTable[rowIndex]["cc1"][0], midpoint[1])
            lc1 = (self.hashTable[rowIndex]["cc1"][0], midpoint[1])
            lc2 = (self.hashTable[rowIndex]["cc2"][0], midpoint[1])
        
        self.hashTable[rowIndex]["lc1"] = lc1
        self.hashTable[rowIndex]["lc2"] = lc2
        self.canvas.create_line(lc1[0], lc1[1], lc2[0], lc2[1])
        return cc1, cc2, lc1, lc2
    #---------------------------------------------------------------------------------------------------------------
    
    def DeleteNode(self, event):
         d = self.deleteKey.get("1.0", END)
         self.deleteKey.delete('1.0', END)
         try:
             d=int(d)
             self.ResetWarning()
             indexList = [ind for ind, ht in enumerate(self.hashTable) if d == int(ht["NodeID"])]
             if len(indexList) > 0:
                xy = self.hashTable[indexList[0]]["xy"]
                cc1 = self.hashTable[indexList[0]]["cc1"]
                cc2 = self.hashTable[indexList[0]]["cc2"]
                flag = False
                self.canvas.create_oval(xy[0]-7, xy[1]-7, xy[0]+7, xy[1]+7, fill="#F0F0F0", outline="#F0F0F0")
                b = list()
                b.append({"x": cc1[0], "y1": cc1[1], "y2": cc2[1]})
                b.append({"x1": cc1[0], "x2": cc2[0], "y": cc1[1]})
                b.append({"x": cc2[0], "y1": cc1[1], "y2": cc2[1]})
                b.append({"x1": cc1[0], "x2": cc2[0], "y": cc2[1]})
                for j in range(0, len(b)):
                    if j == 0:
                        lstSelectedNodes = [(ht_i, n["cc2"][1]-n["cc1"][1]) for ht_i, n in enumerate(self.hashTable) if n["cc2"][0] == b[j]["x"] and n["cc1"][1] >= b[j]["y1"] and n["cc2"][1] <= b[j]["y2"]]
                        td = b[j]["y2"]-b[j]["y1"]
                        flag, ld = self.CheckBoundary(lstSelectedNodes, td)
                        if(flag):
                            self.canvas.create_line(b[j]["x"], b[j]["y1"], b[j]["x"], b[j]["y2"], fill="#F0F0F0")
                            if len(lstSelectedNodes) > 1:
                                for lsn in lstSelectedNodes:
                                    ht_i = lsn[0]
                                    l_selN = self.hashTable[ht_i]
                                    self.canvas.create_line(l_selN["cc2"][0], l_selN["cc2"][1], cc2[0], l_selN["cc2"][1])
                                    self.hashTable[ht_i]["cc2"] = (cc2[0], l_selN["cc2"][1])
                            else:
                                ht_i = lstSelectedNodes[0][0]
                                l_selN = self.hashTable[ht_i]
                                self.hashTable[ht_i]["cc2"] = (cc2[0], l_selN["cc2"][1])
                            break 
                    elif j == 1:
                        lstSelectedNodes = [(ht_i, n["cc2"][0]-n["cc1"][0]) for ht_i, n in enumerate(self.hashTable) if n["cc2"][1] == b[j]["y"] and n["cc1"][0] >= b[j]["x1"] and n["cc2"][0] <= b[j]["x2"]]
                        td = b[j]["x2"]-b[j]["x1"]
                        flag, ld = self.CheckBoundary(lstSelectedNodes, td)
                        if(flag):
                            self.canvas.create_line(b[j]["x1"], b[j]["y"], b[j]["x2"], b[j]["y"], fill="#F0F0F0")
                            if len(lstSelectedNodes) > 1:
                                for lsn in lstSelectedNodes:
                                    ht_i = lsn[0]
                                    l_selN = self.hashTable[ht_i]
                                    self.canvas.create_line(l_selN["cc2"][0], l_selN["cc2"][1], l_selN["cc2"][0], cc2[1])
                                    self.hashTable[ht_i]["cc2"] = (l_selN["cc2"][0], cc2[1])
                            else:
                                ht_i = lstSelectedNodes[0][0]
                                l_selN = self.hashTable[ht_i]
                                self.hashTable[ht_i]["cc2"] = (l_selN["cc2"][0], cc2[1])
                            break
                    elif j == 2:
                        lstSelectedNodes = [(ht_i, n["cc2"][1]-n["cc1"][1]) for ht_i, n in enumerate(self.hashTable) if n["cc1"][0] == b[j]["x"] and n["cc1"][1] >= b[j]["y1"] and n["cc2"][1] <= b[j]["y2"]]
                        td = b[j]["y2"]-b[j]["y1"]
                        flag, ld = self.CheckBoundary(lstSelectedNodes, td)
                        if(flag):
                            self.canvas.create_line(b[j]["x"], b[j]["y1"], b[j]["x"], b[j]["y2"], fill="#F0F0F0")
                            if len(lstSelectedNodes) > 1:
                                for lsn in lstSelectedNodes:
                                    ht_i = lsn[0]
                                    l_selN = self.hashTable[ht_i]
                                    self.canvas.create_line(cc1[0], l_selN["cc2"][1], l_selN["cc2"][0], l_selN["cc2"][1])
                                    self.hashTable[ht_i]["cc1"] = (cc1[0], l_selN["cc1"][1])
                            else:
                                ht_i = lstSelectedNodes[0][0]
                                l_selN = self.hashTable[ht_i]
                                self.hashTable[ht_i]["cc1"] = (cc1[0], l_selN["cc1"][1])
                            break
                    else:
                        lstSelectedNodes = [(ht_i, n["cc2"][0]-n["cc1"][0]) for ht_i, n in enumerate(self.hashTable) if n["cc1"][1] == b[j]["y"] and n["cc1"][0] >= b[j]["x1"] and n["cc2"][0] <= b[j]["x2"]]
                        td = b[j]["x2"]-b[j]["x1"]
                        flag, ld = self.CheckBoundary(lstSelectedNodes, td)
                        if(flag):
                            self.canvas.create_line(b[j]["x1"], b[j]["y"], b[j]["x2"], b[j]["y"], fill="#F0F0F0")
                            if len(lstSelectedNodes) > 1:
                                for lsn in lstSelectedNodes:
                                    ht_i = lsn[0]
                                    l_selN = self.hashTable[ht_i]
                                    self.canvas.create_line(l_selN["cc2"][0], cc1[1], l_selN["cc2"][0], l_selN["cc1"][1])
                                    self.hashTable[ht_i]["cc1"] = (l_selN["cc1"][0], cc1[1])
                            else:
                                ht_i = lstSelectedNodes[0][0]
                                l_selN = self.hashTable[ht_i]
                                self.hashTable[ht_i]["cc1"] = (l_selN["cc1"][0], cc1[1])
                            break
                self.hashTable.pop(indexList[0]) 
             else:
                 self.lblDelWarning.config(text="The input key is not a node.")
         except Exception as ex:
             print(ex)
             self.lblDelWarning.config(text="Please input integer value only")
    #---------------------------------------------------------------------------------------------------------------
    
    def AddNode(self):
        flagCollision = True
        flagBreakFor = False
        txt = 1
        selectedRowIndex = None
        lc1, lc2 = None, None
        while flagCollision or (len(self.hashTable) > 0 and selectedRowIndex is None):
            x = random.randint(70, 930)
            y = random.randint(70, 680)
            flagCollision = False
            selectedRowIndex = None
            for i, dictInfo in enumerate(self.hashTable):
                xy = dictInfo["xy"]
                lc1 = dictInfo["lc1"]
                lc2 = dictInfo["lc2"]
                if lc1 is not None and lc2 is not None:
                    if lc1[0] == lc2[0] and abs(x-lc1[0]) < 20:
                        flagCollision = True
                        flagBreakFor = True
                    elif lc1[1] == lc2[1] and abs(y-lc1[1]) < 20:
                        flagCollision = True
                        flagBreakFor = True
                if flagBreakFor:
                    flagCollision = True
                    flagBreakFor = False
                    break
                dist = math.sqrt((xy[0]-x)**2+(xy[1]-y)**2)
                if (dist <= 25):
                    flagCollision = True
                    break
                else:
                    if dictInfo["cc1"][0] < x and dictInfo["cc2"][0] > x and dictInfo["cc1"][1] < y and dictInfo["cc2"][1] > y:
                        selectedRowIndex = i        
        
        self.canvas.create_oval(x-7, y-7, x+7, y+7, fill="yellow")
        
        if len(self.hashTable) > 0:
            txt = int(self.hashTable[-1]["NodeID"]) + 1
            cc1, cc2, lc1, lc2 = self.FindBoundary(selectedRowIndex, x, y)
        else:
            cc1 = (self.x0, self.y0)
            cc2 = (self.x1, self.y1)
        
        self.hashTable.append({"NodeID": txt, "xy": (x, y), "cc1": cc1, "cc2": cc2, "lc1": lc1, "lc2": lc2});
        self.canvas.create_text(x,y,text=txt)
    #---------------------------------------------------------------------------------------------------------------
        
    def Can(self):
        # Draw Main Circle in Canvas
        self.canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1)
        self.AddNode()
        self.win.mainloop()
    #---------------------------------------------------------------------------------------------------------------

CanArch()
    
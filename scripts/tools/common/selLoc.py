## -*- coding: utf-8 -*-
import maya.cmds as cmds
from mods.common.smartBake import smartBake
from mods.common.delConst import delConst


#選択したものに対して、様々なロケータを作成するクラス

#使用例
#import tools.common.selLoc as selLoc
#selLoc = selLoc.selLoc()
#selLoc.cnst("long")
#selLoc.bake("short")
#selLoc.lock("short")
#selLoc.add("long")

class selLoc():
    def __init__(self):
        True
    #コンスト付きでロケータを作成
    def cnst(self,type='short'):
        sel = []
        self.type = type
        LocArray = []
        if self.type == "long":
            sel = cmds.ls(sl=1,l=1)
        elif self.type == "short":
            sel = cmds.ls(sl=1)
        for work in sel:
            loc = cmds.spaceLocator(n=work+"_loc#")[0]
            cmds.select(work,loc)
            cnst = cmds.parentConstraint()
            cmds.select(loc)
            LocArray.append(loc)
        cmds.select(sel)
        return LocArray
    #コンスト付きでロケータを作成
    def bake(self,type='short'):
        sel = []
        self.type = type
        LocArray = []
        if self.type == "long":
            sel = cmds.ls(sl=1,l=1)
        elif self.type == "short":
            sel = cmds.ls(sl=1)
        for work in sel:
            loc = cmds.spaceLocator(n=work+"_loc#")[0]
            cmds.select(work,loc)
            cnst = cmds.parentConstraint()
            cmds.select(loc)
            LocArray.append(loc)
        cmds.select(LocArray)
        smartBake()
        delConst()
        cmds.select(sel)
        return LocArray
    #ロケータで逆コンストする
    def lock(self,type='short',bake=True):
        sel = []
        self.type = type
        
        if self.type == "long":
            sel = cmds.ls(sl=1,l=1)
        elif self.type == "short":
            sel = cmds.ls(sl=1)
        
        #変数の初期化
        LocArray = []
        CnstArray = []
        
        #選択したノードをループ処理
        for work in sel:
            #選択したノード名の末尾に_locを付けてロケータを作成
            loc = cmds.spaceLocator(n=work+"_loc#")[0]
            LocArray.append(cmds.ls(sl=1,l=1)[0])
            #コンストレインを行う
            cmds.select(work,loc)
            cnst = cmds.parentConstraint()[0]
            CnstArray.append(cnst)
        
        cmds.select(LocArray)
        if bake:
            smartBake()
        delConst()
        
        for i in range(len(LocArray)):
            #ポイントコンストレインを行う。この時処理が実行されなかったら、処理をスルーする
            try:
               cmds.pointConstraint(LocArray[i],sel[i])
            except:
               print "do not point constrain"
            #オリエントコンストレインを行う。この時処理が実行されなかったら、処理をスルーする
            try:
               cmds.orientConstraint(LocArray[i],sel[i])
            except:
               cmds.warning("do not orient constrain")
        cmds.select(sel)
        return LocArray
    
    def tempPivot(self,type='short',bake=True):
        sel = []
        self.type = type
        
        if self.type == "long":
            sel = cmds.ls(sl=1,l=1)
        elif self.type == "short":
            sel = cmds.ls(sl=1)
        
        #変数の初期化
        PivotArray = []
        LocArray = []
        CnstArray = []
        
        #選択したノードをループ処理
        for work in sel:
            #選択したノード名の末尾に_locを付けてロケータを作成
            pivot = cmds.createNode('transform',n='custompivot#')
            loc = cmds.spaceLocator(n=work+"_loc#")[0]
            cmds.parent(loc,pivot)

            PivotArray.append(pivot)
            LocArray.append(loc)
            #コンストレインを行う
            cmds.select(work,pivot)
            cnst = cmds.parentConstraint()[0]
            CnstArray.append(cnst)
        
        cmds.select(PivotArray)
        if bake:
            smartBake()
        delConst()
        
        for i in range(len(LocArray)):
            #ポイントコンストレインを行う。この時処理が実行されなかったら、処理をスルーする
            try:
               cmds.pointConstraint(LocArray[i],sel[i])
            except:
               print "do not point constrain"
            #オリエントコンストレインを行う。この時処理が実行されなかったら、処理をスルーする
            try:
               cmds.orientConstraint(LocArray[i],sel[i])
            except:
               cmds.warning("do not orient constrain")
        cmds.select(sel)
        return LocArray
        
    #選択したノードの位置にロケータを作成する
    def add(self,type='short'):
        sel = []
        self.type = type
        LockArray = []
        if self.type == "long":
            sel = cmds.ls(sl=1,l=1)
        elif self.type == "short":
            sel = cmds.ls(sl=1)
        for work in sel:
            if work.find("|") != -1:
                shortName = work.split("|")[-1]
            loc = cmds.spaceLocator(n=work+"_loc#")[0]
            cmds.select(work,loc)
            cnst = cmds.parentConstraint()
            cmds.select(loc)
            cmds.delete(cnst)
            LockArray.append(loc)
        cmds.select(sel)
        return LockArray
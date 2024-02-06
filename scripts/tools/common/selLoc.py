## -*- coding: utf-8 -*-
import maya.cmds as cmds
from mods.common.smartBake import smartBake
from mods.common.delConst import delConst


#�I���������̂ɑ΂��āA�l�X�ȃ��P�[�^���쐬����N���X

#�g�p��
#import tools.common.selLoc as selLoc
#selLoc = selLoc.selLoc()
#selLoc.cnst("long")
#selLoc.bake("short")
#selLoc.lock("short")
#selLoc.add("long")

class selLoc():
    def __init__(self):
        True
    #�R���X�g�t���Ń��P�[�^���쐬
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
    #�R���X�g�t���Ń��P�[�^���쐬
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
    #���P�[�^�ŋt�R���X�g����
    def lock(self,type='short',bake=True):
        sel = []
        self.type = type
        
        if self.type == "long":
            sel = cmds.ls(sl=1,l=1)
        elif self.type == "short":
            sel = cmds.ls(sl=1)
        
        #�ϐ��̏�����
        LocArray = []
        CnstArray = []
        
        #�I�������m�[�h�����[�v����
        for work in sel:
            #�I�������m�[�h���̖�����_loc��t���ă��P�[�^���쐬
            loc = cmds.spaceLocator(n=work+"_loc#")[0]
            LocArray.append(cmds.ls(sl=1,l=1)[0])
            #�R���X�g���C�����s��
            cmds.select(work,loc)
            cnst = cmds.parentConstraint()[0]
            CnstArray.append(cnst)
        
        cmds.select(LocArray)
        if bake:
            smartBake()
        delConst()
        
        for i in range(len(LocArray)):
            #�|�C���g�R���X�g���C�����s���B���̎����������s����Ȃ�������A�������X���[����
            try:
               cmds.pointConstraint(LocArray[i],sel[i])
            except:
               print "do not point constrain"
            #�I���G���g�R���X�g���C�����s���B���̎����������s����Ȃ�������A�������X���[����
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
        
        #�ϐ��̏�����
        PivotArray = []
        LocArray = []
        CnstArray = []
        
        #�I�������m�[�h�����[�v����
        for work in sel:
            #�I�������m�[�h���̖�����_loc��t���ă��P�[�^���쐬
            pivot = cmds.createNode('transform',n='custompivot#')
            loc = cmds.spaceLocator(n=work+"_loc#")[0]
            cmds.parent(loc,pivot)

            PivotArray.append(pivot)
            LocArray.append(loc)
            #�R���X�g���C�����s��
            cmds.select(work,pivot)
            cnst = cmds.parentConstraint()[0]
            CnstArray.append(cnst)
        
        cmds.select(PivotArray)
        if bake:
            smartBake()
        delConst()
        
        for i in range(len(LocArray)):
            #�|�C���g�R���X�g���C�����s���B���̎����������s����Ȃ�������A�������X���[����
            try:
               cmds.pointConstraint(LocArray[i],sel[i])
            except:
               print "do not point constrain"
            #�I���G���g�R���X�g���C�����s���B���̎����������s����Ȃ�������A�������X���[����
            try:
               cmds.orientConstraint(LocArray[i],sel[i])
            except:
               cmds.warning("do not orient constrain")
        cmds.select(sel)
        return LocArray
        
    #�I�������m�[�h�̈ʒu�Ƀ��P�[�^���쐬����
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
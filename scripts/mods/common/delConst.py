## -*- coding: utf-8 -*-
import maya.cmds as cmds

def delConst():
    for sel in cmds.ls(sl=1,fl=1,l=1):
        if cmds.objExists(sel):
            childList = cmds.listRelatives(sel,c=1,f=1)
            if childList != None:
                for child in cmds.listRelatives(sel,c=1,f=1):
                    type = cmds.objectType(child)
                    if type.find("Constraint") > 0:
                        cmds.delete(child)
            else:
                print("noting constraint\r")
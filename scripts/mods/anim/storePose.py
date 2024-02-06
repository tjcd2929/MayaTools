## -*- coding:utf-8 -*-
import maya.cmds as cmds

#ポーズを返す関数
def main(mode='shelf'):
    AttrCmd = ''
    for work in cmds.ls(sl=1):
        AttrList = cmds.listAttr(work,k=1,u=1,se=1)
        userDifineAttr = cmds.listAttr(work,ud=1,u=1,se=1)
        if userDifineAttr != None and AttrList != None:
            AttrList = AttrList+userDifineAttr
        if AttrList != None:
            for Attr in AttrList:
                if cmds.objExists(work+"."+Attr):
                    AttrType = cmds.getAttr(work+'.'+Attr,type=1)
                    if Attr != "translate" and Attr != "rotate" and Attr != "scale" :
                        if AttrType != 'message' and AttrType != 'string' and AttrType != 'matrix':
                            AttrValue = cmds.getAttr(work+"."+Attr)
                            if AttrValue == True:
                                AttrValue = 'true'
                            if AttrValue == False:
                                AttrValue = 'false'
                            if mode == 'shelf':
                                AttrCmd += ('catch(`setAttr \\"'+work+'.'+Attr+'\\" '+str(AttrValue)+'`);\\r')
                            elif mode == 'cmd':
                                AttrCmd += ('catch(`setAttr "'+work+'.'+Attr+'" '+str(AttrValue)+'`);')
    return AttrCmd
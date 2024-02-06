#-*- coding:utf-8 -*-
import maya.cmds as cmds

class smartReset():
    def __init__(self):
        True
    
    def resetT(self,node):
        cmds.setAttr(node+'.t',0,0,0)
    
    def resetR(self,node):
        cmds.setAttr(node+'.r',0,0,0)
    
    def resetS(self,node):
        cmds.setAttr(node+'.s',1,1,1)
    
    def resetAll(self,node):
        self.resetT(node)
        self.resetR(node)
        self.resetS(node)
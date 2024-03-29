# -*- coding:utf-8 -*-
import maya.cmds as cmds

"""
import mods.common.smartBake_TEST
reload(mods.common.smartBake_TEST)
from mods.common.smartBake_TEST import smartBake_TEST
"""

import mods.anim.revCnst
reload(mods.anim.revCnst)
from mods.anim.revCnst import *

width = 170
if cmds.window("revCnstWindow",ex=1) == 1:
    cmds.deleteUI("revCnstWindow")
cmds.window("revCnstWindow",t="revCnst_Window",w=width)
cmds.columnLayout(w=width)
cmds.optionMenu("revCnstRotateOrder",l="rotateOrder",w=width)
cmds.menuItem(p="revCnstRotateOrder",label="xyz")
cmds.menuItem(p="revCnstRotateOrder",label="yzx")
cmds.menuItem(p="revCnstRotateOrder",label="zxy")
cmds.menuItem(p="revCnstRotateOrder",label="xzy")
cmds.menuItem(p="revCnstRotateOrder",label="yxz")
cmds.menuItem(p="revCnstRotateOrder",label="zyx")
cmds.checkBox("revCnstSimMode",l="Do simlation?",v=1)
cmds.checkBox("revCnstSingleFrame",l="single frame",v=0)
cmds.button(l="run",w=width,c="revCnst(cmds.optionMenu(\"revCnstRotateOrder\",q=1,sl=1)-1,cmds.checkBox(\"revCnstSimMode\",q=1,v=1),singleFrame=cmds.checkBox('revCnstSingleFrame',q=1,v=1))")
cmds.showWindow("revCnstWindow")

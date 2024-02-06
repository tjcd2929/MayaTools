# -*- coding:utf-8 -*-
'''
import maya.OpenMaya as om
import maya.cmds as cmds

class microTransform:
    def __init__(self, node, attribute, multiplier=1.0):
        self.node = node
        self.attribute = attribute
        self.multiplier = multiplier
        self.prev_value = cmds.getAttr("%s.%s" % (node, attribute))
        
        # Timer関連の変数を追加
        self.microTransformStartTimer = None

        # CallbackのIDを保存しておく変数を追加
        self.callback_id = None

    def attribute_changed(self, msg, plug, other_plug, clientData):
        if om.MNodeMessage.kAttributeSet == (om.MNodeMessage.kAttributeSet & msg):
            # Callbackを一時的に無効にする
            self.remove_callback()
            
            nodeAttr = "%s.%s" % (self.node, self.attribute)
            val = cmds.getAttr(nodeAttr)

            # Timerの計算
            if self.microTransformStartTimer is None:
                self.microTransformStartTimer = cmds.timerX()
            
            microTransformTimer = cmds.timerX(startTime=self.microTransformStartTimer)
            self.microTransformStartTimer = cmds.timerX()

            microTransformTimer *= 50
            if microTransformTimer == 0: microTransformTimer = 1000
            mult = self.multiplier / microTransformTimer

            if mult >= self.multiplier: mult = self.multiplier

            # 値の変更
            diff = val - self.prev_value
            new_val = self.prev_value + diff * mult
            cmds.setAttr(nodeAttr, new_val)

            # 以前の値の更新
            self.prev_value = new_val

            # Callbackを再度有効にする
            self.add_callback()

    def add_callback(self):
        selectionList = om.MSelectionList()
        om.MGlobal.getSelectionListByName(self.node, selectionList)
        mobj = om.MObject()
        selectionList.getDependNode(0, mobj)
        self.callback_id = om.MNodeMessage.addAttributeChangedCallback(mobj, self.attribute_changed)

    def remove_callback(self):
        if self.callback_id:
            om.MMessage.removeCallback(self.callback_id)
            self.callback_id = None

modX = microTransform('pCube1','translateX',0.1)
modY = microTransform('pCube1','translateY',0.1)
modZ = microTransform('pCube1','translateZ',0.1)
modX.add_callback()
modY.add_callback()
modZ.add_callback()

modX.remove_callback()
modY.remove_callback()
modZ.remove_callback()
'''

'''
import maya.OpenMaya as om
import maya.cmds as cmds

class microTransform:
    def __init__(self, node, multiplier=1.0):
        self.node = node
        self.multiplier = multiplier

        # すべての属性の前の値を初期化
        self.prev_values = {
            "translateX": cmds.getAttr("%s.translateX" % node),
            "translateY": cmds.getAttr("%s.translateY" % node),
            "translateZ": cmds.getAttr("%s.translateZ" % node),
            "rotateX": cmds.getAttr("%s.rotateX" % node),
            "rotateY": cmds.getAttr("%s.rotateY" % node),
            "rotateZ": cmds.getAttr("%s.rotateZ" % node),
            "scaleX": cmds.getAttr("%s.scaleX" % node),
            "scaleY": cmds.getAttr("%s.scaleY" % node),
            "scaleZ": cmds.getAttr("%s.scaleZ" % node),
        }
        
        # Timer関連の変数を追加
        self.microTransformStartTimer = None

        # CallbackのIDを保存しておく変数を追加
        self.callback_id = None

    def attribute_changed(self, msg, plug, other_plug, clientData):
        if om.MNodeMessage.kAttributeSet == (om.MNodeMessage.kAttributeSet & msg):
            # Callbackを一時的に無効にする
            self.remove_callback()
            
            changed_attr = plug.partialName()
            if changed_attr in self.prev_values.keys():
                val = cmds.getAttr("%s.%s" % (self.node, changed_attr))
                # Timerの計算
                if self.microTransformStartTimer is None:
                    self.microTransformStartTimer = cmds.timerX()
                
                microTransformTimer = cmds.timerX(startTime=self.microTransformStartTimer)
                self.microTransformStartTimer = cmds.timerX()

                microTransformTimer *= 50
                if microTransformTimer == 0: microTransformTimer = 1000
                mult = self.multiplier / microTransformTimer

                if mult >= self.multiplier: mult = self.multiplier

                # 値の変更
                diff = val - self.prev_values[changed_attr]
                new_val = self.prev_values[changed_attr] + diff * mult
                cmds.setAttr("%s.%s" % (self.node, changed_attr), new_val)
                # 以前の値の更新
                self.prev_values[changed_attr] = new_val

            # Callbackを再度有効にする
            self.add_callback()

    def add_callback(self):
        selectionList = om.MSelectionList()
        om.MGlobal.getSelectionListByName(self.node, selectionList)
        mobj = om.MObject()
        selectionList.getDependNode(0, mobj)
        self.callback_id = om.MNodeMessage.addAttributeChangedCallback(mobj, self.attribute_changed)

    def remove_callback(self):
        if self.callback_id:
            om.MMessage.removeCallback(self.callback_id)
            self.callback_id = None

# 使用例
mod = microTransform('pCube1', multiplier=0.1)
mod.add_callback()

'''


import maya.OpenMaya as om
import maya.cmds as cmds

class microTransform:
    def __init__(self, node, attribute, multiplier=1.0):
        self.node = node
        self.attribute = attribute
        self.multiplier = multiplier
        self.prev_value = cmds.getAttr("%s.%s" % (node, attribute))

        # CallbackのIDを保存しておく変数を追加
        self.callback_id = None

    def attribute_changed(self, msg, plug, other_plug, clientData):
        if om.MNodeMessage.kAttributeSet == (om.MNodeMessage.kAttributeSet & msg):
            # Callbackを一時的に無効にする
            self.remove_callback()
            
            nodeAttr = "%s.%s" % (self.node, self.attribute)
            val = cmds.getAttr(nodeAttr)

            # 値の変更
            diff = val - self.prev_value
            new_val = self.prev_value + diff * self.multiplier
            cmds.setAttr(nodeAttr, new_val)

            # 以前の値の更新
            self.prev_value = new_val

            # Callbackを再度有効にする
            self.add_callback()

    def add_callback(self):
        selectionList = om.MSelectionList()
        om.MGlobal.getSelectionListByName(self.node, selectionList)
        mobj = om.MObject()
        selectionList.getDependNode(0, mobj)
        self.callback_id = om.MNodeMessage.addAttributeChangedCallback(mobj, self.attribute_changed)

    def remove_callback(self):
        if self.callback_id:
            om.MMessage.removeCallback(self.callback_id)
            self.callback_id = None
    
    def switch(self):
        if self.callback_id == None:
            self.prev_value = cmds.getAttr("%s.%s" % (self.node, self.attribute))
            self.add_callback()
        else:
            self.remove_callback()

'''
#how to use
sel = cmds.ls(sl=1)[0]
modTX = microTransform(sel,'translateX',0.1)
modTY = microTransform(sel,'translateY',0.1)
modTZ = microTransform(sel,'translateZ',0.1)

modTX.switch()
modTY.switch()
modTZ.switch()
'''

'''
#how to use 2
import mods.anim.microTransform
reload(mods.anim.microTransform)

sel = cmds.ls(sl=1)[0]
modTX = mods.anim.microTransform.microTransform(sel,'translateX',0.1)
modTY = mods.anim.microTransform.microTransform(sel,'translateY',0.1)
modTZ = mods.anim.microTransform.microTransform(sel,'translateZ',0.1)

modTX.switch()
modTY.switch()
modTZ.switch()
'''

'''
メモ
ScriptJobで選択が変更されたらmicroTransformを破棄、新たに選択されたノードで処理
という風にする。（複数処理はどうしているのか？）
'''
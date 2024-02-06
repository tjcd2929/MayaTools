## -*- coding: utf-8 -*-
import maya.cmds as cmds
import sys

def smartBake(bakeMode="allKey",
              start=0,
              end=1,
              viewportOff=False):
    
    #関数が実行されたのをプリント文で出力
    print "start : --- "+sys._getframe().f_code.co_name+" --- \n",
    
    #スタートとエンドのフレームを取得
    if bakeMode == "allKey":
        start = cmds.playbackOptions(q=1,min=1)
        end = cmds.playbackOptions(q=1,max=1)
    
    selArray = cmds.ls(sl=1,l=1)
    
    if viewportOff:
        #アクティブなパネルを取得
        WfPanel = cmds.getPanel(wf=1)
        WfPanelType = cmds.getPanel(to=WfPanel)
        #isolate selectionモードにして処理の負荷を低減させる
        if WfPanelType == "modelPanel":
            cmds.select(cl=1)
            cmds.isolateSelect(WfPanel,state=1)
    
    #ベイク処理を行う
    if bakeMode == "allKey":
        cmds.bakeResults(selArray,simulation=1,pok=1,t=(start,end))
    elif bakeMode == "inFrame":
        #スタートとエンドのフレームを取得
        start = cmds.playbackOptions(q=1,min=1)
        end = cmds.playbackOptions(q=1,max=1)
        cmds.bakeResults(selArray,simulation=1,pok=0,t=(start,end))
    else:
        cmds.bakeResults(selArray,simulation=1,pok=1,t=(start,end))
    cmds.filterCurve()

    if viewportOff:
        #ビューの表示を元に戻す
        if WfPanelType == "modelPanel":
            cmds.isolateSelect(WfPanel,state=0)
    
    cmds.select(selArray)
    
    #関数が終了したのをプリント文で出力
    print "end : --- "+sys._getframe().f_code.co_name+" --- \n",
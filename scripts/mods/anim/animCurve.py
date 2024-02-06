## -*- coding:utf-8 -*-
import maya.cmds as cmds
import tween_machine

def getAnimCurves():
    return cmds.keyframe(q=1,sl=1,n=1)

def getFrames():
    cmds.keyframe(q=1,timeChange=1)
    frames = cmds.keyframe(q=1)
    frames = sorted( list(set(frames)) )
    return frames

def insertTween(frames=None,
                animCurve=None,
                time1=0.25,
                time2=0.75,
                tween1=0.1,
                tween2=0.9,
                insert1=True,
                insert2=True,
                cleanup=False):
    '''
    2点間のアニメーションキーの間で、カーブにコントラストを付けるキーを挿入する
    '''
    if animCurve == None:
        #animCurveを選択から取得
        animCurve = getAnimCurves()
    if frames == None:
        #選択しているanimCurveのキーのフレーム数を取得
        frames = getFrames()
    if frames != None and len(frames) >= 2:
        #最小フレームと最大フレームを取得
        startFrame = frames[0]
        endFrame   = frames[-1]
        #フレーム間の数字を取得
        dist = endFrame - startFrame
        
        #キーの挿入位置を取得
        insertFrame1 = int( startFrame + ( dist * time1 ) )
        insertFrame2 = int( startFrame + ( dist * time2 ) )
        
        #キーの挿入
        #cmds.setKeyframe(animCurve,time=insertFrame1,insert=1)
        #cmds.setKeyframe(animCurve,time=insertFrame2,insert=1)
        if insert1:
            cmds.currentTime(insertFrame1)
            tween_machine.tween(tween1)
        if insert2:
            cmds.currentTime(insertFrame2)
            tween_machine.tween(tween2)
        
def cleanupAnimCurve():
    '''
    選択したアニメーションカーブ間で、最初と最後以外のキーを削除
    '''
    #animCurveを選択から取得
    animCurve = getAnimCurves()
    #選択しているanimCurveのキーのフレーム数を取得
    frames = getFrames()
    if frames != None and len(frames) >= 2:
        #最小フレームと最大フレームを取得
        startFrame = frames[0]
        endFrame   = frames[-1]
        for frame in frames:
            if frame != startFrame and frame != endFrame:
                cmds.selectKey(animCurve,k=1,t=(frame,frame))
                cmds.cutKey(animation='keys',clear=True)
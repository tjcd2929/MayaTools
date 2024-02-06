# -*- coding:utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel

import mods.common.undo_chanck

class keyframeUtil():
    def __init__(self):
        self.var = cmds.about(version=True)
        mel.eval('source "C:/Program Files/Autodesk/Maya'+self.var+'/scripts/others/buildKeyframeTangentMM.mel";')
    #--------------------------------
    #キーを選択しているかどうかをチェック
    def exSelKey(self):
        if cmds.keyframe(q=1,sl=1):
            return True
        else:
            return False
    #タイムスライダー上にキーがあるかどうかをチェックする
    def exTimeSliderKey(self):
        range = self.getTimeSliderRange()
        if cmds.keyframe(q=1,sl=1) == None:
            selKey = cmds.keyframe(q=1,t=(range[0],range[1]))
            #time slider上にキーがあるか
            if selKey != None:
                return True
            elif selKey == None:
                return False
        else:
            return False
    #タイムスライダー上の状況を元に、フレームレンジを返す関数。
    #ハイライト選択時は、選択したフレームレンジを
    #通常時は、現在フレームのリストを返す
    def getTimeSliderRange(self,mode=1):
        range = []
        if mel.eval('timeControl -query -rangeVisible $gPlayBackSlider;'):
            range = mel.eval('timeControl -query -rangeArray $gPlayBackSlider;')
        else:
            range = [cmds.playbackOptions(q=1,min=1),cmds.playbackOptions(q=1,max=1)]
            if mode == 1:
                ct = cmds.currentTime(q=1)
                range = [ct,ct]
        return range
    #BreakDownKeyがタイムスライダー上にあるかどうか（AnimCurve非対応）
    def getBreakDownState(self,range=[]):
        if len(range) == 2:
            exselKey = self.exSelKey()
            if exselKey == True:
                cmds.selectKey(clear=1)
            breakDownState = cmds.keyframe(q=1,breakdown=1,t=(range[0],range[1]))
            return breakDownState
        else:
            cmds.error('please set range')
    
    #--------------------------------
    #BreakDownKeyをToggle（AnimCurve非対応）
    def toggleBreakDown(self):
        range = self.getTimeSliderRange()
        breakDownState = self.getBreakDownState(range)
        exselKey = self.exSelKey()
        if breakDownState != None:
            cmds.keyframe( breakdown=False,an='objects',iub=False,t=(range[0],range[1]) )
            cmds.keyframe( an='objects',tds=False,iub=False,t=(range[0],range[1]) )
        else:
            cmds.keyframe( breakdown=True,an='objects',iub=False,t=(range[0],range[1]) )
            cmds.keyframe( an='objects',tds=False,iub=False,t=(range[0],range[1]) )
    
    #オフセット(AnimCurve対応)
    def offset(self,v=0):
        range = self.getTimeSliderRange()
        cmd = "keyframe"
        if range[0] == range[1]:
            if self.exSelKey() == False:
                cmd = cmd + "-time \"" + str(cmds.currentTime(q=1)) + ":\" "
        else:
            cmd = cmd + "-time \"" + str(range[0]) + ":" + str(range[1]) + "\" "
        cmd = cmd + "-relative -timeChange " + str(v) + " -option over"
        print(cmd)
        mel.eval(cmd)
    
    #削除(AnimCurve対応)
    def delete(self):
        exselKey = self.exSelKey()
        exTimeSliderKey = self.exTimeSliderKey()
        
        if exselKey:
            cmds.cutKey()
        elif exTimeSliderKey:
            mel.eval('keyOperationFromMM 1')
    
    #コピー（AnimCurve対応）
    def copy(self):
        if self.exSelKey():
            cmds.copyKey()
        else:
            mel.eval('keyOperationFromMM 2')
    
    #カット(AnimCurve対応)
    def cut(self):
        if self.exSelKey():
            cmds.cutKey()
        else:
            mel.eval('keyOperationFromMM 3')
    
    #ペースト（AnimCurve対応）
    def paste(self):
        if self.exSelKey():
            ct = str( cmds.currentTime(q=1) )
            cmd = 'pasteKey -time '+ct+' -float '+ct+' -option merge -copies 1 -connect 0 -timeOffset 0 -floatOffset 0 -valueOffset 0;'
            mel.eval(cmd)
        else:
            mel.eval('pasteKeyFromMM')
    #コピーを実行後、すぐにペーストを実行する
    def copypaste(self):
        if self.exSelKey():
            cmds.copyKey()

            ct = str( cmds.currentTime(q=1) )
            cmd = 'pasteKey -time '+ct+' -float '+ct+' -option merge -copies 1 -connect 0 -timeOffset 0 -floatOffset 0 -valueOffset 0;'
            mel.eval(cmd)
        else:
            mel.eval('keyOperationFromMM 2')
            mel.eval('pasteKeyFromMM')
    
    #小数点の数字を削除（カーブが同様になるようにキーを打つ&なぜか2018.7環境だとタンジェントがBreakされるのでAutoにする）
    def smartRoundKey(self):
        range = self.getTimeSliderRange(mode=0)
        frames = cmds.keyframe(q=1,t=(range[0],range[1]) )
        if frames != None:
            frames = list(set(frames))
            #整数キーに抑えのキーを打つ
            for frame in frames:
                if not frame.is_integer():
                    cmds.currentTime( int(frame) )
                    cmds.setKeyframe(insert=1)
            #小数点のキーを削除
            for frame in frames:
                if not frame.is_integer():
                    cmds.selectKey(t=(frame,frame))
                    cmds.cutKey()
            #打ったキーのタンジェントをautoにする
            for frame in frames:
                if not frame.is_integer():
                    cmds.keyTangent( t=(int(frame),int(frame)),inTangentType='auto',outTangentType='auto' )

class timeSliderUtil():
    def __init__(self):
        self._storeRange = [0,1]
        self.ver = cmds.about(version=1)
        mel.eval('source "C:/Program Files/Autodesk/Maya'+self.ver+'/scripts/others/TimeSliderMenu.mel";')
    #タイムスライダー上の状況を元に、フレームレンジを返す関数。
    #ハイライト選択時は、選択したフレームレンジを
    #通常時は、タイムスライダーのmin maxを返す
    def getTimeSliderRange(self):
        range = []
        if mel.eval('timeControl -query -rangeVisible $gPlayBackSlider;'):
            range = mel.eval('timeControl -query -rangeArray $gPlayBackSlider;')
        else:
            range = [cmds.playbackOptions(q=1,min=1),cmds.playbackOptions(q=1,max=1)]
        return range
    
    def play(self):
        mel.eval('togglePlayback')
    def offset(self,v=0):
        ct  = cmds.currentTime(q=1)
        cmds.currentTime(ct+v)
    def next(self):
        cmds.NextFrame()
    def previous(self):
        cmds.PreviousFrame()
    def setMinTime(self):
        cmds.playbackOptions(min=cmds.currentTime(q=1))
    def setMaxTime(self):
        cmds.playbackOptions(max=cmds.currentTime(q=1))
    def setRange(self):
        if mel.eval('timeControl -query -rangeVisible $gPlayBackSlider;'):
            mel.eval('setPlaybackRangeToHighlight')
        elif cmds.keyframe(q=1,sl=1) != None:
            keys = cmds.keyframe(q=1,sl=1)
            keys = [int(work) for work in keys]
            minFrame = min( keys )
            maxFrame = max( keys )
            cmds.playbackOptions(e=1,min=minFrame)
            cmds.playbackOptions(e=1,max=maxFrame)

            #storeしておいた所とToggle
            #self.temp = [self._storeRange[0],self._storeRange[1]]
            #self._storeRange[0] = cmds.playbackOptions(q=1,min=1)
            #self._storeRange[1] = cmds.playbackOptions(q=1,max=1)
            #cmds.playbackOptions(e=1,min=self.temp[0])
            #cmds.playbackOptions(e=1,max=self.temp[1])
    
    def storeRange(self):
        self._storeRange = self.getTimeSliderRange()
    
    def smartNextKey(self):
        if cmds.keyframe(q=1,sl=1) != None:
            frames = sorted(list(set(cmds.keyframe(q=1,sl=1))))
            firstKey = frames[0]
            endKey = frames[-1]
            
            ct = cmds.currentTime(q=1)
            serchKey = cmds.findKeyframe(animation="keys",which="next")
            
            if serchKey <= ct:
                cmds.currentTime(firstKey)
            else:
                cmds.currentTime(serchKey)
        elif cmds.keyframe(q=1,sl=1) == None:
            serchKey = cmds.findKeyframe(timeSlider=1,which="next")
            cmds.currentTime(serchKey)
        
    def smartPreviousKey(self):
        if cmds.keyframe(q=1,sl=1) != None:
            frames = sorted(list(set(cmds.keyframe(q=1,sl=1))))
            firstKey = frames[0]
            endKey = frames[-1]
            
            ct = cmds.currentTime(q=1)
            serchKey = cmds.findKeyframe(animation="keys",which="previous")
            
            if serchKey >= ct:
                cmds.currentTime(endKey)
            else:
                cmds.currentTime(serchKey)
        elif cmds.keyframe(q=1,sl=1) == None:
            serchKey = cmds.findKeyframe(timeSlider=1,which="previous")
            cmds.currentTime(serchKey)

def toggleEvaluation():
    u'''
    Mayaの評価モードをparallelとDGでトグル切り替えする。
    '''
    if cmds.evaluationManager(q=1,mode=1)[0] == 'off':
        cmds.evaluationManager(mode='parallel')
        print('Evaluation mode changed from DG to parallel')
    elif cmds.evaluationManager(q=1,mode=1)[0] == 'parallel':
        cmds.evaluationManager(mode='off')
        print('Evaluation mode changed from parallel to DG')

def animCurveZeroOffset():
    u'''
    選択しているアニメーションカーブを、0を基準にスタートするように値をオフセットする。
    '''
    for work in cmds.ls(sl=1):
        animCurves = cmds.keyframe(work,sl=1,q=1,n=1)
        if animCurves != None:
            for animCurve in animCurves:
                keys = cmds.keyframe(animCurve,sl=1,q=1,vc=1)
                if keys != None:
                    offset = keys[0] * -1
                    cmds.keyframe(animCurve,e=1,iub=True,r=1,o='over',vc=offset)

def smartFitFrame():
    u'''
    GraphEditorのフィットをトグルする。
    FrameSelectionコマンドのデフォの仕様が、
    選択していない時に全体表示しちゃうのがちょっとNGだったため（長尺やってる時は特に･･･）
    '''
    if cmds.keyframe(q=1,sl=1) != None:
        cmds.FrameSelected()
    else:
        mel.eval('animView -startTime (`playbackOptions -query -minTime` - 1) -endTime (`playbackOptions -query -maxTime` + 1) graphEditor1GraphEd;')

def forceReflesh():
    u'''
    デフォーム結果がおかしい場合、ノードの評価を強制的に再度評価させる。
    '''
    cmds.dgdirty(a=True)
    cmds.refresh(force=True)

@symods.other.undo_chanck.undo_chunk
def bakeSetkeyframe(nodes=None,start_frame=None,end_frame=None):
    u'''
    bakeSimulationだと何か変になっちゃうときの強制アニメーションベイク（setKeyframeを指定範囲でやっているだけ）
    '''
    if nodes == None:
        nodes = cmds.ls(sl=1,l=1)
    elif type(nodes) == str or type(nodes) == unicode:
        nodes = [nodes]
    
    #nodesが結局Noneなら処理をしない
    if nodes == [] or nodes==None:
        text=u'Nothing is specified for nodes. \nor nothing is selected.\n\nnodes引数にTransformノードを渡して実行、\n或いは、Transformを選択して実行してください。'
        cmds.confirmDialog(m=text,button='OK',title='')
        cmds.error(text)
        return

    if start_frame == None:
        start_frame = cmds.playbackOptions(q=1,min=1)
    if end_frame == None:
        end_frame = cmds.playbackOptions(q=1,max=1)
    
    # プログレスウィンドウの作成
    cmds.progressWindow(
        title='Setting Keyframes',
        progress=0,
        status='Setting Keyframes: 0%',
        isInterruptable=True
    )
    
    # 指定された範囲で1フレームずつ進行
    for frame in range(int(start_frame), int(end_frame) + 1):
        # キャンセルの検出
        if cmds.progressWindow(query=True, isCancelled=True):
            print("Operation cancelled by user.")
            break
    
        # タイムスライダを現在のフレームに設定
        cmds.currentTime(frame)
    
        # 現在のフレームにキーフレームを設定
        cmds.setKeyframe()
        
        # プログレスウィンドウの更新
        progress = 100 * (frame - start_frame) / (end_frame - start_frame)
        cmds.progressWindow(edit=True, progress=progress, status=('Setting Keyframes: %d%%' % progress))
    
    # プログレスウィンドウの終了
    cmds.progressWindow(endProgress=True)
    
    print("Keyframing completed.")

def toggleSets(setsNode=None,trgs=[]):
    u'''
    選択セットの出し入れを行う関数
    '''
    #引数が初期値の場合、選択に基づいて実行
    if setsNode == None or trgs == []:
        sel = cmds.ls(sl=1)
        setsNode = sel[-1]
        trgs = sel[:-1]

    for trg in trgs:
        if cmds.sets(trg,im=setsNode):
            cmds.sets(trg,rm=setsNode)
        else:
            cmds.sets(trg,add=setsNode)

def paste_delayCurve(src=None,trgs=None,delay=5):
    '''
    アニメーションカーブをディレイしてペーストする関数（AnimationLayerだと選択したキーのコピペには非対応）
    #how to use
    paste_delayCurve(delay=10,clear=False)
    '''
    if src == None:
        src = cmds.ls(sl=1)[0]
    elif type(src) == str or type(src) == unicode:
        src = [src]
    if trgs == None:
        trgs = cmds.ls(sl=1)[1:]
    elif type(trgs) == str or type(trgs) == unicode:
        trgs = [trgs]
    
    cmds.select(trgs,d=1)
    
    #get src anim curve
    animCurves = cmds.keyframe(q=1,n=1)
    
    #if clear == true
    #if clear == True:
    #    cmds.select(trgs)
    #    trgsAnimCurves = cmds.keyframe(q=1,n=1)
    #    cmds.delete(trgsAnimCurves)

    if len(cmds.ls(type="animLayer")) <= 1:
        animLayerExits = False
    else:
        animLayerExits = True

    if animLayerExits:
        frames = cmds.keyframe(animCurves[0],q=1,sl=1)
        if frames == None:
            frames = cmds.keyframe(animCurves[0],q=1)
        
        #get min max frame 
        minFrame = min(frames)
        
        #copy keyframe
        cmds.select(src)
        cmds.copyKey()
        
        #paste keyframe
        delayFrame = minFrame+delay
        cmds.currentTime(delayFrame)
        for trg in trgs:
            cmds.select(trg)
            cmds.pasteKey(time=(delayFrame,delayFrame),
                          float=(delayFrame,delayFrame),
                          option='merge',
                          copies=1,
                          connect=0,
                          timeOffset=0,
                          floatOffset=0,
                          valueOffset=0)
            delayFrame = delayFrame+delay
        cmds.select(src,trgs)
    
    #loop animCurve
    for animCurve in animCurves:
        #get animCurve key frames
        frames = cmds.keyframe(animCurve,q=1,sl=1)
        #if not selected animCurve,get animCurve all frames
        if frames == None:
            frames = cmds.keyframe(animCurve,q=1)
        
        #get min max frame 
        minFrame = min(frames)
        maxFrame = max(frames)
        cmds.selectKey(clear=1)
        
        #copy keyframe
        for f in frames:
            cmds.selectKey(animCurve,add=1,k=1,t=(f,f))
        
        cmds.copyKey()
        
        #delay paste
        delayFrame = minFrame+delay
        for trg in trgs:
            cmds.select(trg)
            cmds.pasteKey(time=(delayFrame,delayFrame),
                          float=(delayFrame,delayFrame),
                          option='merge',
                          copies=1,
                          connect=0,
                          timeOffset=0,
                          floatOffset=0,
                          valueOffset=0)
            
            delayFrame = delayFrame+delay
    cmds.select(src,trgs)
    
def getAnimCurves():
    u"""Description
        選択しているノードのアニメーションカーブを取得する関数
    Returns:
        [string]: アニメーションカーブノードのリスト
    """    
    return cmds.keyframe(q=1,n=1)

def getFrames(animCurve):
    u"""Description
        アニメーションカーブのキーフレームを取得する関数
    Args:
        animCurve (string): アニメーションカーブノード
    Returns:
        [float]: アニメーションカーブにあるキーのフレームのリスト
    """    
    return cmds.keyframe(animCurve,q=1)

def offsetKeyframe(offsetFrame):
    u"""Description
        キーフレームをオフセットする関数
    Args:
        offsetFrame (float): オフセット値
    """
    cmds.keyframe(e=1,r=1,tc=offsetFrame)

def cycleOffsetKeyframe(offsetFrame):
    u"""Description
        サイクルするキーフレームをオフセットする関数
    Args:
        offsetFrame (float): オフセット値
    """    
    cmds.selectKey(cl=1)
    #アニムカーブ一覧を取得
    animCrvs = cmds.keyframe(q=1,n=1)
    
    #キーの先頭と終端を取得
    minFrame = min(cmds.keyframe(q=1))
    maxFrame = max(cmds.keyframe(q=1))
    distFrame = maxFrame-minFrame
    
    #最初と最後に抑えのキーを打つ
    cmds.currentTime(minFrame)
    cmds.setKeyframe(insert=1)
    cmds.currentTime(maxFrame)
    cmds.setKeyframe(insert=1)
    
    #前フレームと後ろフレームにアニメーションをコピペ
    minPasteFrame = minFrame-distFrame
    cmds.selectKey(cl=1)
    cmds.copyKey()
    cmds.pasteKey(copies=1,
                  option='merge',
                  time=(minPasteFrame ,minPasteFrame ) )
    cmds.pasteKey(copies=1,
                  option='merge',
                  time=(maxFrame,maxFrame) )
    
    #アニメーションカーブを指定値だけオフセット
    cmds.selectKey()
    cmds.keyframe(e=1,r=1,tc=offsetFrame)
    
    #最初と最後に抑えのキーを打つ
    cmds.currentTime(minFrame)
    cmds.setKeyframe(insert=1)
    cmds.currentTime(maxFrame)
    cmds.setKeyframe(insert=1)
    
    #不要なキーフレームを削除
    cmds.selectKey(cl=1)
    maxPasteFrame = max(set(cmds.keyframe(q=1)))
    cmds.cutKey( time=(minPasteFrame,minFrame-1),option="keys" )
    cmds.cutKey( time=(maxFrame+1,maxPasteFrame),option="keys" )
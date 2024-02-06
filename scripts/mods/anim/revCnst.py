# -*- coding:utf-8 -*-
import maya.cmds as cmds

def revCnst(scale        = 0,
             rotateOrder = 0,
             simMode     = 1,
             time        = [cmds.playbackOptions(q=1,min=1),
                            cmds.playbackOptions(q=1,max=1)],
             singleFrame = False,
             cnstOption  = True,
             viewportOff = False):
    #使い方：選択して実行

    #処理内容：選択したノードのアニメーション情報をロケーターに移し、
    #そのロケータで逆にアニメーション元のノードにコンストレインかけるスクリプト

    #スタートとエンドのフレームを取得
    #StartFrame = cmds.playbackOptions(q=1,min=1)
    #EndFrame   = cmds.playbackOptions(q=1,max=1)
    StartFrame = time[0]
    EndFrame   = time[1]

    #変数の初期化
    SelArray = cmds.ls(sl=1,l=0)
    LocArray = []
    CnstArray = []

    #選択したノードをループ処理
    for work in SelArray:
        #選択したノード名の末尾に_locを付けてロケータを作成
        loc = cmds.spaceLocator(n=work+"_loc#")

        cmds.setAttr(loc[0]+".rotateOrder",rotateOrder)
        LocArray.append(cmds.ls(sl=1,l=1)[0])

        #コンストレインを行う
        cmds.select(work,loc)
        cnst = cmds.parentConstraint()[0]
        CnstArray.append(cnst)

        cnst = cmds.scaleConstraint()[0]
        CnstArray.append(cnst)

    cmds.select(LocArray)

    if viewportOff:
      #アクティブなパネルを取得
      WfPanel = cmds.getPanel(wf=1)
      WfPanelType = cmds.getPanel(to=WfPanel)
      #isolate selectionモードにして処理の負荷を低減させる
      if WfPanelType == "modelPanel":
         cmds.isolateSelect(WfPanel,state=1)

    #ベイク処理を行う
    if singleFrame == False: #singleFrameに値が入ってなければベイク処理
      if simMode == 1:
         cmds.bakeResults(LocArray,simulation=1,t=(StartFrame,EndFrame))
      else:
         cmds.bakeResults(LocArray,simulation=0,t=(StartFrame,EndFrame))

    #コンストレインの削除
    cmds.delete(CnstArray)

    if viewportOff:
       #ビューの表示を元に戻す
       if WfPanelType == "modelPanel":
          cmds.isolateSelect(WfPanel,state=0)
    
    #cnstオプションがある場合、逆コンスト
    if cnstOption:
      for i in range(len(LocArray)):
         #ポイントコンストレインを行う。この時処理が実行されなかったら、処理をスルーする
         try:
            cmds.pointConstraint(LocArray[i],SelArray[i],mo=0)
         except:
            print "do not point constrain"
         #オリエントコンストレインを行う。この時処理が実行されなかったら、処理をスルーする
         try:
            cmds.orientConstraint(LocArray[i],SelArray[i],mo=0)
         except:
            print "do not orient constrain"
         #スケールコンストレインを行う。この時処理が実行されなかったら、処理をスルーする
         try:
            cmds.scaleConstraint(LocArray[i],SelArray[i],mo=0)
         except:
            print "do not orient constrain"
    cmds.filterCurve()
    return LocArray
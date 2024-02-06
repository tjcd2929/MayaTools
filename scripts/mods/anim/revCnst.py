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
    #�g�����F�I�����Ď��s

    #�������e�F�I�������m�[�h�̃A�j���[�V�����������P�[�^�[�Ɉڂ��A
    #���̃��P�[�^�ŋt�ɃA�j���[�V�������̃m�[�h�ɃR���X�g���C��������X�N���v�g

    #�X�^�[�g�ƃG���h�̃t���[�����擾
    #StartFrame = cmds.playbackOptions(q=1,min=1)
    #EndFrame   = cmds.playbackOptions(q=1,max=1)
    StartFrame = time[0]
    EndFrame   = time[1]

    #�ϐ��̏�����
    SelArray = cmds.ls(sl=1,l=0)
    LocArray = []
    CnstArray = []

    #�I�������m�[�h�����[�v����
    for work in SelArray:
        #�I�������m�[�h���̖�����_loc��t���ă��P�[�^���쐬
        loc = cmds.spaceLocator(n=work+"_loc#")

        cmds.setAttr(loc[0]+".rotateOrder",rotateOrder)
        LocArray.append(cmds.ls(sl=1,l=1)[0])

        #�R���X�g���C�����s��
        cmds.select(work,loc)
        cnst = cmds.parentConstraint()[0]
        CnstArray.append(cnst)

        cnst = cmds.scaleConstraint()[0]
        CnstArray.append(cnst)

    cmds.select(LocArray)

    if viewportOff:
      #�A�N�e�B�u�ȃp�l�����擾
      WfPanel = cmds.getPanel(wf=1)
      WfPanelType = cmds.getPanel(to=WfPanel)
      #isolate selection���[�h�ɂ��ď����̕��ׂ�ጸ������
      if WfPanelType == "modelPanel":
         cmds.isolateSelect(WfPanel,state=1)

    #�x�C�N�������s��
    if singleFrame == False: #singleFrame�ɒl�������ĂȂ���΃x�C�N����
      if simMode == 1:
         cmds.bakeResults(LocArray,simulation=1,t=(StartFrame,EndFrame))
      else:
         cmds.bakeResults(LocArray,simulation=0,t=(StartFrame,EndFrame))

    #�R���X�g���C���̍폜
    cmds.delete(CnstArray)

    if viewportOff:
       #�r���[�̕\�������ɖ߂�
       if WfPanelType == "modelPanel":
          cmds.isolateSelect(WfPanel,state=0)
    
    #cnst�I�v�V����������ꍇ�A�t�R���X�g
    if cnstOption:
      for i in range(len(LocArray)):
         #�|�C���g�R���X�g���C�����s���B���̎����������s����Ȃ�������A�������X���[����
         try:
            cmds.pointConstraint(LocArray[i],SelArray[i],mo=0)
         except:
            print "do not point constrain"
         #�I���G���g�R���X�g���C�����s���B���̎����������s����Ȃ�������A�������X���[����
         try:
            cmds.orientConstraint(LocArray[i],SelArray[i],mo=0)
         except:
            print "do not orient constrain"
         #�X�P�[���R���X�g���C�����s���B���̎����������s����Ȃ�������A�������X���[����
         try:
            cmds.scaleConstraint(LocArray[i],SelArray[i],mo=0)
         except:
            print "do not orient constrain"
    cmds.filterCurve()
    return LocArray
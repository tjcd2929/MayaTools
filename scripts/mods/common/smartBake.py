## -*- coding: utf-8 -*-
import maya.cmds as cmds
import sys

def smartBake(bakeMode="allKey",
              start=0,
              end=1,
              viewportOff=False):
    
    #�֐������s���ꂽ�̂��v�����g���ŏo��
    print "start : --- "+sys._getframe().f_code.co_name+" --- \n",
    
    #�X�^�[�g�ƃG���h�̃t���[�����擾
    if bakeMode == "allKey":
        start = cmds.playbackOptions(q=1,min=1)
        end = cmds.playbackOptions(q=1,max=1)
    
    selArray = cmds.ls(sl=1,l=1)
    
    if viewportOff:
        #�A�N�e�B�u�ȃp�l�����擾
        WfPanel = cmds.getPanel(wf=1)
        WfPanelType = cmds.getPanel(to=WfPanel)
        #isolate selection���[�h�ɂ��ď����̕��ׂ�ጸ������
        if WfPanelType == "modelPanel":
            cmds.select(cl=1)
            cmds.isolateSelect(WfPanel,state=1)
    
    #�x�C�N�������s��
    if bakeMode == "allKey":
        cmds.bakeResults(selArray,simulation=1,pok=1,t=(start,end))
    elif bakeMode == "inFrame":
        #�X�^�[�g�ƃG���h�̃t���[�����擾
        start = cmds.playbackOptions(q=1,min=1)
        end = cmds.playbackOptions(q=1,max=1)
        cmds.bakeResults(selArray,simulation=1,pok=0,t=(start,end))
    else:
        cmds.bakeResults(selArray,simulation=1,pok=1,t=(start,end))
    cmds.filterCurve()

    if viewportOff:
        #�r���[�̕\�������ɖ߂�
        if WfPanelType == "modelPanel":
            cmds.isolateSelect(WfPanel,state=0)
    
    cmds.select(selArray)
    
    #�֐����I�������̂��v�����g���ŏo��
    print "end : --- "+sys._getframe().f_code.co_name+" --- \n",
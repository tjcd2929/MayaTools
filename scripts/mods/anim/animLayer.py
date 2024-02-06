# -*- coding:utf-8 -*-

import maya.cmds as cmds
import maya.mel as mel

#source : https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-get-the-animated-attr-associated-with-an-anim-curve-in-Maya.html

def get_sel_anim_layers():
    u"""
    get current selected layers
    選択しているアニメーションレイヤを取得
    ================================================================================================================
    """
    return mel.eval('getSelectedAnimLayer("AnimLayerTab")')

def get_all_anim_layers():
    u"""
    select all anim layers
    全部のアニメーションレイヤを取得
    ================================================================================================================
    """
    return cmds.ls(type='animLayer')

def select_layer(names = None, add_root = False):
    u"""
    select layer
    アニメーションレイヤを選択
    ================================================================================================================
    :param names: list with layer names to select
    :param add_root: add root to selection
    :return:
    ================================================================================================================
    """
    # create list if none provided
    if names is None:
        names= list()
    
    # select base layer
    if add_root and add_root not in names:
        names.append(cmds.animLayer(root = True, q = True))
    
    # nothing to select
    if not names:
        return
    
    # select layers and deselect others
    all_anim = get_all_anim_layers()
    for i in all_anim:
        if i not in names:
            # deselect
            mel.eval('animLayerEditorOnSelect "{}" 0'.format(i))
        elif i in names:
            # select
            mel.eval('animLayerEditorOnSelect "{}" 1'.format(i))
        else:
            raise RuntimeError('layer name not found', i)
    return names
    
def get_curves_from_layers(objects, layers):
    u"""
    get curves by layer
    オブジェクト、レイヤーを指定して、関連するアニメーションカーブを取得
    ================================================================================================================
    :param objects: objects to look for
    :param layers: layers to look at
    :return:
    ================================================================================================================
    """
    if not get_all_anim_layers():
        return []
    sel = get_sel_anim_layers()
    # build anim layer menu if procedure not found
    mel.eval('if (!`exists selectLayer`) source buildSetAnimLayerMenu;')
    # deselect all
    select_layer(names=None, add_root=False)
    curves = list()
    for layer in layers:
        # select Layer
        mel.eval('selectLayer {} ;'.format(layer))
        # get curves
        get_curves = cmds.keyframe(objects, query=True, name=True, selected=False) or []
        curves.extend(get_curves)
        # deselect all
        select_layer(names=None, add_root=False)
        # select original selection
        select_layer(names=sel)
    return curves

def get_anim_curve_by_selected():
    u"""
    get curves by selected layer
    選択しているノード、選択しているアニメーションレイヤー
    を自動で取得して、それに関連するアニメーションカーブを取得。
    :param objects: objects list
    :param layers: layer name
    """
    objects=cmds.ls(sl=1)
    layers=get_sel_anim_layers()
    all_curve = get_curves_from_layers(objects = objects, layers = layers)

    return all_curve
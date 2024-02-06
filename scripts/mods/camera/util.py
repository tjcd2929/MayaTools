import maya.cmds as cmds
import math

#カメラの水平視野角を取得
def calculateHAOV(cameraName):
    # カメラの焦点距離を取得（ミリメートル単位）
    focalLength = cmds.camera(cameraName, query=True, focalLength=True)

    # カメラのフィルムの幅を取得（インチ単位）
    # Mayaではフィルムのサイズはインチ単位で提供されているので、ミリメートルに変換する
    filmWidthInch = cmds.camera(cameraName, query=True, horizontalFilmAperture=True)
    filmWidth = filmWidthInch * 25.4  # 1インチ = 25.4ミリメートル

    # 視野角を計算（ラジアン単位）
    aovRadians = 2 * math.atan(filmWidth / (focalLength * 2))

    # 視野角を度数法に変換
    aovDegrees = math.degrees(aovRadians)

    return aovDegrees

#カメラの垂直視野角を取得
def calculateVAOV(cameraName):
    # カメラのフィルムの高さを取得（インチ単位）
    # Mayaではフィルムのサイズはインチ単位で提供されているので、ミリメートルに変換する
    filmHeightInch = cmds.camera(cameraName, query=True, verticalFilmAperture=True)
    filmHeight = filmHeightInch * 25.4  # 1インチ = 25.4ミリメートル

    # カメラの焦点距離を取得（ミリメートル単位）
    focalLength = cmds.camera(cameraName, query=True, focalLength=True)

    # 視野角を計算（ラジアン単位）
    aovRadians = 2 * math.atan(filmHeight / (focalLength * 2))

    # 視野角を度数法に変換
    aovDegrees = math.degrees(aovRadians)

    return aovDegrees

def calculateBaseOfTriangle(cameraName, distance):
    #cameraNameのFit Resolution Gateをチェックして処理を分岐
    fitResGate = cmds.camera(cameraName, query=True, fitResGate=True)
    
    if fitResGate == 2:
        # カメラの垂直視野角を取得（度数法）
        aov = calculateVAOV(cameraName)
    else:
        # カメラの水平視野角を取得（度数法）
        aov = calculateHAOV(cameraName)
    
    # 視野角をラジアンに変換
    aovRadians = math.radians(aov)
    
    # 三角形の底辺を計算
    base = 2 * distance * math.tan(aovRadians / 2)
    
    return base
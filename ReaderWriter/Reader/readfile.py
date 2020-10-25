#!/usr/bin/env python3
# Copyright (c) 2018 Zih-Rou Cyue. All rights reserved

# coding=utf-8
# -*- coding: utf8 -*-


"""
my_readfile is a module to process the read file with/without tag line
in a file. 

"""

# python module
import sys
import os
import collections
# my module

from .tagline import readTagColNum, GroupCheckBool, GroupSelect

def strMultiSepSplit(strr, mysep = " \t", maxsplit = -1):
    split_row = strr
    if len(mysep)>0:
        for ii in (range(len(mysep)-1)):
            strr = strr.replace(mysep[ii+1],mysep[0])
        split_row = [r for r in strr.split(mysep[0],maxsplit) if r]        
    return split_row 
def myStr2Number(strr, MustNumberFlag=False, errMsg='', IsIntBol=False, errPrintFlag=True):
    try:   
        if IsIntBol==True:
            return True, int(strr)
        else:
            return True, float(strr)
    except ValueError:
        if (MustNumberFlag==False):
            return True, strr # string data
        else:
            if errPrintFlag:
                print(errMsg)
            return False,  strr # string data
def readContents(fpath, filename, mysep = " \t", maxsplit = -1, removeEmptyLine=False):
    """
    readContents is a function to read the contents in the file and
    return a list of tokens of the content
    path: the file path need processed
    filename: the name of file need processed
    mysep: (Optional) Character dividing the string into split groups; default is space and tab.
    
    >>> fpath = './Example'
    >>> fname = 'cbp_irppy2acac.spc'
    >>> Valid, content_tokens = readContents(fpath,fname)
    >>> print(content_tokens)
    [['380', '0.00358'], ['410', '0.00201'], ['411', '0'], ['412', '0.00244'], ['413', '0.00125'], ['414', '0.00339'], ['415', '0.00422'], ['416', '0.00713'], ['417', '0.00327'], ['418', '0.00277'], ['419', '8.00308E-4'], ['420', '0.00349'], ['421', '0.00387'], ['422', '0.00355'], ['423', '0.00286'], ['424', '0.00346'], ['425', '0.003'], ['426', '0.00272'], ['427', '0.00217'], ['428', '0.0023'], ['429', '0.00173'], ['430', '0.00158'], ['431', '0.00214'], ['432', '0.00156'], ['433', '0.00213'], ['434', '0.00152'], ['435', '0.00185'], ['436', '0.00124'], ['437', '0.00139'], ['438', '7.04193E-4'], ['439', '9.79747E-4'], ['440', '0.00112'], ['441', '5.66416E-4'], ['442', '7.96044E-4'], ['443', '3.06171E-4'], ['444', '4.28639E-4'], ['445', '8.11353E-4'], ['446', '2.29628E-4'], ['447', '5.51108E-4'], ['448', '4.43948E-4'], ['449', '5.97033E-4'], ['450', '4.28639E-4'], ['451', '3.36788E-4'], ['452', '4.43948E-4'], ['453', '2.60245E-4'], ['454', '6.12342E-5'], ['455', '0'], ['456', '9.18513E-5'], ['457', '3.36788E-4'], ['458', '7.65427E-5'], ['459', '2.29628E-4'], ['460', '2.1432E-4'], ['461', '1.22468E-4'], ['462', '6.2765E-4'], ['463', '2.90862E-4'], ['464', '4.28639E-4'], ['465', '8.72587E-4'], ['466', '8.11353E-4'], ['467', '9.33821E-4'], ['468', '0.00124'], ['469', '0.00181'], ['470', '0.00196'], ['471', '0.00277'], ['472', '0.00292'], ['473', '0.004'], ['474', '0.00456'], ['475', '0.00531'], ['476', '0.00733'], ['477', '0.00788'], ['478', '0.0098'], ['479', '0.01079'], ['480', '0.01453'], ['481', '0.01531'], ['482', '0.0177'], ['483', '0.02143'], ['484', '0.02664'], ['485', '0.02967'], ['486', '0.03538'], ['487', '0.04071'], ['488', '0.04932'], ['489', '0.05675'], ['490', '0.06763'], ['491', '0.08081'], ['492', '0.09381'], ['493', '0.11462'], ['494', '0.12867'], ['495', '0.15639'], ['496', '0.18089'], ['497', '0.21101'], ['498', '0.24183'], ['499', '0.27612'], ['500', '0.31404'], ['501', '0.35773'], ['502', '0.39525'], ['503', '0.44234'], ['504', '0.48487'], ['505', '0.52381'], ['506', '0.57954'], ['507', '0.62228'], ['508', '0.66888'], ['509', '0.71774'], ['510', '0.75512'], ['511', '0.79828'], ['512', '0.83647'], ['513', '0.87381'], ['514', '0.90253'], ['515', '0.92704'], ['516', '0.95501'], ['517', '0.97277'], ['518', '0.98282'], ['519', '0.98901'], ['520', '0.98584'], ['521', '1'], ['522', '0.9957'], ['523', '0.98812'], ['524', '0.97667'], ['525', '0.96545'], ['526', '0.95414'], ['527', '0.94014'], ['528', '0.92044'], ['529', '0.90992'], ['530', '0.88297'], ['531', '0.87104'], ['532', '0.84981'], ['533', '0.8456'], ['534', '0.81752'], ['535', '0.8016'], ['536', '0.79047'], ['537', '0.76238'], ['538', '0.74609'], ['539', '0.73472'], ['540', '0.72379'], ['541', '0.7126'], ['542', '0.69965'], ['543', '0.69147'], ['544', '0.68082'], ['545', '0.66442'], ['546', '0.65657'], ['547', '0.65224'], ['548', '0.64327'], ['549', '0.63564'], ['550', '0.6256'], ['551', '0.61334'], ['552', '0.60412'], ['553', '0.59246'], ['554', '0.58171'], ['555', '0.57461'], ['556', '0.56479'], ['557', '0.55919'], ['558', '0.54255'], ['559', '0.53137'], ['560', '0.51879'], ['561', '0.50971'], ['562', '0.49356'], ['563', '0.48266'], ['564', '0.47181'], ['565', '0.45707'], ['566', '0.4497'], ['567', '0.43031'], ['568', '0.41527'], ['569', '0.40422'], ['570', '0.39602'], ['571', '0.38157'], ['572', '0.36886'], ['573', '0.35488'], ['574', '0.34156'], ['575', '0.3342'], ['576', '0.32171'], ['577', '0.31447'], ['578', '0.30299'], ['579', '0.29189'], ['580', '0.27952'], ['581', '0.27332'], ['582', '0.26608'], ['583', '0.25392'], ['584', '0.2489'], ['585', '0.23845'], ['586', '0.23372'], ['587', '0.22223'], ['588', '0.21619'], ['589', '0.20553'], ['590', '0.20022'], ['591', '0.19653'], ['592', '0.18932'], ['593', '0.18525'], ['594', '0.17694'], ['595', '0.1715'], ['596', '0.16717'], ['597', '0.16389'], ['598', '0.15546'], ['599', '0.15064'], ['600', '0.14757'], ['601', '0.14157'], ['602', '0.13756'], ['603', '0.13263'], ['604', '0.1257'], ['605', '0.12135'], ['606', '0.11991'], ['607', '0.11615'], ['608', '0.11229'], ['609', '0.10878'], ['610', '0.10344'], ['611', '0.10035'], ['612', '0.0966'], ['613', '0.09205'], ['614', '0.09041'], ['615', '0.08799'], ['616', '0.0821'], ['617', '0.08002'], ['618', '0.07722'], ['619', '0.07582'], ['620', '0.07291'], ['621', '0.06759'], ['622', '0.06923'], ['623', '0.06358'], ['624', '0.05957'], ['625', '0.05908'], ['626', '0.05496'], ['627', '0.05389'], ['628', '0.05118'], ['629', '0.0492'], ['630', '0.04646'], ['631', '0.04599'], ['632', '0.04329'], ['633', '0.04135'], ['634', '0.03849'], ['635', '0.03823'], ['636', '0.03749'], ['637', '0.03576'], ['638', '0.0333'], ['639', '0.03285'], ['640', '0.03247'], ['641', '0.02864'], ['642', '0.02979'], ['643', '0.02731'], ['644', '0.02621'], ['645', '0.02679'], ['646', '0.02583'], ['647', '0.02387'], ['648', '0.0237'], ['649', '0.02261'], ['650', '0.02443'], ['651', '0.02065'], ['652', '0.02002'], ['653', '0.01972'], ['654', '0.01911'], ['655', '0.01907'], ['656', '0.01708'], ['657', '0.0178'], ['658', '0.01545'], ['659', '0.01399'], ['660', '0.01431'], ['661', '0.01381'], ['662', '0.01381'], ['663', '0.01257'], ['664', '0.01249'], ['665', '0.0118'], ['666', '0.01147'], ['667', '0.01171'], ['668', '0.01078'], ['669', '0.01108'], ['670', '0.00989'], ['671', '0.00865'], ['672', '0.00914'], ['673', '0.00863'], ['674', '0.00795'], ['675', '0.00744'], ['676', '0.00798'], ['677', '0.00683'], ['678', '0.00631'], ['679', '0.00661'], ['680', '0.00603'], ['681', '0.0203'], ['682', '0.01896'], ['683', '0.01225'], ['684', '0.01683'], ['685', '0.01469'], ['686', '0.01183'], ['687', '0.0141'], ['688', '0.00948'], ['780', '0.00368']]
    >>> 

    """
    try:
        f = open(os.path.join(fpath, filename), 'r')  
    except FileNotFoundError:
        #print('[ReadContents] Cannot find file {0}.'.format(os.path.join(fpath, filename)))
        return False, []
    data = f.read() 
    f.close()
    rows = data.split('\n') 
    # data = readtag(rows)
    # print(data.keys())
    content_tokens = [] 
    for row in rows:
        tokens = strMultiSepSplit(row,mysep,maxsplit)
        if removeEmptyLine and len(tokens)==0:
            continue 
        content_tokens.append( tokens )
    return True, content_tokens
def Content2data(content_tokens,TagDict):
    """
    Content2data is a function to translate the content_tokens to a 
    dictionary of data. The key of output is the same as the key 
    in TagDict and the column number is the value of TagDict. 
    content_tokens: a list of list, containing the content of the file
    TagDict: a dictionaty. key is the name of the column, value is 
             the number of column

    >>> # case 1
    >>> TagDict = {'wavelength':0,'PL':1}
    >>> content_tokens = [ ["520","1"],["530","2"], ["540","3"], ["550","2"], ["560","1"]]
    >>> dataDict = Content2data(content_tokens,TagDict)
    >>> print(dataDict['wavelength'])
    [520.0, 530.0, 540.0, 550.0, 560.0]
    >>> print(dataDict['PL'])
    [1.0, 2.0, 3.0, 2.0, 1.0]
    >>>
    >>> # case 2
    >>> TagDict = {'wavelength':1,'PL':0}
    >>> content_tokens = [ ["1","520"],["2","530"], ["3","540"], ["2","550"], ["1","560"]]
    >>> dataDict = Content2data(content_tokens,TagDict)
    >>> print(dataDict['wavelength'])
    [520.0, 530.0, 540.0, 550.0, 560.0]
    >>> print(dataDict['PL'])
    [1.0, 2.0, 3.0, 2.0, 1.0]
    >>> 
    >>> #case 3
    >>> fpath = './Example'
    >>> fname = 'cbp_irppy2acac.spc'
    >>> TagDict = {'wavelength':0, 'PL':1}
    >>> Valid, content_tokens = readContents(fpath,fname)
    >>> dataDict = Content2data(content_tokens,TagDict)
    >>> print(dataDict['wavelength'])
    [380.0, 410.0, 411.0, 412.0, 413.0, 414.0, 415.0, 416.0, 417.0, 418.0, 419.0, 420.0, 421.0, 422.0, 423.0, 424.0, 425.0, 426.0, 427.0, 428.0, 429.0, 430.0, 431.0, 432.0, 433.0, 434.0, 435.0, 436.0, 437.0, 438.0, 439.0, 440.0, 441.0, 442.0, 443.0, 444.0, 445.0, 446.0, 447.0, 448.0, 449.0, 450.0, 451.0, 452.0, 453.0, 454.0, 455.0, 456.0, 457.0, 458.0, 459.0, 460.0, 461.0, 462.0, 463.0, 464.0, 465.0, 466.0, 467.0, 468.0, 469.0, 470.0, 471.0, 472.0, 473.0, 474.0, 475.0, 476.0, 477.0, 478.0, 479.0, 480.0, 481.0, 482.0, 483.0, 484.0, 485.0, 486.0, 487.0, 488.0, 489.0, 490.0, 491.0, 492.0, 493.0, 494.0, 495.0, 496.0, 497.0, 498.0, 499.0, 500.0, 501.0, 502.0, 503.0, 504.0, 505.0, 506.0, 507.0, 508.0, 509.0, 510.0, 511.0, 512.0, 513.0, 514.0, 515.0, 516.0, 517.0, 518.0, 519.0, 520.0, 521.0, 522.0, 523.0, 524.0, 525.0, 526.0, 527.0, 528.0, 529.0, 530.0, 531.0, 532.0, 533.0, 534.0, 535.0, 536.0, 537.0, 538.0, 539.0, 540.0, 541.0, 542.0, 543.0, 544.0, 545.0, 546.0, 547.0, 548.0, 549.0, 550.0, 551.0, 552.0, 553.0, 554.0, 555.0, 556.0, 557.0, 558.0, 559.0, 560.0, 561.0, 562.0, 563.0, 564.0, 565.0, 566.0, 567.0, 568.0, 569.0, 570.0, 571.0, 572.0, 573.0, 574.0, 575.0, 576.0, 577.0, 578.0, 579.0, 580.0, 581.0, 582.0, 583.0, 584.0, 585.0, 586.0, 587.0, 588.0, 589.0, 590.0, 591.0, 592.0, 593.0, 594.0, 595.0, 596.0, 597.0, 598.0, 599.0, 600.0, 601.0, 602.0, 603.0, 604.0, 605.0, 606.0, 607.0, 608.0, 609.0, 610.0, 611.0, 612.0, 613.0, 614.0, 615.0, 616.0, 617.0, 618.0, 619.0, 620.0, 621.0, 622.0, 623.0, 624.0, 625.0, 626.0, 627.0, 628.0, 629.0, 630.0, 631.0, 632.0, 633.0, 634.0, 635.0, 636.0, 637.0, 638.0, 639.0, 640.0, 641.0, 642.0, 643.0, 644.0, 645.0, 646.0, 647.0, 648.0, 649.0, 650.0, 651.0, 652.0, 653.0, 654.0, 655.0, 656.0, 657.0, 658.0, 659.0, 660.0, 661.0, 662.0, 663.0, 664.0, 665.0, 666.0, 667.0, 668.0, 669.0, 670.0, 671.0, 672.0, 673.0, 674.0, 675.0, 676.0, 677.0, 678.0, 679.0, 680.0, 681.0, 682.0, 683.0, 684.0, 685.0, 686.0, 687.0, 688.0, 780.0]
    >>> print(dataDict['PL'])
    [0.00358, 0.00201, 0.0, 0.00244, 0.00125, 0.00339, 0.00422, 0.00713, 0.00327, 0.00277, 0.000800308, 0.00349, 0.00387, 0.00355, 0.00286, 0.00346, 0.003, 0.00272, 0.00217, 0.0023, 0.00173, 0.00158, 0.00214, 0.00156, 0.00213, 0.00152, 0.00185, 0.00124, 0.00139, 0.000704193, 0.000979747, 0.00112, 0.000566416, 0.000796044, 0.000306171, 0.000428639, 0.000811353, 0.000229628, 0.000551108, 0.000443948, 0.000597033, 0.000428639, 0.000336788, 0.000443948, 0.000260245, 6.12342e-05, 0.0, 9.18513e-05, 0.000336788, 7.65427e-05, 0.000229628, 0.00021432, 0.000122468, 0.00062765, 0.000290862, 0.000428639, 0.000872587, 0.000811353, 0.000933821, 0.00124, 0.00181, 0.00196, 0.00277, 0.00292, 0.004, 0.00456, 0.00531, 0.00733, 0.00788, 0.0098, 0.01079, 0.01453, 0.01531, 0.0177, 0.02143, 0.02664, 0.02967, 0.03538, 0.04071, 0.04932, 0.05675, 0.06763, 0.08081, 0.09381, 0.11462, 0.12867, 0.15639, 0.18089, 0.21101, 0.24183, 0.27612, 0.31404, 0.35773, 0.39525, 0.44234, 0.48487, 0.52381, 0.57954, 0.62228, 0.66888, 0.71774, 0.75512, 0.79828, 0.83647, 0.87381, 0.90253, 0.92704, 0.95501, 0.97277, 0.98282, 0.98901, 0.98584, 1.0, 0.9957, 0.98812, 0.97667, 0.96545, 0.95414, 0.94014, 0.92044, 0.90992, 0.88297, 0.87104, 0.84981, 0.8456, 0.81752, 0.8016, 0.79047, 0.76238, 0.74609, 0.73472, 0.72379, 0.7126, 0.69965, 0.69147, 0.68082, 0.66442, 0.65657, 0.65224, 0.64327, 0.63564, 0.6256, 0.61334, 0.60412, 0.59246, 0.58171, 0.57461, 0.56479, 0.55919, 0.54255, 0.53137, 0.51879, 0.50971, 0.49356, 0.48266, 0.47181, 0.45707, 0.4497, 0.43031, 0.41527, 0.40422, 0.39602, 0.38157, 0.36886, 0.35488, 0.34156, 0.3342, 0.32171, 0.31447, 0.30299, 0.29189, 0.27952, 0.27332, 0.26608, 0.25392, 0.2489, 0.23845, 0.23372, 0.22223, 0.21619, 0.20553, 0.20022, 0.19653, 0.18932, 0.18525, 0.17694, 0.1715, 0.16717, 0.16389, 0.15546, 0.15064, 0.14757, 0.14157, 0.13756, 0.13263, 0.1257, 0.12135, 0.11991, 0.11615, 0.11229, 0.10878, 0.10344, 0.10035, 0.0966, 0.09205, 0.09041, 0.08799, 0.0821, 0.08002, 0.07722, 0.07582, 0.07291, 0.06759, 0.06923, 0.06358, 0.05957, 0.05908, 0.05496, 0.05389, 0.05118, 0.0492, 0.04646, 0.04599, 0.04329, 0.04135, 0.03849, 0.03823, 0.03749, 0.03576, 0.0333, 0.03285, 0.03247, 0.02864, 0.02979, 0.02731, 0.02621, 0.02679, 0.02583, 0.02387, 0.0237, 0.02261, 0.02443, 0.02065, 0.02002, 0.01972, 0.01911, 0.01907, 0.01708, 0.0178, 0.01545, 0.01399, 0.01431, 0.01381, 0.01381, 0.01257, 0.01249, 0.0118, 0.01147, 0.01171, 0.01078, 0.01108, 0.00989, 0.00865, 0.00914, 0.00863, 0.00795, 0.00744, 0.00798, 0.00683, 0.00631, 0.00661, 0.00603, 0.0203, 0.01896, 0.01225, 0.01683, 0.01469, 0.01183, 0.0141, 0.00948, 0.00368]
    >>> print(len(dataDict['wavelength']))
    281
    >>> print(len(dataDict['PL']))
    281

    """

    # output initialization
    dataDict = collections.defaultdict(list)
    #return dataDict
    for key in TagDict:
        dataDict[key] = []
    # insert data
    for ii,tokens in enumerate(content_tokens):
        if len(tokens)==0:
            continue
        if len(tokens)!=len(TagDict):
            #raise Exception('ColumnUnmatchedError', 'Line({0}): read number of column = {1}| valid number of column = {2}'
            #      .format(ii,len(tokens),len(TagDict)))
            print('[ColumnUnmatchedError] Line({0}): read number of column = {1}| valid number of column = {2}'.format(ii+1,len(tokens),len(TagDict)))
            return None
        for key, colNum in TagDict.items():
            Bool, value = myStr2Number(tokens[colNum])
            dataDict[key].append(value)
    return dataDict
def ColFileRead(fpath, filename, TagGroupList = None, unitBool = True, mysep = " \t", maxsplit = -1):
    """
    ColFileRead is a function to read the data from a file. 
    path: the file path need processed
    filename: the name of file need processed
    TagGroupList is a List of List to specify the group of the tag string.
    unitBool: is a bool to specify whether the tag contains unit or not
    mysep: (Optional) Character dividing the string into split groups; default is space and tab.
    
    >>> #case 1
    >>> fpath = './Example'
    >>> fname = 'cbp_irppy2acac.spc'
    >>> TagGroupList = [['wavelength', 'PL']]
    >>> validFile, dataDict, TagDict, unitDict, groupNumber = ColFileRead(fpath,fname, TagGroupList)
    >>> print(validFile)
    True
    >>> print(dataDict)
    defaultdict(<class 'list'>, {'wavelength': [380.0, 410.0, 411.0, 412.0, 413.0, 414.0, 415.0, 416.0, 417.0, 418.0, 419.0, 420.0, 421.0, 422.0, 423.0, 424.0, 425.0, 426.0, 427.0, 428.0, 429.0, 430.0, 431.0, 432.0, 433.0, 434.0, 435.0, 436.0, 437.0, 438.0, 439.0, 440.0, 441.0, 442.0, 443.0, 444.0, 445.0, 446.0, 447.0, 448.0, 449.0, 450.0, 451.0, 452.0, 453.0, 454.0, 455.0, 456.0, 457.0, 458.0, 459.0, 460.0, 461.0, 462.0, 463.0, 464.0, 465.0, 466.0, 467.0, 468.0, 469.0, 470.0, 471.0, 472.0, 473.0, 474.0, 475.0, 476.0, 477.0, 478.0, 479.0, 480.0, 481.0, 482.0, 483.0, 484.0, 485.0, 486.0, 487.0, 488.0, 489.0, 490.0, 491.0, 492.0, 493.0, 494.0, 495.0, 496.0, 497.0, 498.0, 499.0, 500.0, 501.0, 502.0, 503.0, 504.0, 505.0, 506.0, 507.0, 508.0, 509.0, 510.0, 511.0, 512.0, 513.0, 514.0, 515.0, 516.0, 517.0, 518.0, 519.0, 520.0, 521.0, 522.0, 523.0, 524.0, 525.0, 526.0, 527.0, 528.0, 529.0, 530.0, 531.0, 532.0, 533.0, 534.0, 535.0, 536.0, 537.0, 538.0, 539.0, 540.0, 541.0, 542.0, 543.0, 544.0, 545.0, 546.0, 547.0, 548.0, 549.0, 550.0, 551.0, 552.0, 553.0, 554.0, 555.0, 556.0, 557.0, 558.0, 559.0, 560.0, 561.0, 562.0, 563.0, 564.0, 565.0, 566.0, 567.0, 568.0, 569.0, 570.0, 571.0, 572.0, 573.0, 574.0, 575.0, 576.0, 577.0, 578.0, 579.0, 580.0, 581.0, 582.0, 583.0, 584.0, 585.0, 586.0, 587.0, 588.0, 589.0, 590.0, 591.0, 592.0, 593.0, 594.0, 595.0, 596.0, 597.0, 598.0, 599.0, 600.0, 601.0, 602.0, 603.0, 604.0, 605.0, 606.0, 607.0, 608.0, 609.0, 610.0, 611.0, 612.0, 613.0, 614.0, 615.0, 616.0, 617.0, 618.0, 619.0, 620.0, 621.0, 622.0, 623.0, 624.0, 625.0, 626.0, 627.0, 628.0, 629.0, 630.0, 631.0, 632.0, 633.0, 634.0, 635.0, 636.0, 637.0, 638.0, 639.0, 640.0, 641.0, 642.0, 643.0, 644.0, 645.0, 646.0, 647.0, 648.0, 649.0, 650.0, 651.0, 652.0, 653.0, 654.0, 655.0, 656.0, 657.0, 658.0, 659.0, 660.0, 661.0, 662.0, 663.0, 664.0, 665.0, 666.0, 667.0, 668.0, 669.0, 670.0, 671.0, 672.0, 673.0, 674.0, 675.0, 676.0, 677.0, 678.0, 679.0, 680.0, 681.0, 682.0, 683.0, 684.0, 685.0, 686.0, 687.0, 688.0, 780.0], 'PL': [0.00358, 0.00201, 0.0, 0.00244, 0.00125, 0.00339, 0.00422, 0.00713, 0.00327, 0.00277, 0.000800308, 0.00349, 0.00387, 0.00355, 0.00286, 0.00346, 0.003, 0.00272, 0.00217, 0.0023, 0.00173, 0.00158, 0.00214, 0.00156, 0.00213, 0.00152, 0.00185, 0.00124, 0.00139, 0.000704193, 0.000979747, 0.00112, 0.000566416, 0.000796044, 0.000306171, 0.000428639, 0.000811353, 0.000229628, 0.000551108, 0.000443948, 0.000597033, 0.000428639, 0.000336788, 0.000443948, 0.000260245, 6.12342e-05, 0.0, 9.18513e-05, 0.000336788, 7.65427e-05, 0.000229628, 0.00021432, 0.000122468, 0.00062765, 0.000290862, 0.000428639, 0.000872587, 0.000811353, 0.000933821, 0.00124, 0.00181, 0.00196, 0.00277, 0.00292, 0.004, 0.00456, 0.00531, 0.00733, 0.00788, 0.0098, 0.01079, 0.01453, 0.01531, 0.0177, 0.02143, 0.02664, 0.02967, 0.03538, 0.04071, 0.04932, 0.05675, 0.06763, 0.08081, 0.09381, 0.11462, 0.12867, 0.15639, 0.18089, 0.21101, 0.24183, 0.27612, 0.31404, 0.35773, 0.39525, 0.44234, 0.48487, 0.52381, 0.57954, 0.62228, 0.66888, 0.71774, 0.75512, 0.79828, 0.83647, 0.87381, 0.90253, 0.92704, 0.95501, 0.97277, 0.98282, 0.98901, 0.98584, 1.0, 0.9957, 0.98812, 0.97667, 0.96545, 0.95414, 0.94014, 0.92044, 0.90992, 0.88297, 0.87104, 0.84981, 0.8456, 0.81752, 0.8016, 0.79047, 0.76238, 0.74609, 0.73472, 0.72379, 0.7126, 0.69965, 0.69147, 0.68082, 0.66442, 0.65657, 0.65224, 0.64327, 0.63564, 0.6256, 0.61334, 0.60412, 0.59246, 0.58171, 0.57461, 0.56479, 0.55919, 0.54255, 0.53137, 0.51879, 0.50971, 0.49356, 0.48266, 0.47181, 0.45707, 0.4497, 0.43031, 0.41527, 0.40422, 0.39602, 0.38157, 0.36886, 0.35488, 0.34156, 0.3342, 0.32171, 0.31447, 0.30299, 0.29189, 0.27952, 0.27332, 0.26608, 0.25392, 0.2489, 0.23845, 0.23372, 0.22223, 0.21619, 0.20553, 0.20022, 0.19653, 0.18932, 0.18525, 0.17694, 0.1715, 0.16717, 0.16389, 0.15546, 0.15064, 0.14757, 0.14157, 0.13756, 0.13263, 0.1257, 0.12135, 0.11991, 0.11615, 0.11229, 0.10878, 0.10344, 0.10035, 0.0966, 0.09205, 0.09041, 0.08799, 0.0821, 0.08002, 0.07722, 0.07582, 0.07291, 0.06759, 0.06923, 0.06358, 0.05957, 0.05908, 0.05496, 0.05389, 0.05118, 0.0492, 0.04646, 0.04599, 0.04329, 0.04135, 0.03849, 0.03823, 0.03749, 0.03576, 0.0333, 0.03285, 0.03247, 0.02864, 0.02979, 0.02731, 0.02621, 0.02679, 0.02583, 0.02387, 0.0237, 0.02261, 0.02443, 0.02065, 0.02002, 0.01972, 0.01911, 0.01907, 0.01708, 0.0178, 0.01545, 0.01399, 0.01431, 0.01381, 0.01381, 0.01257, 0.01249, 0.0118, 0.01147, 0.01171, 0.01078, 0.01108, 0.00989, 0.00865, 0.00914, 0.00863, 0.00795, 0.00744, 0.00798, 0.00683, 0.00631, 0.00661, 0.00603, 0.0203, 0.01896, 0.01225, 0.01683, 0.01469, 0.01183, 0.0141, 0.00948, 0.00368]})
    >>> print(TagDict)
    defaultdict(<class 'list'>, {'wavelength': 0, 'PL': 1})
    >>> print(unitDict)
    None
    >>>
    >>> #case 2
    >>> fpath = './Example'
    >>> fname = 'cbp_irppy2acac_tagline.spc'
    >>> TagGroupList = [['PL', 'wavelength']]
    >>> validFile, dataDict, TagDict, unitDict, groupNumber = ColFileRead(fpath,fname, TagGroupList)
    >>> print(validFile)
    True
    >>> print(dataDict)
    defaultdict(<class 'list'>, {'PL': [0.00358, 0.00201, 0.0, 0.00244, 0.00125, 0.00339, 0.00422, 0.00713, 0.00327, 0.00277, 0.000800308, 0.00349, 0.00387, 0.00355, 0.00286, 0.00346, 0.003, 0.00272, 0.00217, 0.0023, 0.00173, 0.00158, 0.00214, 0.00156, 0.00213, 0.00152, 0.00185, 0.00124, 0.00139, 0.000704193, 0.000979747, 0.00112, 0.000566416, 0.000796044, 0.000306171, 0.000428639, 0.000811353, 0.000229628, 0.000551108, 0.000443948, 0.000597033, 0.000428639, 0.000336788, 0.000443948, 0.000260245, 6.12342e-05, 0.0, 9.18513e-05, 0.000336788, 7.65427e-05, 0.000229628, 0.00021432, 0.000122468, 0.00062765, 0.000290862, 0.000428639, 0.000872587, 0.000811353, 0.000933821, 0.00124, 0.00181, 0.00196, 0.00277, 0.00292, 0.004, 0.00456, 0.00531, 0.00733, 0.00788, 0.0098, 0.01079, 0.01453, 0.01531, 0.0177, 0.02143, 0.02664, 0.02967, 0.03538, 0.04071, 0.04932, 0.05675, 0.06763, 0.08081, 0.09381, 0.11462, 0.12867, 0.15639, 0.18089, 0.21101, 0.24183, 0.27612, 0.31404, 0.35773, 0.39525, 0.44234, 0.48487, 0.52381, 0.57954, 0.62228, 0.66888, 0.71774, 0.75512, 0.79828, 0.83647, 0.87381, 0.90253, 0.92704, 0.95501, 0.97277, 0.98282, 0.98901, 0.98584, 1.0, 0.9957, 0.98812, 0.97667, 0.96545, 0.95414, 0.94014, 0.92044, 0.90992, 0.88297, 0.87104, 0.84981, 0.8456, 0.81752, 0.8016, 0.79047, 0.76238, 0.74609, 0.73472, 0.72379, 0.7126, 0.69965, 0.69147, 0.68082, 0.66442, 0.65657, 0.65224, 0.64327, 0.63564, 0.6256, 0.61334, 0.60412, 0.59246, 0.58171, 0.57461, 0.56479, 0.55919, 0.54255, 0.53137, 0.51879, 0.50971, 0.49356, 0.48266, 0.47181, 0.45707, 0.4497, 0.43031, 0.41527, 0.40422, 0.39602, 0.38157, 0.36886, 0.35488, 0.34156, 0.3342, 0.32171, 0.31447, 0.30299, 0.29189, 0.27952, 0.27332, 0.26608, 0.25392, 0.2489, 0.23845, 0.23372, 0.22223, 0.21619, 0.20553, 0.20022, 0.19653, 0.18932, 0.18525, 0.17694, 0.1715, 0.16717, 0.16389, 0.15546, 0.15064, 0.14757, 0.14157, 0.13756, 0.13263, 0.1257, 0.12135, 0.11991, 0.11615, 0.11229, 0.10878, 0.10344, 0.10035, 0.0966, 0.09205, 0.09041, 0.08799, 0.0821, 0.08002, 0.07722, 0.07582, 0.07291, 0.06759, 0.06923, 0.06358, 0.05957, 0.05908, 0.05496, 0.05389, 0.05118, 0.0492, 0.04646, 0.04599, 0.04329, 0.04135, 0.03849, 0.03823, 0.03749, 0.03576, 0.0333, 0.03285, 0.03247, 0.02864, 0.02979, 0.02731, 0.02621, 0.02679, 0.02583, 0.02387, 0.0237, 0.02261, 0.02443, 0.02065, 0.02002, 0.01972, 0.01911, 0.01907, 0.01708, 0.0178, 0.01545, 0.01399, 0.01431, 0.01381, 0.01381, 0.01257, 0.01249, 0.0118, 0.01147, 0.01171, 0.01078, 0.01108, 0.00989, 0.00865, 0.00914, 0.00863, 0.00795, 0.00744, 0.00798, 0.00683, 0.00631, 0.00661, 0.00603, 0.0203, 0.01896, 0.01225, 0.01683, 0.01469, 0.01183, 0.0141, 0.00948, 0.00368], 'wavelength': [380.0, 410.0, 411.0, 412.0, 413.0, 414.0, 415.0, 416.0, 417.0, 418.0, 419.0, 420.0, 421.0, 422.0, 423.0, 424.0, 425.0, 426.0, 427.0, 428.0, 429.0, 430.0, 431.0, 432.0, 433.0, 434.0, 435.0, 436.0, 437.0, 438.0, 439.0, 440.0, 441.0, 442.0, 443.0, 444.0, 445.0, 446.0, 447.0, 448.0, 449.0, 450.0, 451.0, 452.0, 453.0, 454.0, 455.0, 456.0, 457.0, 458.0, 459.0, 460.0, 461.0, 462.0, 463.0, 464.0, 465.0, 466.0, 467.0, 468.0, 469.0, 470.0, 471.0, 472.0, 473.0, 474.0, 475.0, 476.0, 477.0, 478.0, 479.0, 480.0, 481.0, 482.0, 483.0, 484.0, 485.0, 486.0, 487.0, 488.0, 489.0, 490.0, 491.0, 492.0, 493.0, 494.0, 495.0, 496.0, 497.0, 498.0, 499.0, 500.0, 501.0, 502.0, 503.0, 504.0, 505.0, 506.0, 507.0, 508.0, 509.0, 510.0, 511.0, 512.0, 513.0, 514.0, 515.0, 516.0, 517.0, 518.0, 519.0, 520.0, 521.0, 522.0, 523.0, 524.0, 525.0, 526.0, 527.0, 528.0, 529.0, 530.0, 531.0, 532.0, 533.0, 534.0, 535.0, 536.0, 537.0, 538.0, 539.0, 540.0, 541.0, 542.0, 543.0, 544.0, 545.0, 546.0, 547.0, 548.0, 549.0, 550.0, 551.0, 552.0, 553.0, 554.0, 555.0, 556.0, 557.0, 558.0, 559.0, 560.0, 561.0, 562.0, 563.0, 564.0, 565.0, 566.0, 567.0, 568.0, 569.0, 570.0, 571.0, 572.0, 573.0, 574.0, 575.0, 576.0, 577.0, 578.0, 579.0, 580.0, 581.0, 582.0, 583.0, 584.0, 585.0, 586.0, 587.0, 588.0, 589.0, 590.0, 591.0, 592.0, 593.0, 594.0, 595.0, 596.0, 597.0, 598.0, 599.0, 600.0, 601.0, 602.0, 603.0, 604.0, 605.0, 606.0, 607.0, 608.0, 609.0, 610.0, 611.0, 612.0, 613.0, 614.0, 615.0, 616.0, 617.0, 618.0, 619.0, 620.0, 621.0, 622.0, 623.0, 624.0, 625.0, 626.0, 627.0, 628.0, 629.0, 630.0, 631.0, 632.0, 633.0, 634.0, 635.0, 636.0, 637.0, 638.0, 639.0, 640.0, 641.0, 642.0, 643.0, 644.0, 645.0, 646.0, 647.0, 648.0, 649.0, 650.0, 651.0, 652.0, 653.0, 654.0, 655.0, 656.0, 657.0, 658.0, 659.0, 660.0, 661.0, 662.0, 663.0, 664.0, 665.0, 666.0, 667.0, 668.0, 669.0, 670.0, 671.0, 672.0, 673.0, 674.0, 675.0, 676.0, 677.0, 678.0, 679.0, 680.0, 681.0, 682.0, 683.0, 684.0, 685.0, 686.0, 687.0, 688.0, 780.0]})
    >>> print(TagDict)
    defaultdict(<class 'list'>, {'PL': 1, 'wavelength': 0})
    >>> print(unitDict)
    defaultdict(<class 'list'>, {'wavelength': 'nm', 'PL': ''})
    >>>
    >>>
    >>> # case 3
    >>> fpath = './Example'
    >>> fname = 'bmpypb_ne.mat'
    >>> TagGroupList = [['wavelength','n','k'],['wavelength','no','ko','ne','ke']]
    >>> validFile, dataDict, TagDict, unitDict, groupNumber = ColFileRead(fpath,fname, TagGroupList)
    >>> print(validFile)
    True
    >>> print(dataDict)
    defaultdict(<class 'list'>, {'wavelength': [400.0, 410.0, 420.0, 430.0, 440.0, 450.0, 460.0, 470.0, 480.0, 490.0, 500.0, 510.0, 520.0, 530.0, 540.0, 550.0, 560.0, 570.0, 580.0, 590.0, 600.0, 610.0, 620.0, 630.0, 640.0, 650.0, 660.0, 670.0, 680.0, 690.0, 700.0, 710.0, 720.0, 730.0, 740.0, 750.0, 760.0, 770.0, 780.0, 790.0, 800.0, 810.0, 820.0, 830.0, 840.0, 850.0, 860.0, 870.0, 880.0, 890.0, 900.0, 910.0, 920.0, 930.0, 940.0, 950.0, 960.0, 970.0, 980.0, 990.0, 1000.0], 'n': [1.73895953, 1.72595527, 1.71449179, 1.70435832, 1.69537676, 1.68739605, 1.68028758, 1.67394149, 1.6682636, 1.66317292, 1.6585996, 1.65448319, 1.65077127, 1.64741821, 1.64438424, 1.64163458, 1.63913873, 1.6368699, 1.63480452, 1.63292178, 1.63120327, 1.62963269, 1.62819558, 1.62687905, 1.62567165, 1.62456313, 1.62354435, 1.62260711, 1.62174406, 1.6209486, 1.62021479, 1.61953728, 1.61891123, 1.61833229, 1.61779651, 1.61730032, 1.61684046, 1.61641401, 1.61601828, 1.61565084, 1.61530946, 1.61499213, 1.61469699, 1.61442236, 1.61416669, 1.61392855, 1.61370667, 1.61349983, 1.61330696, 1.61312704, 1.61295915, 1.61280244, 1.61265612, 1.61251947, 1.61239181, 1.61227254, 1.61216109, 1.61205692, 1.61195954, 1.61186851, 1.6117834], 'k': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]})
    >>> print(TagDict)
    defaultdict(<class 'list'>, {'wavelength': 0, 'n': 1, 'k': 2})
    >>> print(unitDict)
    None

    """
    # content process
    validFile, content_tokens = readContents(fpath, filename, mysep, maxsplit)
    if validFile ==  False:
        return False,[],[],[],-1 
    validFile = False
    # tag process
    if TagGroupList==None:
        TagGroupList = [content_tokens[0]]
    tagstrList = [item for sublist in TagGroupList for item in sublist]
    if len(content_tokens) == 0: # empty file
        print("{0} {1} is an empty file.".format(fpath,filename))
        return validFile,None,None,None,None
    validTagDict, invalidTagDict, unitDict = readTagColNum(content_tokens[0], tagstrList, unitBool)
    groupNumber = GroupSelect(GroupCheckBool(validTagDict, TagGroupList))
    if  groupNumber == -1: # no tag line
        unitDict = None
        colNum = len(content_tokens[0])
        TagDict = None
        for ii,taggroup in enumerate(TagGroupList):
            if colNum == len(taggroup):
                TagDict =  collections.defaultdict(list,{key:ii for ii,key in enumerate(taggroup)})
                groupNumber = ii
                break
        if TagDict == None:
            print("{0} is with wrong column number.".format(os.path.join(fpath, filename)))
            print("Possible Group:")
            for taggroup in TagGroupList:
                print("ColNo:{0} | {1}".format(len(taggroup),'|'.join(taggroup)))
            return validFile,None,None,None,None
    else:
        content_tokens.pop(0)
        TagDict = collections.defaultdict(list,{key:validTagDict[key] for key in TagGroupList[groupNumber] })
    # content to data dict
    dataDict = Content2data(content_tokens,TagDict)
    validFile = False if dataDict==None else True
    # return
    return validFile, dataDict, TagDict, unitDict, groupNumber 
def test_fun():
    fpath = './Example'
    fname = 'cbp_irppy2acac.spc'
    TagDict = {'wavelength':0, 'PL':1}
    ValidFile, content_tokens = readContents(fpath,fname)
    dataDict = Content2data(content_tokens,TagDict)
    for ii in range(len(dataDict['wavelength'])):
        print("{0} {1}".format(dataDict['wavelength'][ii],dataDict['PL'][ii]))
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    # test_fun()










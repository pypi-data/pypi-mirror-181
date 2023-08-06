# -*- coding: utf-8 -*-

import pydatamodel.creditScore as creditScore
import pydatamodel.databaseModel as databaseModel
import pydatamodel.databaseModel as databaseModel

try:
    import pydatamodel.mechineLearning as mechineLearning
except ImportError:
    print('pydatamodel包的其他模块导入成功，但是mechineLearning模块导入失败。mechineLearning模块中，以下库是必须的，\
          你可能缺少了其中的一个或者多个：xlsxwriter、joblib、xgboost、openpyxl。如你不使用mechinelearning模块则无需理会本提示。')

__all__=['creditScore','mechineLearning']

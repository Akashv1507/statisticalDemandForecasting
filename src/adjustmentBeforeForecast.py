import datetime as dt
from typing import List, Tuple
from src.repos.adjustmentRepo import Adjustment

def doAdjustmentBeforeForecast(startDate : dt.datetime, endDate :dt.datetime, configDict:dict)->bool:
    """ this will do necessary adjustment for D-2

    Args:
        startDate (dt.datetime): start date
        endDate (dt.datetime): end date
        configDict (dict): application configuration dictionary

    Returns:
        bool: returns true if adjustment is success else false
    """
    conString:str = configDict['con_string_mis_warehouse']
    isAdjustmentSuccesscount = 0
    currDate = startDate
    #create object of class Adjustment
    obj_adjustment = Adjustment(conString)

    while currDate <= endDate:
        isAdjustmentSuccess = obj_adjustment.doAdjustment(currDate)
        if isAdjustmentSuccess:
            isAdjustmentSuccesscount = isAdjustmentSuccesscount + 1
        currDate += dt.timedelta(days=1)

    numOfDays = (endDate-startDate).days
    if isAdjustmentSuccesscount == numOfDays +1 :
        return True
    else:
        return False

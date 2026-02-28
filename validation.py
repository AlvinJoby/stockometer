def validateInput(symbol,start_date,end_date):

    if not symbol:
        return {"status":False,"error":"symbol is required"}
    if not start_date or not end_date:
        return {"status":False,"error":"both dates is required"}
    
    if start_date > end_date:
        return {"status":False,"error":"start date should be before end date"}
    
    return {"status":True}
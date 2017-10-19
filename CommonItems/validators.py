import os
import pandas as pd
from django.core.exceptions import ValidationError

def ValidCategoryFile(value):
    ext = os.path.splitext(value.name)[1]  
    validateExtension(ext)
    df = makeDataFrame(value)
    columnList = [u'Category Level 1 Code', 
        u'Category Level 1 Name', 
        u'Category Level 2 Code', 
        u'Category Level 2 Name'
        ]
    for column in columnList:
        validateColumn(df, column)
    validateRowCount(df)
    value.seek(0)
    


def getFileExtension(file):
    return os.path.splitext(file.name)[1]

def makeDataFrame(file):
    ext = getFileExtension(file)
    if ext == '.xlsx' or ext == '.xls':
        return pd.read_excel(file)
    elif ext == '.csv':
        return pd.read_csv(file, delimiter=u';')
    else:
        raise ValidationError(u'Unsupported file extension.')

def validateExtension (fileName):
    valid_extensions = ['.xlsx', '.xls', '.csv']
    if not fileName.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file extension.')

def validateColumn(dataFrame, columnName):
        if not columnName in dataFrame:
            raise ValidationError(u'Column: ' + columnName + u' missing from the provided file')
        
def validateRowCount(dataFrame):
    if dataFrame.shape[0] == 0:
        raise ValidationError(u'No rows found in the file.')


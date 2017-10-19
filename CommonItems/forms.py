from django import forms
from .validators import ValidCategoryFile
from models import SubCategory
import pandas as pd
import os

class FileForm(forms.Form):
    file = forms.FileField(validators=[ValidCategoryFile], help_text='Please upload a XLS, XLSX or CSV file.')

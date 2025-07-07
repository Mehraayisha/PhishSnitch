from django.test import TestCase
from .models import Quiz,Question,Choice,Category
import pandas as pd
import io
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
# Create your tests here.
class QuizModelTest(TestCase):
    def setUp(self):
        self.category=Category.objects.create(name='AI')
        self.excel_file=io.BytesIO()#create a memory space for excel_file
        df=pd.DataFrame({
            'Question':['What is 2+1?','What is 3+5?'],
            'A':['2','1'],
            'B':['3','8'],
            'C':['5','2'],
            'D':['1','4'],
            'Answer':['B','B']
        })
        df.to_excel(self.excel_file,index=False)#convert df to excel
        self.uploaded_file=SimpleUploadedFile('test_quiz.xlsx',self.excel_file,content_type='application/vnd.ms-excel')#treats the excel_file as uploaded file
        self.quiz=Quiz.objects.create(
            name='Quiz title',
            description='Quiz dec',
            category=self.category,
            quiz_file=self.uploaded_file
        )
    @patch('quiz.models.pd.read_excel')
    def test_import_quiz_from_excel(self,mock_read_excel_file):
        mock_df=pd.DataFrame({
            'Question':['What is 2+1?','What is 3+5?'],
            'A':['2','1'],
            'B':['3','8'],
            'C':['5','2'],
            'D':['1','4'],
            'Answer':['B','B']
        })
        mock_read_excel_file.return_value=mock_df
        self.assertEqual(self.category,"AI")
        self.assertEqual(self.quiz.name,'Quiz title')
        self.assertEqual(self.quiz.description,'Quiz dec')


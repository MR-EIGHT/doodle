from django.test import TestCase
import Document
# Create your tests here.

doc = Document(
    title = 'test',
    content = 'hi',
    url = 'https://google.com'
)
doc.save()
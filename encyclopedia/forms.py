from django import forms
class NewTaskForm(forms.Form):
    entryTitle = forms.CharField(label = "Title")
    entryContent = forms.CharField(widget = forms.Textarea())

    def __init__(self, session, title= None, content = None):
        self.session = session
        self.entryTitle = title
        self.entryContent = content
    def setTitle(self, title):
        self.entryTitle = title

    def setContent(self, content):
        self.entryContent = content

    def setEntry(self, title, content):
        self.entryTitle = title
        self.entryContent = content

import re

class specialchar:
    def spRemover(self, user):
        regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')
        if regex.search(user) == None:
            return True
        else:
            return False

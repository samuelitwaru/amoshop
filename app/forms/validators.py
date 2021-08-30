import re


class IsRequired:
    
    def __init__(self, msg="This field is required"):
        self.msg = msg

    def validate(self, form_data, str_data):
        if bool(str_data):
            return True, str_data
        return False, self.msg


class Email:
    
    def __init__(self, msg="Invalid email address"):
        self.msg = msg

    def validate(self, form_data, str_data):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, str_data):
            return True, str_data
        return False, self.msg


class EqualTo:

    def __init__(self, field_name, msg="Fields do not match"):
        self.field_name = field_name
        self.msg = msg

    def validate(self, form_data, str_data):
        if form_data[self.field_name] == str_data:
            return True, str_data
        return False, self.msg


class NotEqualTo:

    def __init__(self, field_name, msg="Fields should not be equal"):
        self.field_name = field_name
        self.msg = msg

    def validate(self, form_data, str_data):
        if form_data[self.field_name] != str_data:
            return True, str_data
        return False, self.msg


class RangeLen:

    def __init__(self, min_len=1, max_len=1024, msg=None):
        self.min_len = min_len
        self.max_len = max_len
        if msg:
            self.msg = msg 
        else:
            self.msg = f"Number of characters should range from {self.min_len} to {self.max_len}"

    def validate(self, form_data, str_data):
        if len(str_data) in range(self.min_len, self.max_len+1):
            return True, str_data
        return False, self.msg

import re


class Validator:

    def checkemail(email):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(regex, email):
            return 1
        else:
            return 0

    def checkmob(mobile):
        regex_mobile = '^[0][1-9]\d{9}$|^[1-9]\d{9}$'
        if re.match(regex_mobile, mobile):
            return 1
        else:
            return 0

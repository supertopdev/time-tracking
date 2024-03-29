from app.models import Users

class UserWeekInfo():
    """
    Class to compute and obtain the weekly info of an user
    """
    def __init__(self, data):
        self.user_id = data.get('user').get('id')
        self.data = data
        self.charge_codes_total = {}
        self.total_hrs = None
        self.user_name = None
        self.getName()
        self.computeDetails()

    def getName(self):
        """
        Gets Full Name corresponding to user_id
        """
        user = Users.query.get(self.user_id)
        self.full_name = user.full_name

    def computeDetails(self):
        """
        Computes the CC hours and total hours of an user
        """ 
        self.total_hrs = 0
        for charge_code, info in self.data['info'].items():
            charge_code_total = sum(int(item['hours']) for item in info if item['hours'] != None)
            self.total_hrs += charge_code_total
            self.charge_codes_total[charge_code] = charge_code_total

    def getHrs(self):
        """
        Returns total hours of user for week
        """
        return self.total_hrs

    def getCC(self):
        """
        Returns total hours of user for week by Charge Code
        """
        return self.charge_codes_total


class ManagerView():
    """
    Class to help with the 3 Manager views
    """
    def __init__(self, users_info=[]):
        self.users_info = users_info 

    def getChargeCodeTotal(self):
        """
        Get sum of all charge codes of all users
        """    
        result = {}

        for user_info in self.users_info:
            for charge_code, hrs in user_info.getCC().items():
                if charge_code in result:
                    result[charge_code] = hrs + result[charge_code]
                else:
                    result[charge_code] = hrs
        return result

    def getTotalHours(self):
        """
        Get total hours of each user
        """
        result = {}
        
        for user_info in self.users_info:
            result[user_info.full_name] = user_info.getHrs()
                    
        return result
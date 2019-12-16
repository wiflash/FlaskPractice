from datetime import datetime

class UserData:
    def __init__(self):
        self.created_at = None
        self.updated_at = None
        self.deleted_at = None
        self.id = 0
        self.name = None
        self.age = 0
        self.sex = None
        self.client_id = 0
    
    def reset(self):
        self.created_at = None
        self.updated_at = None
        self.deleted_at = None
        self.id = 0
        self.name = None
        self.age = 0
        self.sex = None
        self.client_id = 0


class Users:
    each_user = UserData()
    def __init__(self):
        self.users = []
    
    def get_all(self):
        return self.users
    
    def get_by_id(self, id):
        for selected_user in self.users:
            if selected_user["id"] == id:
                return selected_user
    
    def update_by_id(self, new_data, id):
        for index in range(len(self.users)):
            if self.users[index]["id"] == id:
                self.users[index]["updated_at"] = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                if new_data["name"] is not None: self.users[index]["name"] = new_data["name"]
                if new_data["age"] is not None: self.users[index]["age"] = new_data["age"]
                if new_data["sex"] is not None: self.users[index]["sex"] = new_data["sex"]
                if new_data["client_id"] is not None: self.users[index]["client_id"] = new_data["client_id"]
                return self.users[index]
    
    def add_new(self, new_data):
        self.users.append(new_data)
    
    def delete_by_id(self, id):
        for index in range(len(self.users)):
            if self.users[index]["id"] == id:
                self.users.pop(index)
                return True
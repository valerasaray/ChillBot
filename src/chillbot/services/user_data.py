class UserDataManager:
    def __init__(self):
        self.user_data = {}
    
    def save_message(self, user_id: int, message_text: str):
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                "messages": []
            }
        
        self.user_data[user_id]["messages"].append({
            "text": message_text,
        })
        
        if len(self.user_data[user_id]["messages"]) > 20:
            self.user_data[user_id]["messages"].pop(0)
    
    def get_last_message(self, user_id: int):
        if user_id in self.user_data and self.user_data[user_id]["messages"]:
            return self.user_data[user_id]["messages"][-1]
        return None
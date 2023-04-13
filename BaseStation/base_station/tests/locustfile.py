from locust import HttpUser, TaskSet, task, between


# 新建任务集
class QuickStartUser(HttpUser):
    @task
    def req_index(self):
        data = {
            "username": "admin",
            "password": "admin123456",
        }
        login_response = self.client.post('/new_data', data=data)

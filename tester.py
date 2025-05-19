from locust import HttpUser, between, task, constant

class ApiUser(HttpUser):
    wait_time = between(0.1, 0.5)  # 1 запрос в секунду на юзера

    @task
    def compute(self):
        self.client.post("/compute")
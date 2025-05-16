from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(0.01, 0.05)  # ~100 RPS на 1 пользователя

    @task
    def compute(self):
        self.client.post(
            "/compute",
            json={"data": "test"},
            headers={"Content-Type": "application/json"}
        )
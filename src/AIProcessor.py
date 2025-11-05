import threading
import time
import copy

from kivy.clock import Clock

class AIProcessor:
    def __init__(self):
        self.thread = threading.Thread(target=self.thread_proc)
        self.request_lock = threading.Lock()
        self.answer_lock = threading.Lock()

        self.request = None
        self.answer = None

        self.subscriber = None

        self.interrupted = False

    def prepare_to_close(self):
        self.interrupted = True
        self.thread.join()

    def start(self):
        self.thread.start()
        Clock.schedule_interval(self.check_answer, 0.1)

    def thread_proc(self):
        while not self.interrupted:
            key, value = self.pop_next_request()

            if key:
                prompt = self.make_ai_prompt(key, value)
                answer_type, answer = self.send_prompt(prompt)
                self.write_answer(answer_type, answer)

            time.sleep(0.1)

    def pop_next_request(self):
        with self.request_lock:
            if self.request is None:
                return "", ""

            key, value = copy.deepcopy(self.request)
            self.request = None

            return key, value

    def proc_request(self, key: str, value: str):
        with self.request_lock:
            self.request = (key, value)

    def make_ai_prompt(self, key: str, value: str):
        # todo implement
        return key + ": " + value

    def send_prompt(self, prompt: str):
        time.sleep(1.0)
        return "result", "AI generate smth for prompt: " + prompt

    def write_answer(self, answer_type: str, answer: str):
        with self.answer_lock:
            self.answer = (answer_type, answer)

    def pop_answer(self):
        with self.answer_lock:
            if self.answer is None:
                return "", ""

            key, value = copy.deepcopy(self.answer)
            self.answer = None

            return key, value

    def check_answer(self, dt):
        key, value = self.pop_answer()
        if key:
            self.subscriber(key, value)

    def subscribe_on_answer(self, subscriber: callable): #def proc_request(self, type: str, text: str):
        self.subscriber = subscriber
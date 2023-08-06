from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import multiprocessing as mp
import threading
import json
from google.cloud import bigquery

from de2_sentiment_analyzer.src.app import NLPModelPipeline


class ConsumeService:
    def __init__(self, project_id="dynamic-market-370212",
                 subscription_id="python-tweet-consumer", timeout=30.0):
        self.bq_client = bigquery.Client()
        self.bq_table_id = "dynamic-market-370212.twitter_dataset.tweet_sentiment"
        self.job_config = bigquery.QueryJobConfig(allow_large_results=True,
                                                  destination=self.bq_table_id)

        self.project_id = project_id
        self.subscription_id = subscription_id
        self.timeout = timeout
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(self.project_id,
                                                                   self.subscription_id)
        self.tweet_queue = mp.Queue()
        print(f"Listening for messages on {self.subscription_path}..\n")

    def callback(self, message: pubsub_v1.subscriber.message.Message) -> None:
        self.tweet_queue.put(message.data)
        print(f"Received {message}.")
        message.ack()

    def launch_consumer(self):
        print("Started consumer, listening to subscriber")
        streaming_pull_future = self.subscriber.subscribe(self.subscription_path,
                                                          callback=self.callback)
        with self.subscriber:
            try:
                # When `timeout` is not set, result() will block indefinitely,
                # unless an exception is encountered first.
                streaming_pull_future.result()
            except TimeoutError:
                print("Timeout!!!")
                streaming_pull_future.cancel()  # Trigger the shutdown.
                streaming_pull_future.result()  # Block until the shutdown is complete.
                self.tweet_queue.put("FINISHED")

    def get_sentiment(self, nlp_model_obj):
        while True:
            queue_data = self.tweet_queue.get()
            if queue_data == "FINISHED":
                break
            if type(queue_data) == bytes:
                text = json.loads(queue_data)
                sentiment_response = nlp_model_obj.run(text['text'])

                json_to_insert = {'tweet_id': text['transaction_id'],
                                  'sentiment_result': sentiment_response,
                                  'rule_name': text['rule_name']}
                errors = self.bq_client.insert_rows_json(self.bq_table_id,
                                                         [json_to_insert])
                if errors:
                    print(f"Error encountered while publishing {errors}")
                print(f"Text : {queue_data}, Sentiment response : {sentiment_response}")

    def run(self, nlp_model_obj):
        get_sentiment_th = threading.Thread(target=self.get_sentiment,
                                            args=(nlp_model_obj,))
        launch_consumer_th = threading.Thread(target=self.launch_consumer)
        get_sentiment_th.start()
        launch_consumer_th.start()
        for th in [get_sentiment_th, launch_consumer_th]:
            th.join()
        print("Successfully processed stream of tweets")


if __name__ == '__main__':
    cserv = ConsumeService()
    pl_obj = NLPModelPipeline(base_path="../config_store")
    cserv.run(pl_obj)

import tweepy
from gcp_managed.src.utilities import load_keys
import threading
import time
import sys
import json
from google.cloud import pubsub_v1
import datetime


class GatheringEngine(tweepy.StreamingClient):
    def __init__(self, secret_keys, tweet_thresh=5,
                 **kwargs):
        super().__init__(secret_keys['bearer_token'],
                         wait_on_rate_limit=kwargs['wait_on_rate_limit'])
        self.secret_keys = secret_keys

        self.tweet_thresh = tweet_thresh
        self.tweet_counter = 0

        self.change_rule = False
        self.rules_dict = kwargs['rules_dict']
        self.rules_names = list(self.rules_dict.keys())
        self.rule_counter = 0

        self.project_id = "dynamic-market-370212"
        self.topic_id = "tweets"
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

    def monitor_thread(self):
        print("starting monitor thread to check threshold")
        th = threading.Thread(target=self.add_rule)
        th.start()
        return th

    def on_tweet(self, tweet):
        print(tweet.data['id'])
        data = {'transaction_id': str(tweet.data['id']),
                'text': str(tweet.data['text']),
                'tweet_timestamp': datetime.datetime.strftime(datetime.datetime.now(),
                                                              "%d/%m/%Y %H:%M:%S"),
                'rule_name': self.rules_names[self.rule_counter]}
        data = json.dumps(data).encode("utf-8")
        self.publisher.publish(self.topic_path, data)
        print(f"Result published for : {tweet.data['id']}")

        time.sleep(5)
        self.tweet_counter += 1
        if self.tweet_counter > self.tweet_thresh:
            print("Threshold reached, changing rule")
            self.change_rule = True
            self.tweet_counter = 0
            self.rule_counter += 1

    def add_rule(self):
        print("Adding the next rule")
        while True:
            if self.change_rule:
                self.clear_rules()
                rule = self.get_next_rule()
                if rule:
                    self.add_rules(rule)
                else:
                    print("End of all rules")
                    break
            if self.rule_counter == "EXIT":
                print("End of all rules")
                sys.exit(0)

    def clear_rules(self):
        print("Removing existing rules")
        for rules_list in self.get_rules():
            if isinstance(rules_list, list):
                rule_ids = [rule.id for rule in rules_list]
                if rule_ids:
                    self.delete_rules(rule_ids)
                    print("deleted existing rules")
                break

    def get_next_rule(self):
        print("Getting the next rule")
        if self.rule_counter > len(self.rules_names):
            print("Resetting the next rule counter")
            return None
        return tweepy.StreamRule(self.rules_dict[self.rules_names[self.rule_counter]])

    def run(self):
        monitor_th = self.monitor_thread()
        self.clear_rules()
        self.filter()
        monitor_th.join()


if __name__ == '__main__':
    skeys = load_keys(path='../../config_store/.secret_keys')
    rules_dict = load_keys(path='../../config_store/rules.properties')
    streamer_obj = GatheringEngine(skeys, rules_dict=rules_dict, wait_on_rate_limit=True)
    streamer_obj.run()

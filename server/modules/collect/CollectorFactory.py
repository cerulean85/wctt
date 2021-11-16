from modules.collect.CollectorBlogNaver import CollectorBlogNaver
from modules.collect.CollectorInstagram import CollectorInstagram
from modules.collect.CollectorJoongang import CollectorJoongang
from modules.collect.CollectorTweeter import CollectorTweeter


class CollectorFactory:

    def create_instance(self, channel):
        if channel == "nav":
            return CollectorBlogNaver()

        if channel == "jna":
            return CollectorJoongang()

        if channel == "twt":
            return CollectorTweeter()

        if channel == "ins":
            return CollectorInstagram()
import json
import os

class ContextTags:
    def __init__(self, kcontext_manager):
        self.included_tags = self.load_tags_from_env()
        self.tag_color = {key: index + 1 for index, key in enumerate(self.included_tags.keys())}
        contexts = kcontext_manager.get()
        self.contexts = {context: self.parse_context_name(context) for context in contexts}
    
    def load_tags_from_env(self):
        # Access the environment variable for configuration
        tag_json = os.environ.get('K_CONTEXT_TAGS_JSON')

        # Parse the JSON string to obtain the configuration as a dictionary
        if tag_json:
            try:
                config = json.loads(tag_json)
                included_tags = config.get('included_tags', {})
                return included_tags
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON tag information \n    K_CONTEXT_TAGS_JSON={tag_json}")
                print(f"{e}")
                exit(1)
        # Use default or empty configuration if environment variable is not set or parsing fails
        return {
              "prod": "[prod]",
              "stage": "[stage]",
              "staging": "[stage]",
              "dev": "[dev]",
              "test": "[tst]",
              "demo": "[demo]",
              "west": "[west]",
              "central": "[cent]",
              "east": "[east]",
              "internal": "[int]",
              "external": "[ext]",
              "cloud": "[cld]",
              "on-prem": "[onp]",
              "app": "[app]",
              "eks": "[eks]",
              "gke": "[gke]",
              "azure": "[azr]",
          }
    
    def get_tags(self, context):
        return self.contexts.get(context, [])
    
    def get_tag_details(self, tag):
        return (self.included_tags[tag], self.tag_color.get(tag, 0))
    
    def parse_context_name(self, context):
        return [tag for tag in self.included_tags if tag in context]
    
    def get_max_tag_len(self):
        max_len = 0
        for tags in self.contexts.values():
            tag_len = sum(len(self.included_tags[tag]) for tag in tags)
            if tag_len > max_len:
                max_len = tag_len
        return max_len
    
    def sorted_contexts(self):
        return sorted(self.contexts.keys(), key=lambda x: "".join(self.contexts[x]))

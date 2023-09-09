
class KContextManager:
    def get(self):
        # Provide predefined list of contexts for testing
        return ['central-prod-red',
                'central-prod-green',
                'central-dev-red',
                'central-dev-green',
                'central-test-red',
                'central-test-green',
                'east-prod-red',
                'east-prod-green',
                'east-dev-red',
                'east-dev-green',
                'east-test-red',
                'east-test-green']


    def set(self, context):
        # Print a message for testing purposes
        print(f"Setting context to: {context}")

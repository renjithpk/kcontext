import subprocess

class KContextManager:
    def get(self):
        try:
            output = subprocess.check_output(['kubectl', 'config', 'get-contexts', '-o=name'], stderr=subprocess.STDOUT, text=True)
            # contexts = output.strip().split('\n')[1:]  # Skip the header line
            contexts = output.strip().split('\n')
            return contexts
        except subprocess.CalledProcessError:
            return []

    def set(self, context):
        try:
            subprocess.check_output(['kubectl', 'config', 'use-context', context], stderr=subprocess.STDOUT, text=True)
            return None  # No error message
        except subprocess.CalledProcessError as e:
            return str(e)

# A Stub class for validation
class StubKContextManager:
    def get(self):
        # Provide predefined list of contexts for testing
        return [
            'my-cluster-prod',
            'my-cluster-dev',
            'my-cluster-test',
            'another-cluster-prod',
            'another-cluster-dev',
            'another-cluster-test',
            'staging-cluster-prod',
            'staging-cluster-dev',
            'staging-cluster-test',
            'production-cluster',
            'development-cluster',
            'test-cluster',
            'main-cluster-prod',
            'main-cluster-dev',
            'main-cluster-test',
            'west-cluster-prod',
            'west-cluster-dev',
            'west-cluster-test',
            'east-cluster-prod',
            'east-cluster-dev',
            'east-cluster-test',
        ]
    def set(self, context):
        # Print a message for testing purposes
        print(f"Setting context to: {context}")

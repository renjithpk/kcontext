import subprocess

class KContextManager:
    def get_kube_contexts(self):
        try:
            output = subprocess.check_output(['kubectl', 'config', 'get-contexts', '-o=name'], stderr=subprocess.STDOUT, text=True)
            contexts = output.strip().split('\n')[1:]  # Skip the header line
            return contexts
        except subprocess.CalledProcessError:
            return []

    def set_kube_context(self, context):
        try:
            subprocess.check_output(['kubectl', 'config', 'use-context', context], stderr=subprocess.STDOUT, text=True)
            return None  # No error message
        except subprocess.CalledProcessError as e:
            return str(e)

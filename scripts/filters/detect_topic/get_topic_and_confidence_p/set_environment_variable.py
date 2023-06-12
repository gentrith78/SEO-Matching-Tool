import os

PATH = os.path.abspath(os.path.dirname(__file__))


def set_env_var():
    creds_path = os.path.join(PATH, 'service_account_credentials', os.listdir(os.path.join(PATH, 'service_account_credentials'))[0])
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(creds_path)

if __name__ == '__main__':
    set_env_var()



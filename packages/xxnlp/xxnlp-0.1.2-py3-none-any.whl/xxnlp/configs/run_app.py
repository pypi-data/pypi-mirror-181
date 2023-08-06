from fitlog.fastserver.app import start_app


def run_app():
    log_dir = '/mnt/Data/project/nlp-cls/logs/ERISK/erisk/'
    log_config_name = 'default.cfg'
    port = 7000
    start_app(log_dir, log_config_name, port, 1) 


if __name__ == '__main__':
    run_app()
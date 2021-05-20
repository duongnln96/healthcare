import processor
import argparse
import logging
import multiprocessing
from multiprocessing import Process

MAX_WORKER = multiprocessing.cpu_count() - 1

def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", 
                        help="Run application on local environment.\
                                By default run application on docker environment.",
                        action="store_true")
    args = parser.parse_args()

    return args


def main() -> None:
    args = argument_parser()

    appConfig = processor.GetAppConfig(args).get_app_config()
    logging.warning("App Config: {}".format(appConfig))

    num_worker = int(MAX_WORKER / 2)
    proc_list = []

    for _ in range(num_worker):
        p = Process(target=processor.Application.start, args=(appConfig,))
        p.start()
        proc_list.append(p)

    for proc in proc_list:
        proc.join()
        

if __name__ == "__main__":
    main()

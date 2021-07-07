import processor
import argparse
import multiprocessing
from multiprocessing import Process

from utils import logging

MAX_WORKER = multiprocessing.cpu_count() - 1

def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--produce",
                        help="Run produce",
                        action="store_true")

    parser.add_argument("--consume",
                    help="Run consume",
                    action="store_true")
    args = parser.parse_args()

    return args


def main() -> None:
    args = argument_parser()
    log = logging.get_logger()

    appConfig = processor.GetAppConfig().get_app_config()
    logging.info(log, "App Config: {}".format(appConfig))

    if args.produce:
        logging.info(log, "Produce is running")
        num_worker = MAX_WORKER // 2
        proc_list = []

        for _ in range(num_worker):
            p = Process(target=processor.ProduceApplication.start, args=(appConfig,))
            p.start()
            proc_list.append(p)

        for proc in proc_list:
            proc.join()
    elif args.consume:
        logging.info(log, "Consume is running")
        processor.ComsumeApplication.start(appConfig)

if __name__ == "__main__":
    main()

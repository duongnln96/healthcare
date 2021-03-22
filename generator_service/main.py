import processor
import argparse

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
    print("App Config: {}".format(appConfig))

    app = processor.Application(appConfig)
    app.start()

if __name__ == "__main__":
    main()

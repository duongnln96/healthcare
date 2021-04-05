import config
import processor

import argparse

from pyspark.sql import SparkSession

def get_spark_session():
    return SparkSession \
            .builder \
            .master("local[*]")\
            .appName("Heart_Disease_App") \
            .getOrCreate()


# def argument_parser():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--local", 
#                         help="Run application on local environment.\
#                                 By default run application on docker environment.",
#                         action="store_true")
#     args = parser.parse_args()

#     return args


def main() -> None:
    # args = argument_parser()

    appConfig = config.GetAppConfig().get_app_config()
    print("App Config: {}".format(appConfig))

    app = processor.HealthCareApplication(appConfig, get_spark_session())
    app.start()


if __name__ == "__main__":
    main()

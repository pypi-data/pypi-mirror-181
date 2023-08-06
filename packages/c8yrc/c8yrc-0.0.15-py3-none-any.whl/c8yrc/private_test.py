import json
import logging
import sys
import time
import traceback

from c8yrc.rest_client import CumulocityClient
from c8yrc.rest_client.c8y_exception import C8yException
from c8yrc.rest_client.c8y_rest_client import C8yRestClient

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # my_device_address = '2102351HNDDMK2000759'.lower()
    _tenant = 't2700'
    # device = f'cb1-{my_device_address}'.strip()
    _host = 'main.dm-zz-q.ioee10-cloud.com'
    rest_user_name = 'service_schindler-jenkins'
    rest_user_password = '2txFLPmgE5xwWRovG7nW7e4Y94XhwOB3'
    device_type = 'cb4'
    device_serial_number = 'a1eucpg1qb2206001162'

    # client = CumulocityClient(hostname=_host, tenant=_tenant, user=rest_user_name, password=rest_user_password)
    # session = client.retrieve_token()
    # client.get_firmware_info(device, 'c8y_Serial')

    try:
        # client.upload_firmware(artifact_file_location=
        #             '/home/jenkins/packages/images/4.1.0_2022-12-01-1058_cube-imx8-c8y-buster-arm64-schindler.mender',
        #             metadata_file_location='/home/jenkins/packages/images/4.1.0_2022-12-01-1058_cube-imx8-c8y-buster-arm64-schindler.json')

        c8y_serial_number = f'{device_type}-{device_serial_number}'.lower()
        my_c8y_api = C8yRestClient(c8y_serial_number=c8y_serial_number,
                                   user=rest_user_name, password=rest_user_password,
                                   url='https://main.dm-zz-q.ioee10-cloud.com/', tenant='t2700')
        my_c8y_api.start_proxy(port)
        time.sleep(10)
        my_c8y_api.stop_proxy()

    except C8yException as e:
        traceback.print_exc()
        sys.exit(-1)


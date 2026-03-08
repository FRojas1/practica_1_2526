import sys

import rclpy
from rclpy.node import Node

from interfaz.srv import TempConversion


class TempConversionClient(Node):

    def __init__(self):
        super().__init__('temp_conversion_client')
        self.cli = self.create_client(TempConversion, 'convert_temperature')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')
        self.req = TempConversion.Request()

    def send_request(self, temp, conversion_type):
        self.req.input_temp = float(temp)
        self.req.conversion_type = conversion_type
        return self.cli.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)
    client = TempConversionClient()

    temp = float(sys.argv[1])
    conversion_type = sys.argv[2]

    future = client.send_request(temp, conversion_type)
    rclpy.spin_until_future_complete(client, future)
    response = future.result()

    if conversion_type == 'Cel_to_Far':
        client.get_logger().info(f'{temp}°C = {response.converted_temp}°F')
    else:
        client.get_logger().info(f'{temp}°F = {response.converted_temp}°C')

    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

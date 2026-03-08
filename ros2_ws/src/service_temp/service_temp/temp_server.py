import rclpy
from rclpy.node import Node

from interfaz.srv import TempConversion


class TempConversionServer(Node):

    def __init__(self):
        super().__init__('temp_conversion_server')
        self.srv = self.create_service(
            TempConversion, 'convert_temperature', self.convert_callback)
        self.get_logger().info('Temperature conversion server ready.')

    def convert_callback(self, request, response):
        if request.conversion_type == 'Cel_to_Far':
            response.converted_temp = request.input_temp * 9.0 / 5.0 + 32.0
            self.get_logger().info(
                f'{request.input_temp}°C -> {response.converted_temp}°F')
        elif request.conversion_type == 'Far_to_Cel':
            response.converted_temp = (request.input_temp - 32.0) * 5.0 / 9.0
            self.get_logger().info(
                f'{request.input_temp}°F -> {response.converted_temp}°C')
        else:
            self.get_logger().warn(
                f'Unknown conversion type: {request.conversion_type}')
            response.converted_temp = 0.0
        return response


def main(args=None):
    rclpy.init(args=args)
    node = TempConversionServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

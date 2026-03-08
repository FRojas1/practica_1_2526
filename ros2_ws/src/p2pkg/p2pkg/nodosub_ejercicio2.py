import rclpy
from rclpy.node import Node

from interfaz.msg import P2pkgMensaje


class SubscriberEjercicio2(Node):

    def __init__(self):
        super().__init__('nodosub_ejercicio2')
        self.subscription = self.create_subscription(
            P2pkgMensaje,
            '/topic_ejercicio2',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        self.get_logger().info(
            f'Recibido: fecha={msg.fecha}, numero={msg.numero}, '
            f'posicion.position.x={msg.posicion.position.x:.4f}, '
            f'posicion.orientation.w={msg.posicion.orientation.w:.4f}')


def main(args=None):
    rclpy.init(args=args)
    node = SubscriberEjercicio2()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

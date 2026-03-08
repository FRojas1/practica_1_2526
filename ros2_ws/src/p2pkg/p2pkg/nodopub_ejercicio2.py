import rclpy
from rclpy.node import Node
from random import random
from datetime import datetime

from interfaz.msg import P2pkgMensaje
from geometry_msgs.msg import Pose, Point, Quaternion


class PublisherEjercicio2(Node):

    def __init__(self):
        super().__init__('nodopub_ejercicio2')
        self.declare_parameter('numero', 5)
        self.publisher_ = self.create_publisher(P2pkgMensaje, '/topic_ejercicio2', 10)
        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = P2pkgMensaje()
        msg.numero = self.get_parameter('numero').get_parameter_value().integer_value
        msg.fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg.posicion = Pose(
            position=Point(x=random(), y=random(), z=random()),
            orientation=Quaternion(x=random(), y=random(), z=random(), w=random())
        )
        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Enviando: fecha={msg.fecha}, numero={msg.numero}, '
            f'posicion.position.x={msg.posicion.position.x:.4f}, '
            f'posicion.orientation.w={msg.posicion.orientation.w:.4f}')


def main(args=None):
    rclpy.init(args=args)
    node = PublisherEjercicio2()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

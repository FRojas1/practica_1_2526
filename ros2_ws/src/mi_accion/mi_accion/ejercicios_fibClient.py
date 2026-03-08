import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from std_msgs.msg import String

from interfaz.action import EjFibonacci


class EjFibonacciActionClient(Node):

    def __init__(self):
        super().__init__('ej_fibonacci_action_client')
        self._action_client = ActionClient(self, EjFibonacci, 'ej_fibonacci')
        self._estado_pub = self.create_publisher(String, '/estado_accion', 10)
        self.declare_parameter('orden', 5)

    def send_goal(self):
        orden = self.get_parameter('orden').get_parameter_value().integer_value
        goal_msg = EjFibonacci.Goal()
        goal_msg.orden = orden

        self._action_client.wait_for_server()
        self.get_logger().info(f'Sending goal: orden={orden}')

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {list(result.secuencia_final)}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Received feedback: {feedback.feedback_valor:.4f}')
        msg = String()
        msg.data = 'en proceso'
        self._estado_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    client = EjFibonacciActionClient()
    client.send_goal()
    rclpy.spin(client)


if __name__ == '__main__':
    main()

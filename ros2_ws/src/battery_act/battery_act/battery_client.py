import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from interfaz.action import BatteryAction


class BatteryClient(Node):

    def __init__(self):
        super().__init__('battery_client')
        self._action_client = ActionClient(self, BatteryAction, 'battery_action')
        self.declare_parameter('target_percentage', 20)

    def send_goal(self):
        target = self.get_parameter('target_percentage').get_parameter_value().integer_value
        goal_msg = BatteryAction.Goal()
        goal_msg.target_percentage = target

        self._action_client.wait_for_server()
        self.get_logger().info(f'Sending goal: target_percentage={target}%')

        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.warning}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        current = feedback_msg.feedback.current_percentage
        self.get_logger().info(f'Feedback: Battery at {current}%')


def main(args=None):
    rclpy.init(args=args)
    client = BatteryClient()
    client.send_goal()
    rclpy.spin(client)


if __name__ == '__main__':
    main()

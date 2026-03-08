import time

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node

from interfaz.action import BatteryAction


class BatteryChargerServer(Node):

    def __init__(self):
        super().__init__('battery_charger')
        self._action_server = ActionServer(
            self,
            BatteryAction,
            'battery_action',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback)
        self.get_logger().info('Battery charger server ready.')

    def goal_callback(self, goal_request):
        self.get_logger().info(
            f'Received goal: target_percentage={goal_request.target_percentage}%')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing battery discharge simulation...')
        current = 100
        target = goal_handle.request.target_percentage
        feedback_msg = BatteryAction.Feedback()

        while current > target:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled!')
                result = BatteryAction.Result()
                result.warning = 'Acción cancelada'
                return result

            current -= 5
            feedback_msg.current_percentage = current
            self.get_logger().info(f'Battery: {current}%')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()
        result = BatteryAction.Result()
        result.warning = 'Batería Baja, por favor cargue el robot!'
        return result


def main(args=None):
    rclpy.init(args=args)
    server = BatteryChargerServer()
    rclpy.spin(server)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

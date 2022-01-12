import sys
import rclpy
from rclpy.node import Node

from arimetic_operator.srv import ArithmeticOperator

class CustomServiceClient(Node):

    def __init__(self):
        super().__init__('custom_service_client')
        self.client = self.create_client(ArithmeticOperator, 'ArithmeticCalculation') # Client builder 패턴
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for custom service server...')
        self.req = ArithmeticOperator.Request()

    def send_request(self):
        print('len(sys.argv) : ', len(sys.argv))
        self.req.num1 = float(sys.argv[1])
        self.req.num2 = float(sys.argv[2])
        self.req.operation_kind = sys.argv[3]
        self.future = self.client.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)

    custom_service_client = CustomServiceClient()
    custom_service_client.send_request()

    while rclpy.ok():
        rclpy.spin_once(custom_service_client)
        # future가 done 상태가 되면 다음 if문을 실행합니다
        if custom_service_client.future.done():
            try:
                response = custom_service_client.future.result()
            except Exception as e:
                custom_service_client.get_logger().info(
                    'Service call failed: %r' % (e,))
            else:
                if response.is_success:
                    custom_service_client.get_logger().info('Success(%s)' % response.returnval)
                else:
                    custom_service_client.get_logger().info('Failed(%s)' % custom_service_client.req.operation_kind)

                break

    custom_service_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
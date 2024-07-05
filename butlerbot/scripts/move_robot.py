#! /usr/bin/env python3
import rclpy
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
import rclpy.action
from rclpy.node import Node
import time
import rclpy
from action_msgs.msg import GoalStatus

class MoveRobot(Node):
    def __init__(self):
        super().__init__('MoveRobot')
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.current_goal_done = False
        self.process()
        
    def process(self):
        input_str = input('\n### USER ####\nDo you want to order anything (Y/N): ')
        if input_str=='Y' or input_str=='y':
            order = []
            canc = False    
            nos = input('\n### USER ####\nEnter the Table Numbers: ').split(' ')
            nos = list(map(int,nos))  
            nos.sort(); order = order+nos;
            print(order)
            print(f'Order placed for Table {str(order)}')
            
            self.move_to_kitchen()
            
            now = time.time()
            future = now+10
            while True: 
                
                c = input('\n### USER ####\nThe Order is preparing..Would you like to cancel the order(Y/N) ? ')
                if c == 'y' or c =='Y':
                    print('Order is Cancelled')
                    self.move_to_home()
                    break
                             
                conf = input('\n### KITCHEN ####\nPress y for confirmation: ')
                now = time.time()
                future= now+10
                if now>future:
                    print('Timed Out. Returning Home')
                    self.move_to_home()
                    break
                
                if conf == 'y' or conf == 'Y':
                    print('Robot is moving to table')
                    c = input('\n### USER ####\nThe Order is Delivering...Would you like to cancel any of the order(Y/N) ? ')
                    if c == 'y' or c =='Y':
                        canc = True
                        cn = input('\n### USER ####\nEnter the Table Numbers to cancel: ').split(' ')
                        cn = list(map(int,cn)) 
                        for i,j in enumerate(cn):
                            order.remove(j)
                    
                    for i in range(len(order)):
                        
                        if order[i] ==1:
                            print(f'Moving to {order[i]} th table')
                            self.move_to_tableone()
                            att = self.confirm_order()
                            if att:
                                print('Order Delivered')
                            else:
                                cafe = False
                                print('Time Out. Skipping the table')
                                
                        elif order[i] ==2:
                            print(f'Moving to {order[i]} th table')
                            self.move_to_tabletwo()
                            att = self.confirm_order()
                            if att:
                                print('Order Delivered')
                            else:
                                canc = False
                                print('Time Out. Skipping the table')
                            
                        elif order[i]==3:
                            print(f'Moving to {order[i]} th table')
                            self.move_to_tablethree()
                            att = self.confirm_order()
                            if att:
                                print('Order Delivered')
                            else:
                                canc = False
                                print('Time Out. Skipping the table')
                     
                    if canc == True:
                        print('Moving to Kitchen and then Home')
                        self.move_to_kitchen()
                    self.move_to_home()
                    break
                else:
                    print('Robot moving to home')
                    self.move_to_home()
                    break
                
    def confirm_order(self):
        now = time.time()
        future = now+10
        attend = int(input('\n### USER ####\nPls Press 1 to Confirm the Order: ')) 
        now = time.time()
        if now>future:
            print('Time Out')
            return False     
        else:
            if attend==1:
                return True
            else:
                return False
                
    def move_to_kitchen(self):
        self.get_logger().info('Moving to Kitchen')
        self.move_to_position(6.0,0.0,0.0)
    
    def move_to_tabletwo(self):
        self.get_logger().info('Moving to table Two')
        self.move_to_position(-18.06,-3.13,-0.707)
            
    def move_to_tablethree(self):
        self.get_logger().info('Moving to table Three')
        self.move_to_position(-18.27,2.83,-0.707)
        
    def move_to_tableone(self):
        self.get_logger().info('Moving to table One')
        self.move_to_position(-9.84,-2.68,0.707)
    
    def move_to_home(self):
        self.get_logger().info('Moving to Home')
        self.move_to_position(-2.96,7.05,0.0)

    def move_to_position(self, x, y, z):
        self.current_goal_done = False
        goal_pose = NavigateToPose.Goal()
        goal_pose.pose.header.frame_id = 'map'
        goal_pose.pose.pose.position.x = x
        goal_pose.pose.pose.position.y = y
        goal_pose.pose.pose.orientation.z = z
        self.action_client.wait_for_server()
        send_goal_future = self.action_client.send_goal_async(goal_pose, feedback_callback=self.feedback_callback)
        send_goal_future.add_done_callback(self.goal_response_callback)
        
        while not self.current_goal_done:
            rclpy.spin_once(self)
            
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        #self.get_logger().info('FEEDBACK:' + str(feedback) )
        
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            self.current_goal_done = True
            return
        self.get_logger().info('Goal accepted')

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._wait_for_result)

    def _wait_for_result(self, result_future):
        result = result_future.result()
        if result.status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded!')
        else:
            self.get_logger().info('Goal failed with status: {0}'.format(result.status))
        self.current_goal_done = True
        
def main(args=None):
    rclpy.init(args=args)
    robot = MoveRobot()
    rclpy.spin(robot)
    
if __name__ == '__main__':
    main()
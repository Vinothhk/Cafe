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
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')   #Create an Action Client
        self.current_goal_done = False
        self.process()
        
    def process(self):                  #Interacts with USER (under ### USER ####) and Kitchen side (### KITCHEN ####)
        input_str = input('\n### USER ####\nDo you want to order anything (Y/N): ')   
        if input_str=='Y' or input_str=='y':
            order = []                  #To store the numbers of ordered tables  
            canc = False                #BOOL VALUE. (TRUE - if any order get cancel or robot is not attended at the table)
            nos = input('\n### USER ####\nEnter the Table Numbers: ').split(' ')
            nos = list(map(int,nos))  
            nos.sort(); order = order+nos;
            print(f'Order placed for Table {str(order)}')
            
            self.move_to_kitchen()      #Moves to Kitchen once any order is placed
            
            now = time.time()
            future = now+10
            while True: 
                
                c = input('\n### USER ####\nThe Order is preparing..Would you like to cancel the order(Y/N) ? ')
                if c == 'y' or c =='Y':
                    print('Order is Cancelled')
                    self.move_to_home()
                    break
                             
                conf = input('\n### KITCHEN ####\nPress y for confirmation: ')    #Asks Confirmation in Kitchen
                now = time.time()
                future= now+10
                if now>future:                                                    #Time Out in Kitchen if not confirmed within 10 second & then robot moves to Home
                    print('Timed Out. Returning Home')
                    self.move_to_home()
                    break
                
                if conf == 'y' or conf == 'Y':
                    print('Robot is moving to table')
                    c = input('\n### USER ####\nThe Order is Delivering...Would you like to cancel any of the order(Y/N) ? ')
                    if c == 'y' or c =='Y':
                        canc = True   
                        cn = input('\n### USER ####\nEnter the Table Numbers to cancel: ').split(' ')           #Gets the table number for which the order has to cancelled
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
                                canc =True
                                print('Skipping the table')
                                
                        elif order[i] ==2:
                            print(f'Moving to {order[i]} th table')
                            self.move_to_tabletwo()
                            att = self.confirm_order()
                            if att:
                                print('Order Delivered')
                            else:
                                canc = True
                                print('Skipping the table')
                            
                        elif order[i]==3:
                            print(f'Moving to {order[i]} th table')
                            self.move_to_tablethree()
                            att = self.confirm_order()
                            if att:
                                print('Order Delivered')
                            else:
                                canc = True
                                print('Skipping the table')
                     
                    if canc == True:               #If any table didnt response to the order (or) any order cancelled
                        print('Moving to Kitchen and then Home')
                        self.move_to_kitchen()
                    self.move_to_home()
                    break
                else:                              #If not confirmed in the kitchen
                    print('Robot moving to home')
                    self.move_to_home()
                    break
                
    def confirm_order(self): #Asks Confirmation in table. Time out if response is not within 10 seconds
        now = time.time()
        future = now+10
        attend = int(input('\n### USER ####\nPls Press 1 to Confirm the Order: ')) 
        now = time.time()
        if now>future:
            print('Time Out')
            return False     
        else:
            if attend==1:
                return True            #Returns True When order is successfully attended at the table
            else:
                return False
                
    def move_to_kitchen(self):       #Sending goal pose of Kitchen coordinates
        self.get_logger().info('Moving to Kitchen')
        self.move_to_position(6.0,0.0,0.0)
    
    def move_to_tabletwo(self):      #Sending goal pose of Table 2
        self.get_logger().info('Moving to table Two')
        self.move_to_position(-18.06,-3.13,-0.707)
            
    def move_to_tablethree(self):    #Sending goal pose of Table 3
        self.get_logger().info('Moving to table Three')
        self.move_to_position(-18.27,2.83,0.707)
        
    def move_to_tableone(self):      #Sending goal pose of Table 1
        self.get_logger().info('Moving to table One')
        self.move_to_position(-9.84,-2.68,-0.707)
    
    def move_to_home(self):          #Sending goal pose of Home Position
        self.get_logger().info('Moving to Home')
        self.move_to_position(-2.96,7.05,0.0)

    def move_to_position(self, x, y, z):   #Sends a navigation goal to the action server, 
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
            
    def feedback_callback(self, feedback_msg): #process feedback from the Action Server
        feedback = feedback_msg.feedback
        #self.get_logger().info('FEEDBACK:' + str(feedback))   
        
    def goal_response_callback(self, future):  #Invoked when the action server responds to the goal request. Checks whether the goal was accepted or rejected.
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            self.current_goal_done = True
            return
        self.get_logger().info('Goal accepted')

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self._wait_for_result)

    def _wait_for_result(self, result_future):  #Called when the action server finishes processing the goal. retrieves and logs the result of the goal execution.
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
import time
while True:
    input_str = input('\n### USER ####\nDo you want to order anything (Y/N): ')

    if input_str=='Y' or input_str=='y':
        order = []
        canc = []
        cond = []
        nos = input('\n### USER ####\nEnter the Table Numbers: ').split(' ')
        nos = list(map(int,nos))  
        nos.sort(); order = order+nos;
        print(order)
        
        ''' ROBOT MOVING TO KITCHEN'''
        now = time.time()
        future = now+10
        while True:
            
            conf = input('\n### KITCHEN ####\nPress y for confirmation: ')
            now = time.time()
            if now>future:
                print('Timed Out. Returning Home')
                break
            if conf == 'y' or conf == 'Y':
                print('Robot is moving to table')
                c = input('\n### USER ####\nThe Order is Delivering...Would you like to cancel any of the order(Y/N) ? ')
                if c == 'y' or c =='Y':
                    cn = input('\n### USER ####\nEnter the Table Numbers to cancel: ').split(' ')
                    cn = list(map(int,cn)) 
                    for i,j in enumerate(cn):
                        order.remove(j)
                print(order)
                for i in range(len(order)):
                    if order[i] ==1:
                        print(f'Moving to {order[i]} th table')
                    elif order[i] ==2:
                        print(f'Moving to {order[i]} th table')
                    elif order[i]==3:
                        print(f'Moving to {order[i]} th table')
                print('Moving to Home')
                          
                break
            else:
                print('Robot moving to home')
                break
            
            
            
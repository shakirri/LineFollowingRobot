from controller import Robot
robot = Robot()

timestep = int(robot.getBasicTimeStep())

last_error=0
error=0
p=0
i=0
d=0
kp=.98  #.98, 
ki=0
kd=1.5
max_speed=5

#flw=left_front_wheel
#frw=right_front_wheel
#blw=back_left_wheel
#brw=back_right_wheel

flw=robot.getDevice("wheel1")
frw=robot.getDevice("wheel2")
blw=robot.getDevice("wheel3")
brw=robot.getDevice("wheel4")

flw.setPosition(float('inf'))
blw.setPosition(float('inf'))
frw.setPosition(float('inf'))
brw.setPosition(float('inf'))

flw.setVelocity(0.0)
blw.setVelocity(0.0)
frw.setVelocity(0.0)
brw.setVelocity(0.0)

#ir_initialize:
rir=robot.getDevice('left')
rir.enable(timestep)

mir=robot.getDevice('mid')
mir.enable(timestep)

lir=robot.getDevice('right')
lir.enable(timestep)
left_speed=max_speed
right_speed=max_speed

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:

   lir_val=rir.getValue()
   mir_val=mir.getValue()
   rir_val=lir.getValue()
   
   print("left: {} mid: {} right: {} ".format(lir_val,mir_val,rir_val))
   #sensor_threshold_value
   #less than 950 off track
   #>=950 on the track
   t=1000
   if(rir_val<t and lir_val<t and mir_val>=t):
       error=0
       print("mid:ok 1st if")
   elif(rir_val<t and lir_val>=t and mir_val<t):
       error=2
       print("lir ok 2nd if")
   elif(rir_val<t and lir_val>=t and mir_val>=t):
       error=1
       print("lir and mir ok 3rd if")
   elif(rir_val>=t and lir_val<t and mir_val>=t):
       error=-1
       print("rir and mir ok 4th if")
   elif(rir_val>=t and lir_val<t and mir_val<t):
       error=-2
       print("only rir ok 5th if")
    
   last_error = error
   p=error 
   i=error + i 
   d=error-last_error
   balance=int(kp *p)+int(ki*i)+int(kd*d)
   last_error = error 
   left_speed = max_speed - balance 
   right_speed = max_speed + balance
   print("balance {} left speed {} right speed {}".format(balance,left_speed,right_speed))
   print("Last Error:",last_error)
   
   if right_speed == max_speed :
         flw.setVelocity(left_speed)
         frw.setVelocity(right_speed)
         blw.setVelocity(left_speed)
         brw.setVelocity(right_speed) 
         print("in case 1")
         
         
   #error = balance >0 and moving to the left   
   if right_speed > max_speed:    #leftTurn
         flw.setVelocity(0)
         frw.setVelocity(right_speed)
         blw.setVelocity(0)
         brw.setVelocity(right_speed)
         print("in case 2") 
            
      
   if left_speed > max_speed:
         flw.setVelocity(left_speed)
         frw.setVelocity(0)
         blw.setVelocity(left_speed)
         brw.setVelocity(0)
         print("case 3")
"""
Evaluation Agent.
"""

import time
import numpy as np
from device.robot.flexiv import FlexivRobot
from utils.transformation import xyz_rot_transform
from device.gripper.dahuan import DahuanModbusGripper
from device.camera.realsense import RealSenseRGBDCamera
from device.sensor.opto import OptoForceFTSensorWithHistory

class Agent:
    """
    Evaluation agent with Flexiv arm, Dahuan gripper and Intel RealSense RGB-D camera.

    Follow the implementation here to create your own real-world evaluation agent.
    """
    def __init__(
        self,
        robot_ip,
        pc_ip,
        gripper_port,
        camera_serial,
        num_obs_force = 100,
        **kwargs
    ): 
        self.camera_serial = camera_serial

        print("Init robot, gripper, sensor, and camera.")
        self.robot = FlexivRobot(robot_ip_address = robot_ip, pc_ip_address = pc_ip)
        self.robot.send_tcp_pose(self.ready_pose)
        time.sleep(1.5)
        
        self.gripper = DahuanModbusGripper(port = gripper_port)
        self.gripper.set_force(30)
        self.gripper.set_width(0)
        time.sleep(0.5)

        self.sensor = OptoForceFTSensorWithHistory(history_size = num_obs_force)
        self.sensor.streaming()
        time.sleep(1.0)
        
        self.camera = RealSenseRGBDCamera(serial = camera_serial)
        for _ in range(30): 
            self.camera.get_rgbd_image()
        
        print("Initialization Finished.")
        
    
    @property
    def intrinsics(self):
        return np.array([
            [922.37457275, 0, 637.55419922, 0],
            [0, 922.46069336, 368.37557983, 0],
            [0, 0, 1, 0]
        ])
    
    @property
    def ready_pose(self):
        return np.array([0.5, 0.0, 0.17, 0.0, 0.0, 1.0, 0.0])

    @property
    def ready_rot_6d(self):
        return np.array([-1, 0, 0, 0, 1, 0])

    def get_observation(self):
        colors, depths = self.camera.get_rgbd_image()
        return colors, depths
    
    def get_force_torque_history(self, freq = 100):
        return self.sensor.getHistoryfreq(freq=freq)

    def get_force_torque(self):
        return self.get_force_torque_history()[-1]

    def get_force(self):
        return self.get_force_torque()[:3]
    
    def get_torque(self):
        return self.get_force_torque()[3:]  
    
    def get_force_torque_value(self):
        ft = self.get_force_torque()
        return np.sqrt(np.sum(ft[:3] ** 2, axis = -1)), np.sqrt(np.sum(ft[3:] ** 2, axis = -1))
    
    def get_force_value(self):
        force = self.get_force()
        return np.sqrt(np.sum(force ** 2, axis = -1))

    def get_torque_value(self):
        torque = self.get_torque()
        return np.sqrt(np.sum(torque ** 2, axis = -1))
    
    def get_tcp_pose(self):
        return self.robot.get_tcp_pose()
    
    def set_tcp_pose(self, pose, rotation_rep, rotation_rep_convention = None, blocking = False):
        tcp_pose = xyz_rot_transform(
            pose,
            from_rep = rotation_rep, 
            to_rep = "quaternion",
            from_convention = rotation_rep_convention
        )
        # print("next action:", tcp_pose)
        # input()
        self.robot.send_tcp_pose(tcp_pose)
        if blocking:
            time.sleep(0.1)
    
    def set_gripper_width(self, width, blocking = False):
        width = int(np.clip(width / 0.095 * 1000., 0, 1000))
        self.gripper.set_width(width)
        if blocking:
            time.sleep(0.5)
    
    def stop(self):
        self.sensor.stop_streaming()
        self.robot.stop()
    
#! /usr/bin/env python
"""
This script tests the PR2 torso armature joint
"""

from morse.testing.testing import MorseTestCase

# Include this import to be able to use your test file as a regular 
# builder script, ie, usable with: 'morse [run|exec] base_testing.py
try:
    from morse.builder import *
except ImportError:
    pass

import sys
from pymorse import Morse

PR2_JOINTS = {'head_pan', 'head_tilt', 'l_shoulder_pan', 'l_shoulder_lift', 'l_upper_arm', 'l_elbow', 'l_forearm', 'l_wrist_flex', 'l_wrist_roll', 'r_shoulder_pan', 'r_shoulder_lift', 'r_upper_arm', 'r_elbow', 'r_forearm', 'r_wrist_flex', 'r_wrist_roll', 'torso_lift_joint', 'laser_tilt_mount_joint', 'fl_caster_rotation_joint', 'fl_caster_l_wheel_joint', 'fl_caster_r_wheel_joint', 'fr_caster_rotation_joint', 'fr_caster_l_wheel_joint', 'fr_caster_r_wheel_joint', 'bl_caster_rotation_joint', 'bl_caster_l_wheel_joint', 'bl_caster_r_wheel_joint', 'br_caster_rotation_joint', 'br_caster_l_wheel_joint', 'br_caster_r_wheel_joint', 'r_gripper_motor_slider_joint', 'r_gripper_motor_screw_joint', 'r_gripper_l_finger_joint', 'r_gripper_r_finger_joint', 'r_gripper_l_finger_tip_joint', 'r_gripper_r_finger_tip_joint', 'r_gripper_joint', 'l_gripper_motor_slider_joint', 'l_gripper_motor_screw_joint', 'l_gripper_l_finger_joint', 'l_gripper_r_finger_joint', 'l_gripper_l_finger_tip_joint', 'l_gripper_r_finger_tip_joint', 'l_gripper_joint', 'torso_lift_motor_screw_joint', 'head_pan_joint', 'head_tilt_joint', 'l_shoulder_pan_joint', 'l_shoulder_lift_joint', 'l_upper_arm_roll_joint', 'l_elbow_flex_joint', 'l_forearm_roll_joint', 'l_wrist_flex_joint', 'l_wrist_roll_joint', 'r_shoulder_pan_joint', 'r_shoulder_lift_joint', 'r_upper_arm_roll_joint', 'r_elbow_flex_joint', 'r_forearm_roll_joint', 'r_wrist_flex_joint', 'r_wrist_roll_joint'}


class PR2TorsoTest(MorseTestCase):

    def setUpEnv(self):
        from morse.builder.robots import PR2
        pr2 = PR2()
        pr2.add_interface("socket")

        env = Environment('empty', fastmode=True)
        env.aim_camera([1.0470, 0, 0.7854])

    def test_joints(self):

        with Morse() as simu:
            joints = simu.pr2.joint_state.get()

            self.assertEqual(len(set(joints.keys())), len(joints.keys()), 'Some joints are duplicated!' )
            self.assertEqual(set(joints.keys()), PR2_JOINTS, 'Could not find all joints of the PR2. Please check if you named the joints correctly in your pr2_posture sensor and middleware!' )

########################## Run these tests ##########################
if __name__ == "__main__":
    import unittest
    from morse.testing.testing import MorseTestRunner
    suite = unittest.TestLoader().loadTestsFromTestCase(PR2TorsoTest)
    sys.exit(not MorseTestRunner().run(suite).wasSuccessful())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 21:36:24 2022

@author: florence
"""

import unittest
from PET_Dosage import main

#%% Main Function Test

import unittest
from PET_Dosage import main

class testpet(unittest.TestCase):
    
    def test_main(self):
        result_main = main
        
    def test_volume(self):
        result_volume = finding_volume(mass, location)
        self.assertEqual(result_volume, mass*density)
        
        self.assertEqual(result_main, moles)
        
    def test_radioactivity(self):
        result_radioactivity = finding_radioactivity_from_curies(necessary_radioactivity_mCi, disintegrations, conversion_cm_to_m)
        self.assertEqual(result_radioactivity, 37000000000000)
        
    def test_moles(self):
        result_moles = finding_moles(volume, radioactivity, AN)
        self.assertEqual(result_moles, moles)
        
    def test_time(self):
        result_time = Time_of_scan(t_half, desired_percentage)
        self.assertEqual(result_time, 44.5828691966538)
        
if __name__ == "__main__":
    unittest.main()
    print('Main Moles Passed')
                    
if __name__ == "__main__":
    unittest.main()
    print('Main t Passed')

if __name__ == "__main__":
    unittest.main()
    print('Volume Passed')

if __name__ == "__main__":
    unittest.main()
    print('Radioactivity Passed')

if __name__ == "__main__":
    unittest.main()
    print('Moles Passed')
    
if __name__ == "__main__":
    unittest.main()
    print('Time Passed')
    
test_object_main = testpet(unittest.TestCase)
test_object_main.test_main() 
    
test_object_volume = testpet(unittest.TestCase)
test_object_volume.test_volume()
    
test_object_radioactivity = testpet(unittest.TestCase)
test_obj_radioactivity.test_radioactivity()
    
test_object_moles = testpet(unittest.TestCase)
test_obj_moles.test_moles()
    
test_object_time = testpet(unittest.TestCase)
test_object_time.test_time()


#%% Volume Test

class test_volume(unittest.TestCase):
    
    def test_volume_def(self, volume):
        result_volume = finding_volume(mass, location)
        self.assertEqual(result_volume, mass*density)
        
if __name__ == "__main__":
    unittest.main()
    print('Volume Passed')

#%% Radioactivity Test

class test_radioactivity(unittest.TestCase):

    def test_radioactivity_def(self, radioactivity):
        result_radioactivity = finding_radioactivity_from_curies(necessary_radioactivity_mCi, disintegrations, conversion_cm_to_m)
        self.assertEqual(result_radioactivity, 37000000000000)
    
if __name__ == "__main__":
    unittest.main()
    print('Radioactivity Passed')
    
#%% Moles Test

class test_moles(unittest.TestCase):
    
    def test_moles(self, moles):
        result_moles = finding_moles(volume, radioactivity, AN)
        self.assertEqual(result_moles, moles)
    
if __name__ == "__main__":
    unittest.main()
    print('Moles Passed')
    
#%% Time Test

class test_time(unittest.TestCase):

    def test_time_def(self, time):
        result_time = Time_of_scan(t_half, desired_percentage)
        self.assertEqual(result_time, 44.5828691966538)

if __name__ == "__main__":
    unittest.main()
    print('Time Passed')
    
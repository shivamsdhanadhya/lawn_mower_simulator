# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from src.simulator import Simulator

# Create your models here.
class SimulatorDriver(models.Model):

    #def __str__(self):
    #    return self.summary

    def __init__(self, file_name):
        self.simulator = Simulator()
        self.simulator.process_input(file_name)
        self.simulator.setup()

    def get_data(self):
        return self.simulator.get_mdata_for_gui()

    def next_move(self):
        self.simulator.make_simulation_turn()

    def fast_forward(self):
        self.simulator.fast_forward()

    def stop(self):
        self.simulator.stop_simulation()

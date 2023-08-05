#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DataVisual import XParameter


g = XParameter(Name='g', Format="<20s", Unit="1", LongLabel='Anisotropy coefficient', Legend='g', Type=float)
Coupling = XParameter(Name='Coupling', Format="<20s", Unit="Watt", LongLabel='Coupling', Legend='Coupling', Type=float)

Qsca = XParameter(Name='Qsca', Format="<20s", Unit="1", LongLabel='Scattering efficiency', Legend='Qsca', Type=float)
Qext = XParameter(Name='Qext', Format="<20s", Unit="1", LongLabel='Extinction efficiency', Legend='Qext', Type=float)
Qabs = XParameter(Name='Qabs', Format="<20s", Unit="1", LongLabel='Absorption efficiency', Legend='Qabs', Type=float)
Qratio = XParameter(Name='Qratio', Format="<20s", Unit="1", LongLabel='Ratio efficiency', Legend='Qratio', Type=float)
Qback = XParameter(Name='Qback', Format="<20s", Unit="1", LongLabel='Backward efficiency', Legend='Qback', Type=float)
Qforw = XParameter(Name='Qforw', Format="<20s", Unit="1", LongLabel='Forward efficiency', Legend='Qforw', Type=float)
Qpr = XParameter(Name='Qpr', Format="<20s", Unit="1", LongLabel='Radiation pressure efficiency', Legend='Qpr', Type=float)

Csca = XParameter(Name='Csca', Format="<20s", Unit="m^2", LongLabel='Scattering cross-section', Legend='Csca', Type=float)
Cext = XParameter(Name='Cext', Format="<20s", Unit="m^2", LongLabel='Extinction cross-section', Legend='Cext', Type=float)
Cabs = XParameter(Name='Cabs', Format="<20s", Unit="m^2", LongLabel='Absorption cross-section', Legend='Cabs', Type=float)
Cratio = XParameter(Name='Cratio', Format="<20s", Unit="m^2", LongLabel='Ratio cross-section', Legend='Cratio', Type=float)
Cback = XParameter(Name='Cback', Format="<20s", Unit="m^2", LongLabel='Backward cross-section', Legend='Cback', Type=float)
Cforw = XParameter(Name='Cforw', Format="<20s", Unit="m^2", LongLabel='Forward cross-section', Legend='Cforw', Type=float)
Cpr = XParameter(Name='Cpr', Format="<20s", Unit="m^2", LongLabel='Radiation pressure cross-section', Legend='Cpr', Type=float)

a1 = XParameter(Name='a1', Format="<20s", Unit="", LongLabel='Electric dipole coefficient', Type=float)
a2 = XParameter(Name='a2', Format="<20s", Unit="", LongLabel='Electric quadrupole coefficient', Type=float)
a3 = XParameter(Name='a3', Format="<20s", Unit="", LongLabel='Electric octopole coeffcient', Type=float)
b1 = XParameter(Name='b1', Format="<20s", Unit="", LongLabel='Magnertic dipole coefficient', Type=float)
b2 = XParameter(Name='b2', Format="<20s", Unit="", LongLabel='Magnetic quadrupole coefficient', Type=float)
b3 = XParameter(Name='b3', Format="<20s", Unit="", LongLabel='Magnetic octopole coefficient', Type=float)

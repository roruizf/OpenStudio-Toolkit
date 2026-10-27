"""Reference fields whose absence makes a typed OpenStudio accessor segfault.

Derived empirically for OpenStudio 3.11.0 by blanking one reference field at a time on one object of
each type found in the v0.3 corpus (58 types, 19 real models plus repo fixtures) and calling every
accessor that returns a related object directly. Script: docs/architecture/v0.3-evidence/blank_probe.py.
Types absent from that corpus are not covered; re-derive when the OpenStudio pin changes.
"""

from __future__ import annotations

DERIVED_FOR_OPENSTUDIO = "3.11.0"

# (IDD object type, IDD field name) -> accessors that die when the field is empty
FATAL_WHEN_ABSENT: dict[tuple[str, str], tuple[str, ...]] = {
    (
        "OS:AdditionalProperties",
        "Object Name",
    ): ("modelObject",),
    (
        "OS:AirConditioner:VariableRefrigerantFlow",
        "Availability Schedule",
    ): ("availabilitySchedule",),
    (
        "OS:AirLoopHVAC",
        "Demand Side Inlet Node A",
    ): ("demandInletNode",),
    (
        "OS:AirLoopHVAC",
        "Supply Side Outlet Node A",
    ): ("supplyOutletNode",),
    (
        "OS:AirLoopHVAC:OutdoorAirSystem",
        "Controller Name",
    ): ("getControllerOutdoorAir",),
    (
        "OS:AvailabilityManager:NightCycle",
        "Applicability Schedule",
    ): ("applicabilitySchedule",),
    (
        "OS:AvailabilityManager:ScheduledOn",
        "Schedule Name",
    ): ("schedule",),
    (
        "OS:CentralHeatPumpSystem:Module",
        "Chiller Heater Modules Control Schedule Name",
    ): ("chillerHeaterModulesControlSchedule",),
    (
        "OS:CentralHeatPumpSystem:Module",
        "Chiller Heater Modules Performance Component Name",
    ): ("chillerHeaterModulesPerformanceComponent",),
    (
        "OS:Chiller:Electric:EIR",
        "Cooling Capacity Function of Temperature Curve Name",
    ): ("coolingCapacityFunctionOfTemperature",),
    (
        "OS:Chiller:Electric:EIR",
        "Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve Name",
    ): ("electricInputToCoolingOutputRatioFunctionOfPLR",),
    (
        "OS:Chiller:Electric:EIR",
        "Electric Input to Cooling Output Ratio Function of Temperature Curve Name",
    ): ("electricInputToCoolingOutputRatioFunctionOfTemperature",),
    (
        "OS:ChillerHeaterPerformance:Electric:EIR",
        "Cooling Mode Cooling Capacity Function of Temperature Curve Name",
    ): ("coolingModeCoolingCapacityFunctionOfTemperatureCurve",),
    (
        "OS:ChillerHeaterPerformance:Electric:EIR",
        "Cooling Mode Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve Name",
    ): ("coolingModeElectricInputToCoolingOutputRatioFunctionOfPartLoadRatioCurve",),
    (
        "OS:ChillerHeaterPerformance:Electric:EIR",
        "Cooling Mode Electric Input to Cooling Output Ratio Function of Temperature Curve Name",
    ): ("coolingModeElectricInputToCoolingOutputRatioFunctionOfTemperatureCurve",),
    (
        "OS:ChillerHeaterPerformance:Electric:EIR",
        "Heating Mode Cooling Capacity Function of Temperature Curve Name",
    ): ("heatingModeCoolingCapacityFunctionOfTemperatureCurve",),
    (
        "OS:ChillerHeaterPerformance:Electric:EIR",
        "Heating Mode Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve Name",
    ): ("heatingModeElectricInputToCoolingOutputRatioFunctionOfPartLoadRatioCurve",),
    (
        "OS:ChillerHeaterPerformance:Electric:EIR",
        "Heating Mode Electric Input to Cooling Output Ratio Function of Temperature Curve Name",
    ): ("heatingModeElectricInputToCoolingOutputRatioFunctionOfTemperatureCurve",),
    (
        "OS:Coil:Cooling:DX:SingleSpeed",
        "Energy Input Ratio Function of Flow Fraction Curve Name",
    ): ("energyInputRatioFunctionOfFlowFractionCurve",),
    (
        "OS:Coil:Cooling:DX:VariableRefrigerantFlow",
        "Availability Schedule",
    ): ("availabilitySchedule",),
    (
        "OS:Coil:Cooling:DX:VariableRefrigerantFlow",
        "Cooling Capacity Modifier Curve Function of Flow Fraction",
    ): ("coolingCapacityModifierCurveFunctionofFlowFraction",),
    (
        "OS:Coil:Cooling:DX:VariableRefrigerantFlow",
        "Cooling Capacity Ratio Modifier Function of Temperature Curve",
    ): ("coolingCapacityRatioModifierFunctionofTemperatureCurve",),
    (
        "OS:Coil:Heating:DX:SingleSpeed",
        "Energy Input Ratio Function of Flow Fraction Curve Name",
    ): ("energyInputRatioFunctionofFlowFractionCurve",),
    (
        "OS:Coil:Heating:DX:SingleSpeed",
        "Energy Input Ratio Function of Temperature Curve Name",
    ): ("energyInputRatioFunctionofTemperatureCurve",),
    (
        "OS:Coil:Heating:DX:SingleSpeed",
        "Part Load Fraction Correlation Curve Name",
    ): ("partLoadFractionCorrelationCurve",),
    (
        "OS:Coil:Heating:DX:VariableRefrigerantFlow",
        "Availability Schedule",
    ): ("availabilitySchedule",),
    (
        "OS:Coil:Heating:DX:VariableRefrigerantFlow",
        "Heating Capacity Modifier Function of Flow Fraction Curve",
    ): ("heatingCapacityModifierFunctionofFlowFractionCurve",),
    (
        "OS:Coil:Heating:DX:VariableRefrigerantFlow",
        "Heating Capacity Ratio Modifier Function of Temperature Curve",
    ): ("heatingCapacityRatioModifierFunctionofTemperatureCurve",),
    (
        "OS:Controller:MechanicalVentilation",
        "Availability Schedule",
    ): ("availabilitySchedule",),
    (
        "OS:Controller:OutdoorAir",
        "Controller Mechanical Ventilation",
    ): ("controllerMechanicalVentilation",),
    (
        "OS:ElectricEquipment",
        "Electric Equipment Definition Name",
    ): ("definition", "electricEquipmentDefinition",),
    (
        "OS:EnergyManagementSystem:CurveOrTableIndexVariable",
        "Curve or Table Object Name",
    ): ("curveOrTableObject",),
    (
        "OS:Exterior:Lights",
        "Exterior Lights Definition Name",
    ): ("definition", "exteriorLightsDefinition",),
    (
        "OS:HeatExchanger:AirToAir:SensibleAndLatent",
        "Availability Schedule",
    ): ("availabilitySchedule",),
    (
        "OS:InternalMass",
        "Internal Mass Definition Name",
    ): ("definition", "internalMassDefinition",),
    (
        "OS:Lights",
        "Lights Definition Name",
    ): ("definition", "lightsDefinition",),
    (
        "OS:People",
        "People Definition Name",
    ): ("definition", "peopleDefinition",),
    (
        "OS:PlantLoop",
        "Demand Side Inlet Node Name",
    ): ("demandInletNode",),
    (
        "OS:PlantLoop",
        "Demand Side Outlet Node Name",
    ): ("demandOutletNode",),
    (
        "OS:PlantLoop",
        "Plant Side Inlet Node Name",
    ): ("supplyInletNode",),
    (
        "OS:PlantLoop",
        "Plant Side Outlet Node Name",
    ): ("supplyOutletNode",),
    (
        "OS:PortList",
        "HVAC Component",
    ): ("thermalZone",),
    (
        "OS:Schedule:Rule",
        "Day Schedule Name",
    ): ("daySchedule",),
    (
        "OS:Schedule:Ruleset",
        "Default Day Schedule Name",
    ): ("customDay1Schedule", "customDay2Schedule", "defaultDaySchedule", "holidaySchedule",),
    (
        "OS:SetpointManager:Scheduled",
        "Schedule Name",
    ): ("schedule",),
    (
        "OS:Sizing:Plant",
        "Plant or Condenser Loop Name",
    ): ("plantLoop",),
    (
        "OS:Sizing:System",
        "AirLoop Name",
    ): ("airLoopHVAC",),
    (
        "OS:Sizing:Zone",
        "Zone or ZoneList Name",
    ): ("thermalZone",),
    (
        "OS:StandardsInformation:Material",
        "Material Name",
    ): ("material",),
    (
        "OS:ThermalZone",
        "Zone Air Exhaust Port List",
    ): ("exhaustPortList",),
    (
        "OS:ThermalZone",
        "Zone Air Inlet Port List",
    ): ("inletPortList",),
    (
        "OS:ThermalZone",
        "Zone Air Node Name",
    ): ("zoneAirNode",),
    (
        "OS:ThermalZone",
        "Zone Return Air Port List",
    ): ("returnPortList",),
    (
        "OS:WaterHeater:Sizing",
        "WaterHeater Name",
    ): ("waterHeater",),
    (
        "OS:WaterUse:Equipment",
        "Water Use Equipment Definition Name",
    ): ("definition", "waterUseEquipmentDefinition",),
    (
        "OS:ZoneHVAC:EquipmentList",
        "Thermal Zone",
    ): ("thermalZone",),
    (
        "OS:ZoneHVAC:FourPipeFanCoil",
        "Cooling Coil Name",
    ): ("coolingCoil",),
    (
        "OS:ZoneHVAC:FourPipeFanCoil",
        "Heating Coil Name",
    ): ("heatingCoil",),
    (
        "OS:ZoneHVAC:FourPipeFanCoil",
        "Supply Air Fan Name",
    ): ("supplyAirFan",),
    (
        "OS:ZoneHVAC:PackagedTerminalHeatPump",
        "Heating Coil Name",
    ): ("heatingCoil",),
    (
        "OS:ZoneHVAC:TerminalUnit:VariableRefrigerantFlow",
        "Supply Air Fan",
    ): ("supplyAirFan",),
    (
        "OS:ZoneHVAC:TerminalUnit:VariableRefrigerantFlow",
        "Supply Air Fan Operating Mode Schedule",
    ): ("supplyAirFanOperatingModeSchedule",),
    (
        "OS:ZoneHVAC:TerminalUnit:VariableRefrigerantFlow",
        "Terminal Unit Availability schedule",
    ): ("terminalUnitAvailabilityschedule",),
    (
        "OS:ZoneMixing",
        "Schedule Name",
    ): ("schedule",),
    (
        "OS:ZoneMixing",
        "Zone or Space Name",
    ): ("zoneOrSpace",),
}

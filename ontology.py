import owlready2
owlready2.JAVA_EXE = "C:\Program Files\Java\jdk-13.0.2\\bin\java.exe"
onto        = owlready2.get_ontology("http://test.org/onto.owl")

with onto:
    class DomainThing(owlready2.Thing):
        pass

    class Module(onto.DomainThing):
        pass
    class ActuatorModule(Module):
        pass
    class SensorModule(Module):
        pass
    class CommunicationModule(Module):
        pass

    class SensorElement(onto.DomainThing):
        pass
    class Camera(SensorElement):
        pass
    # class Radiation(SensorElement):
    #     pass

    class ActuatorElement(onto.DomainThing):
        pass
    class Thruster(ActuatorElement):
        pass
    # class Motor(ActuatorElement):
    #     pass

    # class CommunicationElement(onto.DomainThing):
    #     pass

    class ValuePartition(owlready2.Thing):
        pass
    class Direction(onto.ValuePartition):
        pass
        # equivalent_to = [North | East | South | West | Up | Down]
    # north   = Direction()
    # east    = Direction()
    # south   = Direction()
    # west    = Direction()
    # up      = Direction()
    # down    = Direction()

    # Direction.is_a.append(owlready2.OneOf([north, east, south, west, up, down]))

    class North(Direction): pass
    class East(Direction):  pass
    class South(Direction): pass
    class West(Direction):  pass
    class Up(Direction):    pass
    class Down(Direction):  pass

    class has_for_direction(Module >> Direction):
        class_property_type = ["only"]
    # class has_for_direction(onto.ObjectProperty, onto.FunctionalProperty):
    #     domain  = [SensorElement]
    #     range   = [Direction]
    class has_for_sensor(Module >> SensorElement):
        class_property_type = ["some"]
    class has_for_actuator(Module >> ActuatorElement):
        class_property_type = ["some"]
    class is_communication(Module >> bool):
        pass
   
mod1 = Module("mod1")
mod2 = Module("mod2")
mod3 = Module("mod3")

owlready2.AllDifferent([mod1, mod2, mod3])

camera1 = Camera("camera1")
thruster = Thruster("thruster")

mod1.has_for_sensor = [camera1]
mod2.has_for_actuator = [thruster]
mod1.is_communication = [False]
mod2.is_communication = [False]
mod3.is_communication = [True]
mod1.has_for_direction = [Down]

owlready2.close_world(DomainThing)
owlready2.sync_reasoner(infer_property_values = True)
onto.save(file = "ontofilepls", format = "rdfxml")

print(mod1.has_for_sensor)
print(mod1.is_communication)
print(mod1.has_for_direction)
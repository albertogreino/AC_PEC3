from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter

from .model import EpsteinCivilViolence
from .agent import Citizen, Cop


COP_COLOR = "#000000"
AGENT_QUIET_COLOR = "#0066CC"
AGENT_REBEL_COLOR = "#CC0000"
JAIL_COLOR = "#757575"


def citizen_cop_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle",
                 "x": agent.pos[0], "y": agent.pos[1],
                 "Filled": "true"}

    if type(agent) is Citizen:
        color = AGENT_QUIET_COLOR if agent.condition == "Quiescent" else \
            AGENT_REBEL_COLOR
        color = JAIL_COLOR if agent.jail_sentence else color
        portrayal["Color"] = color
        portrayal["r"] = 0.8
        portrayal["Layer"] = 0

    elif type(agent) is Cop:
        portrayal["Color"] = COP_COLOR
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
    return portrayal


model_params = {
    "height": 40,
    "width": 40,
    "citizen_density": UserSettableParameter("slider", "Citizen density", 0.7, 0.1, 0.9, 0.1),
    "cop_density": UserSettableParameter("slider", "Cop density", 0.07, 0.01, 0.1, 0.01),
    "legitimacy": UserSettableParameter("slider", "Regime Legitimacy", 0.8, 0., 1.0, 0.1),
    "max_jail_term": UserSettableParameter("slider", "Max Jail term", 1000, 500, 1500, 100)
}

canvas_element = CanvasGrid(citizen_cop_portrayal, 40, 40, 480, 480)
server = ModularServer(EpsteinCivilViolence, [canvas_element],
                       "Epstein Civil Violence", model_params)

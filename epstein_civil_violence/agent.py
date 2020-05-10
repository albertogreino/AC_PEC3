import math

from mesa import Agent


class Citizen(Agent):
    """
    Un miembro de la población, puede estar o no en estado de rebelión.
    Resumen de su rol: If (grievance - risk) > threshold, then rebel.

    Atributos:
        unique_id: id único de tipo int
        x, y: Coordenadas de su posición
        hardship: El sufrimiento que percive el Agente 
            (ej., privación física o economica.)Se sacada de una distribución U(0,1).
        regime_legitimacy: La percepción del Agente de la legitimidad del regimen,
            es la misma para todos los agentes
        risk_aversion: La aversión al riesgo. Se saca de una distribución U(0,1).
        threshold: If (grievance - (risk_aversion * arrest_probability)) >
            threshold, then  Active
        condition: Puede ser "Quiescent" ("en calma") or "Active" ("activo"). 
            Función determinista que depende de los parametros
            greivance, perceived risk y risk_aversion.
        grievance: función de percepción de agravio del Agente que depende 
            de hardship y regime_legitimacy;
        arrest_probability: La probabilidad de que un Agente sea arrestado si está
            en rebelión.

    """

    def __init__(self, unique_id, model, pos, hardship, regime_legitimacy,
                 risk_aversion, threshold):
        """
        Crea un nuevo Agente Citizen.
        Args:
            unique_id: id único de tipo int
            x, y: Coordenadas de su posición
            hardship: El sufrimiento que percive el Agente 
                (ej., privación física o economica.)Se sacada de una distribución U(0,1).
            regime_legitimacy: La percepción del Agente de la legitimidad del regimen,
                es la misma para todos los agentes
            risk_aversion: La aversión al riesgo. Se saca de una distribución U(0,1).
            threshold: If (grievance - (risk_aversion * arrest_probability)) >
                threshold, then  Active
            model: instancia del modelo
        """
        super().__init__(unique_id, model)
        self.breed = 'citizen'
        self.pos = pos
        self.hardship = hardship
        self.regime_legitimacy = regime_legitimacy
        self.risk_aversion = risk_aversion
        self.threshold = threshold
        self.condition = "Quiescent"
        self.jail_sentence = 0
        self.grievance = self.hardship * (1 - self.regime_legitimacy)
        self.arrest_probability = None

    def step(self):
        """
        Decide si un Agente se activa, y se mueve si aplica.
        """
        if self.jail_sentence:
            self.jail_sentence -= 1
            return  # no other changes or movements if agent is in jail.
        self.update_neighbors()
        self.update_estimated_arrest_probability()
        net_risk = self.risk_aversion * self.arrest_probability
        if self.condition == 'Quiescent' and (
                self.grievance - net_risk) > self.threshold:
            self.condition = 'Active'
        elif self.condition == 'Active' and (
                self.grievance - net_risk) <= self.threshold:
            self.condition = 'Quiescent'
        if self.model.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.model.grid.move_agent(self, new_pos)

    def update_neighbors(self):
        """
        Mira alrededor y ve quienes son sus vecinos
        """
        self.neighborhood = self.model.grid.get_neighborhood(self.pos,
                                                        moore=False, radius=1)
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [c for c in self.neighborhood if
                                self.model.grid.is_cell_empty(c)]

    def update_estimated_arrest_probability(self):
        """
        Basada en el ratio de policias en el vecindario, estima la probabilidad
        p(Arrest | I go active).

        """
        cops_in_vision = len([c for c in self.neighbors if c.breed == 'cop'])
        actives_in_vision = 1.  # citizen counts herself
        for c in self.neighbors:
            if (c.breed == 'citizen' and
                    c.condition == 'Active' and
                    c.jail_sentence == 0):
                actives_in_vision += 1
        self.arrest_probability = 1 - math.exp(
            -1 * self.model.arrest_prob_constant * (
                cops_in_vision / actives_in_vision))


class Cop(Agent):
    """
    Un miembro de la policía.
    Resumen del rol: Inspecciona la visión local y arresta un agente 
    Citizen activo aleatoreamente.

    Atributos:
        unique_id: id único de tipo int
        x, y: Coordenadas de su posición
        policía puede inspeccionar.
    """

    def __init__(self, unique_id, model, pos):
        """
        Crear un nuevo agente Cop.
        Args:
            unique_id: id único de tipo int
            x, y: Coordenadas de su posición
            model: instancia del modelo
        """
        super().__init__(unique_id, model)
        self.breed = 'cop'
        self.pos = pos

    def step(self):
        """
        Inspect local vision and arrest a random active agent. Move if
        applicable.
        """
        self.update_neighbors()
        active_neighbors = []
        for agent in self.neighbors:
            if agent.breed == 'citizen' and \
                    agent.condition == 'Active' and \
                    agent.jail_sentence == 0:
                active_neighbors.append(agent)
        if
        for active_neighbor in active_neighbors:
            arrestee = active_neighbor
            sentence = self.random.randint(0, self.model.max_jail_term)
            arrestee.jail_sentence = sentence
        if self.model.movement and self.empty_neighbors:
            new_pos = self.random.choice(self.empty_neighbors)
            self.model.grid.move_agent(self, new_pos)

    def update_neighbors(self):
        """
        Look around and see who my neighbors are.
        """
        self.neighborhood = self.model.grid.get_neighborhood(self.pos,
                                                        moore=False, radius=1)
        self.neighbors = self.model.grid.get_cell_list_contents(self.neighborhood)
        self.empty_neighbors = [c for c in self.neighborhood if
                                self.model.grid.is_cell_empty(c)]

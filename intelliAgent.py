import random
import pygame
import math
import csv

# We create a class target.
class Target:
	def __init__(self, x,y, name, color):
		# This class has four attributes: 
		# x and y the coordinates of the target, the  name and the color of the target.
		self.x = x
		self.y = y
		self.name = name
		self.color = color

	# The graphic representation of a goal is a cross
	# The cross has the color of the target and its center 
	# is in coordinates x and y of the target.
	def draw(self, window):
		pygame.draw.line(window, self.color, [self.x-3,self.y-3], [self.x+3,self.y+3], 4)
		pygame.draw.line(window, self.color, [self.x-3,self.y+3], [self.x+3,self.y-3], 4)

# We create a class target Agent
class Agent:
	def __init__(self, x,y, name, color, targets, steps = 0):
		# This class has seven attributes: 
		# coordinates of the agent, name and color of the agent, 
		# a list of targets, the number of steps taken by the agent and 
		# the trace of the agent.
		self.x = x
		self.y = y
		self.name = name
		self.color = color
		self.targets = targets
		self.steps = steps
		self.trace = []

	def choice_of_route(self,agents):
		# This function specifies the possible coordinates for the agent movement
		# randomly determine the direction of movement
		k = random.randint(1,2)
		if k == 1:
			x = 5*(-6)**random.randint(1,2)
			y = 0
		else:
			x = 0
			y = 5*(-6)**random.randint(1,2)
		
		# the condition of falling into the boundaries of the playing field
		field = ((self.x + x) in range(1, 500)) and ((self.y + y) in range(1, 500))
		
		# the condition that agents will not encounter
		collision = True
		for agent in agents:
			if self.x == agent.x and self.y == agent.y:
				collision = False
				break
		# the condition does not move on the already traversed path
		path = [self.x + x, self.y + y] not in self.trace

		# all conditions must be met
		condition = field and collision and path 
		t = 0 
		# carry out the loop until all conditions are met
		while not condition :
			t += 1
			# if the conditions are not fulfilled, we determine the new random direction of movement
			k = random.randint(1,2)
			if k == 1:
				x = 5*(-6)**random.randint(1,2)
				y = 0
			else:
				x = 0
				y = 5*(-6)**random.randint(1,2)
			field = ((self.x + x) in range(1, 500)) and ((self.y + y) in range(1, 500))
			collision = True
			for agent in agents:
				if self.x == agent.x and self.y == agent.y:
					collision = False
					break
			path = [self.x + x, self.y + y] not in self.trace

			# After 20 impossible moves, we allow the agent to move on the path already traveled.
			if t < 20:
				condition = field and collision and path
			else:
				condition = field and collision
		# determine the new position of the agent
		self.x += x
		self.y += y
		self.trace.append([self.x, self.y])

	def draw(self, window):
		# draw the agent
		pygame.draw.ellipse(window, self.color, [self.x-5,self.y-5, 10, 10], 0)
		# draw the trace
		for i in range(len(self.trace) - 1):
			pygame.draw.line(window, self.color, self.trace[i], self.trace[i + 1], 2)


def achievement_targets(agents):
	# This function determines whether the agent has found its a target.
	# If the target is found, it is removed from the agent's list of goals.
	for agent in agents:
		for target in agent.targets:
			if (agent.x - target.x)**2 + (agent.y - target.y)**2 <= 50**2:
				agent.targets.remove(target)

		
def achievement_goal(agents, case):
	# this function determines whether the goal for different scenarios is reached.
	if case == '1' or case == '3':
		for agent in agents:
			if agent.targets == []:
				return True
	if case == '2':
		for agent in agents:
			if agent.targets != []:
				return False
		return True

	return False

def number_iterations(agents, case):
    # This function follows the number of steps taken by all agents.
    if case == '1' or case == '3':
    	for agent in agents:
    		agent.steps += 1
    else:
    	for agent in agents:
    		if agent.targets != []:
    			agent.steps += 1

def channels(agents, case):
	# This function returns a message about found target of the agent in accordance 
	# with the selected script.
	if case == '1' or case == '3':
	    for agent_1 in agents:
	    	for agent_2 in agents:
	    		for target in agent_2.targets:
	    			if (agent_1.x - target.x)**2 + (agent_1.y - target.y)**2 <= 50**2:
	    				# print a message if the target of the agent j hits the radar of the agent i
	    				print(agent_1.name + " locates a target of " + agent_2.name)
	
	if case == '2':
	    for agent_1 in agents:
	    	for agent_2 in agents:
	    		for target in agent_2.targets:
	    			if (agent_1.x - target.x)**2 + (agent_1.y - target.y)**2 <= 50**2:
	    				# print a message if the target of the agent j hits the radar of the agent i
	    				print(agent_1.name + " to " + agent_2.name + ": I found your target")
	    				

def results_CSV_file(agents, case, step):
	# write the result in two CSV-files
	fieldnames1 = ["case number", "Iteration number", "Agent number", "Number of collected targets by the agent", "Number of steps taken by the agent at the end of iteration", "Agent happiness", "Maximum happiness in each iteration",  "Minimum happiness in each iteration", "Average happiness in each iteration", "Standard deviation of happiness in each iteration", "Agent competitiveness"]
	result1 = []
	for agent in agents:
		item = []
		item.append(case)
		item.append(step)
		item.append(agent.name)
		item.append(5 - len(agent.targets))
		item.append(agent.steps)
		item.append((5 - len(agent.targets))/(agent.steps + 1))
		lst = [(5 - len(x.targets))/(x.steps + 1) for x in agents]
		item.append(max(lst))
		item.append(min(lst))
		item.append(sum(lst)/5)
		item.append(math.sqrt(1/5*sum([(x - sum(lst)/5)**2 for x in lst])))
		item.append(((5 - len(agent.targets))/(agent.steps + 1) - min(lst))/(max(lst) - min(lst)))

		result1.append(item)

		
	file1  = open("G30_1.csv", "w", newline='')
	writer = csv.writer(file1)
	writer.writerow(fieldnames1)
	for row in result1:
		writer.writerow(row)
	file1.close()


	fieldnames2 = ["case number", "Average of column 'i' ", "Average of column 'k'"]
	file2  = open("G30_2.csv", "a", newline='')
	writer = csv.writer(file2)
	writer.writerow([case, sum(lst)/5, math.sqrt(1/5*sum([(x - sum(lst)/5)**2 for x in lst]))])
	
	file2.close()


def main():
	# define colors
	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)
	YELLOW = (231, 232, 89)
	GREEN = (33, 128, 43)
	RED = (206, 8, 43)
	BLUE = (16, 108, 190)
	
	colors = [BLACK, YELLOW, GREEN, RED, BLUE]
	names = ["Agent A", "Agent B", "Agent C", "Agent D", "Agent E"]

	# The user must specify a scenario number
	case = input("Input case (1,2 or 3): ")
	while case not in ['1', '2', '3']:
		case = input("Input error! Input case (1,2 or 3): ")	
	
	# We randomly place agents and their goals in the playing field
	agents = []
	for i in range(5):
		targets = []
		for j in range(5):
			targets.append(Target(random.randint(1, 500), random.randint(1, 500), "T" + names[i][6] + str(j+1), colors[i]))
		
		agents.append(Agent(random.randint(1, 500), random.randint(1, 500), names[i], colors[i], targets))

	# initialize graphic mode
	pygame.init()
	# For better visualization, all objects are increased 5 times. 
	# Therefore, the playing field has a size of 500 to 500.
	size = (500, 500)
	window = pygame.display.set_mode(size)
	pygame.display.set_caption("Design and implementation of a multi-agent system")
	 
	# this variable is responsible for an infinite loop
	done = False
	# first move
	step = 1
	
	clock = pygame.time.Clock()
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		window.fill(WHITE)

		# draw agents
		for agent in agents:
			agent.draw(window)
		# draw targets
			for target in agent.targets:
				target.draw(window)

		# change the position of the agents
		for agent_1 in agents:
			new_agents = []
			for agent_2 in agents:
				if agent_1 != agent_2:
					new_agents.append(agent_2)
			agent_1.choice_of_route(new_agents)

		# collect targets that fall within the scope of the radar
		achievement_targets(agents)
		number_iterations(agents, case)
		channels(agents, case)

		# check the condition for the game to end
		if achievement_goal(agents, case):
			done = True

		pygame.display.flip()

		step += 1
		clock.tick(20)
	 
	# Close the window and quit.
	pygame.quit()

	results_CSV_file(agents, case, step)


if __name__=="__main__":
	main()


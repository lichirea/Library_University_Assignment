from ui.console import Console
import os


f = open("settings.properties", "r")
folder = os.getcwd()
folder = folder + "\\repo\\"

line = f.readline().strip().split()
repository = line[2]

line = f.readline().strip().split()
books = folder + line[2].strip()

line = f.readline().strip().split()
clients = folder + line[2]

line = f.readline().strip().split()
rentals = folder + line[2]

start = Console(repository, books, clients, rentals)
start.initialize()
start.start()

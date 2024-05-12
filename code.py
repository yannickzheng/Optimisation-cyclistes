import pygame
import random
import math

class VeloRacing:
    def __init__(self):
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None

        self.wind_particles = []
        self.velo_speed_data = []

        # Coordinates for cyclist
        self.velo_x_coordinate = (self.display_width * 0.45)
        self.velo_y_coordinate = (self.display_height * 0.8)

        self.cyclists = [
            (self.display_width * 0.35, self.display_height * 0.7),
            (self.display_width * 0.55, self.display_height * 0.6),
            (self.display_width * 0.2, self.display_height * 0.4),
            (self.display_width * 0.7, self.display_height * 0.3),
            (self.display_width * 0.8, self.display_height * 0.7),
            (self.display_width * 0.3, self.display_height * 0.5),
        ]

        self.initialize()

    def initialize(self):
        self.crashed = False

        self.veloImg = pygame.image.load("images/cyclist.png")
        self.velo_width = 49

        # Load image for cyclist2
        self.cyclist2Img = pygame.image.load("images/cyclist2.png")

        self.start_time = pygame.time.get_ticks()

        # Background
        self.bgImg = pygame.image.load("images/back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3

        # Load wind particle image
        self.wind_particle_img = pygame.image.load("images/wind.png")

        # Initialize wind particles
        num_particles = 3  # Adjust the number of wind particles
        for _ in range(num_particles):
            particle = {
                'x': random.randint(0, self.display_width),
                'y': random.randint(0, self.display_height),
                'speed': random.uniform(0.5, 2)  # Adjust the speed of wind particles
            }
            self.wind_particles.append(particle)

    def move_cyclists(self):
        center_x = self.display_width * 0.5
        center_y = self.display_height * 0.4
        radius = 100
        angular_speed = 0.001  # Ajustez cette valeur pour la vitesse de rotation constante

        for i in range(len(self.cyclists)):
            angle = i * (2 * math.pi / len(self.cyclists)) + pygame.time.get_ticks() * angular_speed
            self.cyclists[i] = (
                center_x + radius * math.cos(angle),
                center_y + radius * math.sin(angle),
            )

    def velo(self, velo_x_coordinate, velo_y_coordinate, img):
        self.gameDisplay.blit(img, (velo_x_coordinate, velo_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('jeu')
        self.run_velo()

    def run_velo(self):
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.velo_x_coordinate -= 50
                    if event.key == pygame.K_RIGHT:
                        self.velo_x_coordinate += 50

            self.gameDisplay.fill(self.black)
            self.back_ground_road()
            self.move_cyclists()

            # Calculate and display speed
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Convert milliseconds to seconds
            speed_kmh = self.calculate_speed_kmh(elapsed_time)
            self.velo_speed_data.append(speed_kmh)

            self.display_speed(speed_kmh)
            self.velo(self.velo_x_coordinate, self.velo_y_coordinate, self.veloImg)
            for cyclist in self.cyclists:
                self.velo(cyclist[0], cyclist[1], self.cyclist2Img)
            self.draw_wind_particles()
            self.draw_speed_curve()

            pygame.display.update()
            self.clock.tick(60)

    def back_ground_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def draw_wind_particles(self):
        for particle in self.wind_particles:
            particle['y'] += particle['speed']
            self.gameDisplay.blit(self.wind_particle_img, (particle['x'], particle['y']))

            if particle['y'] > self.display_height:
                particle['y'] = 0

    def calculate_speed_kmh(self, elapsed_time):
        # Ajustez la vitesse initiale à 35 km/h
        initial_speed_kmh = 35
        # Ajustez la constante d'accélération
        acceleration = 0.1

        # Formule pour calculer la vitesse
        speed_kmh = initial_speed_kmh + acceleration * elapsed_time
        return speed_kmh

    def display_speed(self, speed_kmh):
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Speed: {:.2f} km/h".format(speed_kmh), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def draw_speed_curve(self):
        if len(self.velo_speed_data) > 1:
            # Ajustez ces valeurs pour définir la position et la taille de la courbe
            curve_x = self.display_width - 220  # Décalage vers la gauche
            curve_y = 20
            curve_width = 200
            curve_height = 120

            max_speed = max(self.velo_speed_data)
            min_speed = min(self.velo_speed_data)
            speed_range = max_speed - min_speed

            points = [(i * curve_width / len(self.velo_speed_data) + curve_x,
                       curve_y + curve_height - (speed - min_speed) / speed_range * curve_height)
                      for i, speed in enumerate(self.velo_speed_data)]

            pygame.draw.lines(self.gameDisplay, self.white, False, points, 2)

if __name__ == '__main__':
    velo_racing = VeloRacing()
    velo_racing.racing_window()

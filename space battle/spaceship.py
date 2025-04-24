import pygame
import os
from configuration import *


class Spaceship:
    def __init__(self, x, y, image, controls, left_bound, right_bound):
        self.rect = pygame.Rect(x, y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.image = image
        self.controls = controls
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.health = 10
        self.bullets = []

    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        for bullet in self.bullets:
            pygame.draw.rect(WIN, RED if self.image == RED_SPACESHIP else YELLOW, bullet)

    def move(self, keys_pressed):
        if keys_pressed[self.controls['left']] and self.rect.x - VEL > self.left_bound:
            self.rect.x -= VEL
        if keys_pressed[self.controls['right']] and self.rect.x + VEL + self.rect.width < self.right_bound:
            self.rect.x += VEL
        if keys_pressed[self.controls['up']] and self.rect.y - VEL > 0:
            self.rect.y -= VEL
        if keys_pressed[self.controls['down']] and self.rect.y + VEL + self.rect.height < HEIGHT - 15:
            self.rect.y += VEL

    def shoot(self, direction):
        if len(self.bullets) < MAX_BULLETS:
            bullet = pygame.Rect(
                self.rect.x + (self.rect.width if direction > 0 else -10),
                self.rect.y + self.rect.height // 2 - 2,
                10, 5
            )
            self.bullets.append(bullet)
            BULLET_FIRE_SOUND.play()
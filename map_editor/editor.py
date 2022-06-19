import pygame
import json

display = pygame.display.set_mode((700, 1400))
clock = pygame.time.Clock()

blocks = {"map": []}
with open("assets/map/map.json", "r") as f:
    json_string = json.load(f)
    blocks = json_string


while True:
    display.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("assets/map/map.json", "w") as f:
                json_string = json.dumps(blocks)
                json.dump(json_string, f)
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()

                blocks["map"].append([(mx//16)*16, (my//16)*16, 16, 16])

            if event.button == 3:
                mx, my = pygame.mouse.get_pos()
                for idx, block in enumerate(blocks["map"]):
                    if blocks["map"][idx] == [(mx//16)*16, (my//16)*16, 16, 16]:
                        blocks["map"].pop(idx)


    for block in blocks["map"]:
        pygame.draw.rect(display, (255, 0, 0), block)

    pygame.display.update()
    clock.tick(60)
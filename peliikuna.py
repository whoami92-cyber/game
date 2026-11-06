
import pygame
import random

pygame.init()

pisteet = 0

kolikko_x = random.randint(0, 750)
kolikko_y = random.randint(0, 550)

pelaaja_x = 375
pelaaja_y = 275

naytto = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Eka peli")
fontti = pygame.font.Font(None, 36)
bonus_fontti = pygame.font.Font(None, 32)

bonus_aktiivinen = False
bonus_alku = 0
bonus_x = 0
bonus_y = 0
pisteet = 0

pelin_alku = pygame.time.get_ticks()
pelin_kesto = 30000
peli_ohi = False

fontti = pygame.font.Font(None, 36)
bonus_fontti = pygame.font.Font(None, 32)

kello = pygame.time.Clock()
kaynissa = True

tausta = pygame.image.load("kuvat/mars.png").convert()
tausta = pygame.transform.scale(tausta, (800, 600))


kerays_aani = pygame.mixer.Sound("kolikko.wav")
peliloppu = pygame.mixer.Sound("gameover.mp3")

aani_soitettu = False


while kaynissa:
    kulunut_aika = pygame.time.get_ticks() - pelin_alku
    aikaa_jaljella = max(0, (pelin_kesto - kulunut_aika) // 1000)
    pelaaja= pygame.image.load("kuvat/pelaaja.png").convert_alpha()
    pelaaja = pygame.transform.scale(pelaaja, (80, 80))

    kolikko = pygame.image.load("kuvat/kolikko.png").convert_alpha()
    kolikko = pygame.transform.scale(kolikko, (50, 50))
    # Tapahtumat
    for tapahtuma in pygame.event.get():
        if tapahtuma.type == pygame.QUIT:
            kaynissa = False

        if tapahtuma.type == pygame.KEYDOWN:
            if tapahtuma.key == pygame.K_ESCAPE:
                kaynissa = False

    if aikaa_jaljella > 0:
        napit = pygame.key.get_pressed()

        if napit[pygame.K_d]:
            pelaaja_x += 5
        if napit[pygame.K_a]:
            pelaaja_x -= 5
        if napit[pygame.K_w]:
            pelaaja_y -= 5
        if napit[pygame.K_s]:
            pelaaja_y += 5

        pelaaja_x = max(0, min(pelaaja_x, 720))
        pelaaja_y = max(0, min(pelaaja_y, 520))

        pelaaja_rect = pygame.Rect(pelaaja_x, pelaaja_y, 80, 80)
        kolikko_rect = pygame.Rect(kolikko_x, kolikko_y, 20, 20)

        if pelaaja_rect.colliderect(kolikko_rect):
            pisteet += 1
            kerays_aani.play()

            kolikko_x = random.randint(0, 780)
            kolikko_y = random.randint(0, 580)

            bonus_aktiivinen = True
            bonus_alku = pygame.time.get_ticks()
            bonus_x = pelaaja_x + 20
            bonus_y = pelaaja_y - 10

    # Piirtäminen
    naytto.blit(tausta, (0, 0))

    if aikaa_jaljella > 0:
       naytto.blit(kolikko, (kolikko_x, kolikko_y))
    naytto.blit(pelaaja, (pelaaja_x, pelaaja_y))

    aika_teksti = fontti.render(
        f"Aikaa: {aikaa_jaljella}", True, (255, 255, 255)
    )
    naytto.blit(aika_teksti, (10, 50))

    teksti = fontti.render(f"Pisteet: {pisteet}", True, (255, 255, 255))
    naytto.blit(teksti, (10, 10))

    # Pomppaava +1
    if bonus_aktiivinen:
        kulunut = pygame.time.get_ticks() - bonus_alku

        if kulunut < 700:
            bonus = bonus_fontti.render("+1", True, (0, 255, 0))
            bonus.set_alpha(255 - int(255 * kulunut / 700))
            naytto.blit(bonus, (bonus_x, bonus_y - kulunut // 20))
        else:
            bonus_aktiivinen = False

    # Game Over
    if aikaa_jaljella == 0:
        if not aani_soitettu:
            peliloppu.play()
            aani_soitettu = True

        gameover_teksti = fontti.render(
            "GAME OVER!", True, (255, 255, 255)
        )
        naytto.blit(gameover_teksti, (320, 270))

    pygame.display.flip()
    kello.tick(60)

pygame.quit()


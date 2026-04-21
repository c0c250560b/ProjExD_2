import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#　演習課題１
def gameover(screen: pg.Surface) -> None:  # ゲームオーバーの画面を表示する関数
    gm_img = pg.Surface((WIDTH, HEIGHT))  # ゲームオーバーの背景を作成
    gm_img.set_alpha(200)  # 透明度を設定
    screen.blit(gm_img,screen.get_rect())  # ゲームオーバーの背景を画面に描く
    fonto = pg.font.Font(None, 80)  # フォントを作成
    txt = fonto.render("GAME OVER", True, (255, 255, 255))  # ゲームオーバーの文字を描く
    screen.blit(txt, [300,200])  # ゲームオーバーの文字を画面に描く
    kk_img = pg.image.load("fig/8.png").convert_alpha()  # こうかとんの画像を読み込む
    screen.blit(kk_img, [200,200])  # こうかとんの画像を画面に描く
    screen.blit(kk_img, [700,200])  # こうかとんの画像を画面に描く
    pg.display.update()  # ゲームオーバーの画面を更新
    time.sleep(5)  # ゲームオーバーの画面を5秒間表示する

# 演習課題２
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []  
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r), pg.SRCALPHA)  
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]

    return bb_imgs, bb_accs

def check_bound(rct : pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向、縦方向判定効果（True: 画面内　False: 画面外）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img = pg.Surface((20, 20))  # 爆弾の画像を作成
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾を赤い円で描く 
    bb_img.set_colorkey((0, 0, 0))  # 爆弾の黒い部分を透過する
    bb_rct = bb_img.get_rect()  # 爆弾のRectを取得
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 爆弾の位置をランダムに設定
    vx, vy = +5, +5  # 爆弾の速度を設定

    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0

    bb_imgs, bb_accs = init_bb_imgs()
    avx = vx*bb_accs[min(tmr//500,9)]
    avy = vy*bb_accs[min(tmr//500,9)]
    bb_img = bb_imgs[min(tmr//500,9)]
    bb_rct.move_ip(avx, avy)
    bb_rct.width = bb_img.get_rect().width
    bb_rct.height = bb_img.get_rect().height
    
    while True:
        
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が重なったら
            gameover(screen)
            print("ゲームオーバー")
            return  # ゲームオーバーになったらmain関数を抜ける
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
            # sum_mv[0] += 5
        DELTA = {
            pg.K_UP: (0, -5),
            pg.K_DOWN: (0, +5),
            pg.K_LEFT: (-5, 0),
            pg.K_RIGHT: (+5, 0)
        }
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) !=(True, True):  # こうかとんが画面外に出たら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])


        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾を動かす
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向の判定
            vx *= -1
        if not tate:  # 縦方向の判定
            vy *= -1

        screen.blit(bb_img, bb_rct)  # 爆弾を画面に描く
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

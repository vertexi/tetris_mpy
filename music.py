from libs.buzzer_music import Music
from machine import Pin
from control import DelayEvent

# tetris theme modified by https://onlinesequencer.net/2591896
theme_music = '0 E6 4 43;4 B5 2 43;6 C6 2 43;8 D6 2 43;10 E6 1 43;11 D6 1 43;12 C6 ' \
              '2 43;14 B5 2 43;20 A5 2 43;22 C6 2 43;24 E6 4 43;28 D6 2 43;30 C6 2 ' \
              '43;32 B5 6 43;38 C6 2 43;40 D6 4 43;44 E6 4 43;48 C6 4 43;52 A5 4 ' \
              '43;56 A5 8 43;66 D6 4 43;70 F6 2 43;72 A6 4 43;76 G6 2 43;78 F6 2 ' \
              '43;80 E6 6 43;86 C6 2 43;88 E6 4 43;92 D6 2 43;94 C6 2 43;96 B5 4 ' \
              '43;100 B5 2 43;102 C6 2 43;104 D6 4 43;108 E6 4 43;112 C6 4 43;116 ' \
              'A5 4 43;120 A5 4 43;128 E6 4 43;132 B5 2 43;134 C6 2 43;136 D6 2 ' \
              '43;138 E6 1 43;139 D6 1 43;140 C6 2 43;142 B5 2 43;144 A5 4 43;148 ' \
              'A5 2 43;150 C6 2 43;152 E6 4 43;156 D6 2 43;158 C6 2 43;160 B5 6 ' \
              '43;166 C6 2 43;168 D6 4 43;172 E6 4 43;176 C6 4 43;180 A5 4 43;184 ' \
              'A5 8 43;194 D6 4 43;198 F6 2 43;200 A6 4 43;204 G6 2 43;206 F6 2 ' \
              '43;208 E6 6 43;214 C6 2 43;216 E6 4 43;220 D6 2 43;222 C6 2 43;224 ' \
              'B5 4 43;228 B5 2 43;230 C6 2 43;232 D6 4 43;236 E6 4 43;240 C6 4 ' \
              '43;244 A5 4 43;248 A5 4 43;256 E5 8 43;264 C5 8 43;272 D5 8 43;280 ' \
              'B4 8 43;288 C5 8 43;296 A4 8 43;304 G#4 8 43;312 B4 4 43;320 E5 8 ' \
              '43;328 C5 8 43;336 D5 8 43;344 B4 8 43;352 C5 4 43;356 E5 4 43;360 ' \
              'A5 8 43;368 G#5 8 43;384 E6 4 43;388 B5 2 43;390 C6 2 43;392 D6 2 ' \
              '43;394 E6 1 43;395 D6 1 43;396 C6 2 43;398 B5 2 43;400 A5 4 43;404 ' \
              'A5 2 43;406 C6 2 43;408 E6 4 43;412 D6 2 43;414 C6 2 43;416 B5 6 ' \
              '43;422 C6 2 43;424 D6 4 43;428 E6 4 43;432 C6 4 43;436 A5 4 43;440 ' \
              'A5 8 43;450 D6 4 43;454 F6 2 43;456 A6 4 43;460 G6 2 43;462 F6 2 ' \
              '43;464 E6 6 43;470 C6 2 43;472 E6 4 43;476 D6 2 43;478 C6 2 43;480 ' \
              'B5 4 43;484 B5 2 43;486 C6 2 43;488 D6 4 43;492 E6 4 43;496 C6 4 ' \
              '43;500 A5 4 43;504 A5 4 43;512 E6 4 43;516 B5 2 43;518 C6 2 43;520 ' \
              'D6 2 43;522 E6 1 43;523 D6 1 43;524 C6 2 43;526 B5 2 43;528 A5 4 ' \
              '43;532 A5 2 43;534 C6 2 43;536 E6 4 43;540 D6 2 43;542 C6 2 43;544 ' \
              'B5 6 43;550 C6 2 43;552 D6 4 43;556 E6 4 43;560 C6 4 43;564 A5 4 ' \
              '43;568 A5 8 43;578 D6 4 43;582 F6 2 43;584 A6 4 43;588 G6 2 43;590 ' \
              'F6 2 43;592 E6 6 43;598 C6 2 43;600 E6 4 43;604 D6 2 43;606 C6 2 ' \
              '43;608 B5 4 43;612 B5 2 43;614 C6 2 43;616 D6 4 43;620 E6 4 43;624 ' \
              'C6 4 43;628 A5 4 43;632 A5 4 43;16 A5 4 43 '

# https://onlinesequencer.net/145939
celebrate_music = '0 E5 1 0;1 E5 1 0;3 E5 1 0;5 C5 1 0;6 E5 1 0;8 G5 1 0;12 G4 1 0'


class MusicEvent(DelayEvent):
    music: Music
    def __init__(self, time_threshold, callback_handle, music):
        super(MusicEvent, self).__init__(time_threshold, callback_handle)
        self.music = music

    def restart(self):
        self.music.restart()

    def stop(self):
        self.music.stop()

    def resume(self):
        self.music.resume()


class Musics:
    def __init__(self, *args):
        self.musics = []
        for arg in args:
            self.musics.append(MusicEvent(*arg))
        self.current_music = self.musics[0]
        self.pause_ = False

    def tick(self, celebrate=False):
        if celebrate:
            self.current_music = self.musics[1]
            self.current_music.restart()
            self.current_music.tick()
        if not self.pause_:
            if not self.current_music.tick():
                self.current_music= self.musics[0]

    def pause(self):
        for music in self.musics:
            music.stop()
        self.pause_ = True

    def resume(self):
        for music in self.musics:
            music.resume()
        self.pause_ = False


musics: Musics = None


def set_up_musics(pin):
    global musics
    theme_music_ = Music(theme_music, looping=True, tempo=3, duty=256,
                        pins=[Pin(pin)])
    celebrate_music_ = Music(celebrate_music, looping=False, tempo=3, duty=256,
                            pins=[Pin(pin)])
    musics = Musics([40, theme_music_.tick, theme_music_],
                    [40, celebrate_music_.tick, celebrate_music_])

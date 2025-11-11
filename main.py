from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from hand import HandController
from voice import VoiceAssistant
import cv2

class SplashScreen(Screen): pass
class ModeSelectScreen(Screen): pass
class HandControlScreen(Screen): pass
class VoiceControlScreen(Screen): pass

Builder.load_file("splash.kv")
Builder.load_file("gui.kv")

class VoiceHandApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.capture = None
        self.hand_controller = HandController()
        self.voice_assistant = VoiceAssistant()

        self.sm.add_widget(SplashScreen(name='splash'))
        self.sm.add_widget(ModeSelectScreen(name='mode_select'))
        self.sm.add_widget(HandControlScreen(name='hand'))
        self.sm.add_widget(VoiceControlScreen(name='voice'))

        self.sm.current = 'splash'
        Clock.schedule_once(self.goto_mode_select, 3)
        return self.sm

    def goto_mode_select(self, dt):
        self.sm.current = 'mode_select'

    def start_hand_mode(self):
        self.capture = cv2.VideoCapture(0)
        self.sm.current = 'hand'
        Clock.schedule_interval(self.update_hand_feed, 1.0 / 30.0)

    def update_hand_feed(self, dt):
        frame = self.hand_controller.process_frame()
        if frame is None:
            return
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.sm.get_screen('hand').ids.hand_cam.texture = texture

    def stop_hand_mode(self):
        if self.capture:
            self.capture.release()
        Clock.unschedule(self.update_hand_feed)

    def start_voice_mode(self):
        self.sm.current = 'voice'

    def listen_to_voice(self):
        command = self.voice_assistant.listen()
        if command:
            self.voice_assistant.run_command(command)

    def on_stop(self):
        if self.capture:
            self.capture.release()

if __name__ == '__main__':
    VoiceHandApp().run()

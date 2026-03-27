from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText

class UIManager:
    def __init__(self):
        self.message_node = OnscreenText(
            text="Initializing...",
            pos=(0, 0),
            scale=0.07,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
            mayChange=True
        )
        
        self.score_node = OnscreenText(
            text="Score: 0",
            pos=(-1.3, 0.9), # Top Left
            scale=0.07,
            fg=(1, 1, 0, 1),
            align=TextNode.ALeft,
            mayChange=True
        )
        
        self.debug_node = OnscreenText(
            text="",
            pos=(-1.3, -0.95), # Bottom Left
            scale=0.05,
            fg=(0.5, 1, 0.5, 1),
            align=TextNode.ALeft,
            mayChange=True
        )

    def show_message(self, msg, duration=0):
        self.message_node.setText(msg)
        self.message_node.show()
        # Duration logic handling would go here or be managed by caller clearing it

    def hide_message(self):
        self.message_node.hide()

    def update_score(self, score):
        self.score_node.setText(f"Score: {int(score)}")

    def update_debug(self, msg):
        self.debug_node.setText(msg)

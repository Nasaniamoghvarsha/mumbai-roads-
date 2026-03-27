from direct.showbase.ShowBase import ShowBase
from panda3d.core import Texture, NodePath, TextNode, CardMaker, AmbientLight, DirectionalLight, Vec4, Fog, TextureStage
import sys

class DebugApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept('escape', sys.exit)
        
        # Text info
        self.text_node = TextNode('info')
        self.text_np = self.aspect2d.attachNewNode(self.text_node)
        self.text_np.setScale(0.07)
        self.text_np.setPos(-0.9, 0, 0.9)
        
        # Load Level Segment Mockup
        self.seg = NodePath("Segment")
        self.seg.reparentTo(self.render)
        self.seg.setPos(0, 20, 0)
        
        # 1. Floor (Scaled like game)
        self.floor = self.loader.loadModel("models/box")
        self.floor.reparentTo(self.seg)
        self.floor.setScale(10, 50, 0.1)
        self.floor.setPos(0, 0, -0.1)
        
        # 2. Wall (Scaled like game)
        self.wall = self.loader.loadModel("models/box")
        self.wall.reparentTo(self.seg)
        # Note: In game, wall is parented to segment (10, 50, 0.1)?
        # Game code: seg.setScale(10, 50, 0.1). Wall reparented to Seg?
        # NO. Game code: wall_l.reparentTo(seg).
        # IF wall reparented to scaled seg, wall scale (0.1, 1, 100) combines!
        # Result: 10*0.1=1, 50*1=50, 0.1*100=10.
        # Let's mimic parenting exactly.
        
        self.seg.setScale(10, 50, 0.1)
        
        # Re-attach walls to scaled segment
        self.wall_l = self.loader.loadModel("models/box")
        self.wall_l.reparentTo(self.seg)
        self.wall_l.setScale(0.1, 1, 100)
        self.wall_l.setPos(-0.55, 0, 50)
        
        # Load Textures
        self.floor_tex = self.loader.loadTexture("game/assets/floor.jpg")
        self.wall_tex = self.loader.loadTexture("game/assets/wall.jpg")
        
        self.floor.setTexture(self.floor_tex)
        self.wall_l.setTexture(self.wall_tex)
        
        # Apply Logic
        self.ts = TextureStage.getDefault()
        self.floor.setTexScale(self.ts, 2, 10)
        self.wall_l.setTexScale(self.ts, 10, 2)

        # Skip simplistic 'box' var
        self.box = self.floor 
        self.tex_path = "game/assets/floor.jpg" 
        self.tex = self.floor_tex
        
        self.mode = 0
        self.lights_on = False
        self.fog_on = False
        self.repeat_on = False
        self.modes = [
            "Texture: Default",
            "Texture: Compression OFF",
            "Texture: RGB Format"
        ]
        
        self.accept('space', self.cycle_mode)
        self.accept('l', self.toggle_lights)
        self.accept('f', self.toggle_fog)
        self.accept('r', self.toggle_repeat)
        
        self.update_mode()
        print("Debug App Started. SPACE: Mode | L: Lights | F: Fog | R: Repeat")

    def cycle_mode(self):
        self.mode = (self.mode + 1) % len(self.modes)
        self.update_mode()
        
    def toggle_lights(self):
        self.lights_on = not self.lights_on
        if self.lights_on:
            self.setup_lights()
        else:
            self.render.clearLight()
        self.update_mode()

    def toggle_fog(self):
        self.fog_on = not self.fog_on
        if self.fog_on:
            self.fog = Fog("SceneFog")
            self.fog.setColor(0.1, 0.1, 0.15)
            # ... (rest of fog code same)
            self.fog.setExpDensity(0.01)
            self.render.setFog(self.fog)
            self.setBackgroundColor(0.1, 0.1, 0.15)
        else:
            self.render.clearFog()
            self.setBackgroundColor(0.5, 0.5, 0.5)
        self.update_mode()

    def toggle_repeat(self):
        self.repeat_on = not self.repeat_on
        self.update_mode()

    def setup_lights(self):
        self.render.clearLight()
        alight = AmbientLight('alight')
        alight.setColor(Vec4(0.4, 0.4, 0.5, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        dlight = DirectionalLight('dlight')
        dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        dnp = self.render.attachNewNode(dlight)
        dnp.setHpr(0, -60, 0)
        self.render.setLight(dnp)

    def update_mode(self):
        desc = self.modes[self.mode]
        status = f"Lights: {'ON' if self.lights_on else 'OFF'} | Fog: {'ON' if self.fog_on else 'OFF'} | Repeat: {'ON' if self.repeat_on else 'OFF'}"
        self.text_node.setText(f"Mode: {desc}\n{status}\n[L] Lights [F] Fog [R] Repeat")
        print(f"Switching to {desc} (Repeat: {self.repeat_on})")
        
        self.box.clearTexture()
        self.box.clearColor()
        self.box.setTextureOff(1)
        
        # Always reload to be fresh
        self.tex = self.loader.loadTexture(self.tex_path)
        
        # Apply Repeat if ON
        if self.repeat_on:
            self.tex.setWrapU(Texture.WMRepeat)
            self.tex.setWrapV(Texture.WMRepeat)
            # Make it obvious by scaling UVs
            self.box.setTexScale(TextureStage.getDefault(), 2, 2)
        else:
            self.tex.setWrapU(Texture.WMClamp)
            self.tex.setWrapV(Texture.WMClamp)
            self.box.setTexScale(TextureStage.getDefault(), 1, 1)
            
        if self.mode == 0:
            # Default
            self.box.setColor(1, 1, 1, 1)
            self.box.setTexture(self.tex)
            
        elif self.mode == 1:
            # Comp Off
            self.box.setColor(1, 1, 1, 1)
            self.tex.setCompression(Texture.CMOff)
            self.box.setTexture(self.tex)

        elif self.mode == 2:
            # RGB
            self.box.setColor(1, 1, 1, 1)
            self.tex.setFormat(Texture.F_rgb)
            self.box.setTexture(self.tex)

app = DebugApp()
app.run()

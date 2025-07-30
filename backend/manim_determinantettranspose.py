from manim import *
import os
class Ma(Scene):
    def construct(self):
        map=NumberPlane(background_line_style={
            "stroke_color":BLUE_E,
            "stroke_width":1,
            "stroke_opacity":0.5
        })
        map.axes.set_opacity(0)
        self.add(map)

        # Chemin vers le fichier audio (chemin relatif par rapport à l'emplacement du script)
        audio_file = os.path.join(os.path.dirname(__file__), "determinant.mp3")
        
        # Vérifier si le fichier audio existe
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Le fichier audio n'a pas été trouvé à l'emplacement: {audio_file}")
            
        # Démarrer la lecture audio
        self.add_sound(audio_file)
        print(f"Fichier audio chargé depuis: {audio_file}")
        
        # Animation du titre
        det = Text("Determinant",
                 font="times new roman",
                 font_size=70).set_color_by_gradient(PURPLE, WHITE, PURPLE, WHITE)
        self.play(Write(det))

        a2=Text("The determinant of A{2x2} matrix is :").set_color_by_gradient(BLUE,WHITE,BLUE).shift(UP*2.5).scale(0.8)
        A=Text("A=").set_color_by_gradient(PURPLE,WHITE)
        m2=Matrix([
            [1,2],
            [0,4]
        ]).next_to(A,RIGHT)
        ma2=VGroup(A,m2).shift(LEFT*1.5)
        self.play(GrowFromCenter(ma2),
                  det.animate.shift(UP*3.5).scale(0.7))
        self.wait(0.5)
        da2=Text(r"Det(A)=").set_color_by_gradient(PURPLE,WHITE)
        m22=m2.copy().next_to(da2,RIGHT)

        l=Polygon([0,-1,0],[0,1,0],color=WHITE,stroke_width=3).next_to(m22,LEFT,buff=0.1)
        r=l.copy().next_to(m22,RIGHT,buff=0.1)

        deta=VGroup(m22,da2,l,r).shift(LEFT*3.5)
        da2[0].set_color(PURPLE)
        
        self.play(FadeIn(a2),
                  Transform(ma2,deta)
                  )
        cc=RoundedRectangle(
            width=0.6,
            height=2,
            corner_radius=0.1,  # Độ bo tròn góc
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.2
        ).rotate(60*DEGREES).move_to(m22)
        self.wait(0.5)
        f1=MathTex(r"=",
                   r"1 \times 4",
                   r"\quad - \quad",
                   r"2 \times 0").next_to(r,RIGHT)
        f1[1].set_color_by_gradient(BLUE,WHITE,BLUE)
        f1[3].set_color_by_gradient(YELLOW,WHITE,YELLOW)

        self.play(GrowFromCenter(cc),
                  Write(f1[0]),Write(f1[1]))
        self.wait()
        self.play(cc.animate.flip(RIGHT).set_color(YELLOW),
                  Write(f1[2]),Write(f1[3]))
        f2=MathTex(r"=4").next_to(r,RIGHT).set_color_by_gradient(PURPLE,WHITE,PURPLE)
        self.wait()
        self.play(Transform(f1,f2),FadeOut(cc))
        f12=VGroup(ma2,f1)
        self.play(f12.animate.shift(RIGHT*1.5))
        box = RoundedRectangle(
            corner_radius=0.2,  # Bo góc
            width=f12.width + 0.2,
            height=f12.height + 0.2,
            stroke_width=4
        ).move_to(f12).set_color([PURPLE,WHITE])
        self.play(Create(box))
        e1=VGroup(a2,box,f12)

        B=Text("B=").set_color_by_gradient(PURPLE,WHITE)
        m3=Matrix([
            [1,2,3],
            [0,4,5],
            [1,0,6]
        ]).next_to(B,RIGHT)
        mb3=VGroup(B,m3).shift(LEFT*2.5)

        b2=Text("The determinant of B{3x3} matrix is :").shift(UP*2.5).set_color_by_gradient(BLUE,WHITE,BLUE).scale(0.8)
        B2=VGroup(mb3,b2)



        self.play(FadeOut(e1,shift=RIGHT,lag_ratio=0),
                  FadeIn(B2,shift=RIGHT))
        
        ll=Polygon([0,1.5,0],[0,-1.5,0],color=WHITE,stroke_width=3).next_to(m3,LEFT,buff=0.1)
        rr=ll.copy().next_to(m3,RIGHT,buff=0.1)
        det1=Text("Det(B)=").set_color_by_gradient(PURPLE,WHITE).next_to(m3,LEFT)
        

        self.play(Transform(B,det1),FadeIn(ll,rr))
        detb=VGroup(B,m3,ll,rr)
        self.play(detb.animate.shift(UP*0.5+RIGHT*0.5).scale(0.8))

        bb=RoundedRectangle(
            width=0.6,
            height=3,
            corner_radius=0.1,  # Độ bo tròn góc
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.2
        ).rotate(60*DEGREES).move_to(m3)
        br=bb.copy().flip(RIGHT).set_color(YELLOW)
        bb1=cc.copy().move_to(m3).shift(UP*0.3+RIGHT*0.5).scale(0.8).flip(RIGHT).set_color(BLUE)
        bb2=cc.copy().move_to(m3).shift(UP*0.3+LEFT*0.5).scale(0.8)
        br1=RoundedRectangle(
            width=0.6,
            height=0.5,
            corner_radius=0.2,  # Độ bo tròn góc
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.2
        ).move_to(m3.get_entries()[6])


        t1=MathTex(r"=",
                   r"1.4.6",
                   r"+",
                   r"2.5.1",
                   r"+",
                   r"3.0.0",
                   r"\quad-\quad",
                   r"3.4.1",
                   r"-",
                   r"2.0.6",
                   r"-",
                   r"1.5.0").shift(DOWN*1.5)
        t2=MathTex(r"=22").set_color_by_gradient(WHITE,PURPLE).shift(DOWN*1.5)
        tc=VGroup(t1[1],t1[3],t1[5]).set_color(BLUE)
        tp=VGroup(t1[7],t1[9],t1[11]).set_color(YELLOW)

        self.play(Create(bb),Write(t1[0]),Write(t1[1]))
        self.wait(0.5)
        self.play(Transform(bb,bb1),Create(br1),
                  Write(t1[2]),Write(t1[3]))
        self.wait(0.5)
        self.play(bb.animate.shift(DOWN*0.6+LEFT*1),
                  br1.animate.move_to(m3.get_entries()[2]),
                  Write(t1[4]),Write(t1[5]))
        self.wait(0.5)
        self.play(Transform(bb,br),FadeOut(br1),
                  Write(t1[6]),Write(t1[7]))
        self.wait(0.5)
        br1.move_to(m3.get_entries()[8]).set_color(YELLOW)
        self.play(Transform(bb,bb2),Create(br1),
                  Write(t1[8]),Write(t1[9]))
        self.wait(0.5)
        self.play(bb.animate.shift(DOWN*0.6+RIGHT*1),
                  br1.animate.move_to(m3.get_entries()[0]),
                  Write(t1[10]),Write(t1[11]))
        self.wait(0.5)
        self.play(Transform(t1,t2),FadeOut(br1,bb))
        self.play(t1.animate.next_to(m3,direction=RIGHT))
        bv=VGroup(detb,t1)
        self.play(bv.animate.shift(DOWN*0.5).scale(1.2))
        box2=RoundedRectangle(
            corner_radius=0.2,  # Bo góc
            width=bv.width + 0.2,
            height=bv.height + 0.2,
            stroke_width=4
        ).set_color([PURPLE,WHITE]).move_to(bv)
        self.play(Create(box2))
        

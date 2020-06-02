from browsergui import *


class LiveGUI(GUI):
    def __init__(self, **kwargs):
        super(LiveGUI, self).__init__(**kwargs)
        # predefined text elements
        self.texta = EmphasizedText("Live Control Center")
        self.textb = Text("Marshall Ar.Ts \n \n")

        #self.w_field = TextField(value=str(3), placeholder='width')
        #self.h_field = TextField(value=str(5), placeholder='height')

        #self.mine_density = 0.1
        # self.mine_density_slider = FloatSlider(
        #    value=self.mine_density, min=0, max=1)
        #self.reset_button = Button('Reset and Apply')
        self.body.append(self.textb)
        self.body.append(self.texta)

        self.body.append(Grid([
            [self.textb],
            [self.texta]]))
        # self.body.append(Viewport(
        #    CodeBlock('\n' + self.texta) + '\n'),
        #    width=500, height=900))
        # self.body.append(Grid([
        #    [Text('width'), Text('height'), Text(
        #        'mine density'), self.texta, ],
        #    [self.w_field, self.h_field,
        #        Container(Text('0'), self.mine_density_slider, Text('1')),
        #        self.reset_button, self.textb]]))
        #self.grid = None
        self.body.append(self.textb)
        self.body.append(self.texta)

        # self.reset()


def main():
    LiveGUI().run()


if __name__ == '__main__':
    main()
